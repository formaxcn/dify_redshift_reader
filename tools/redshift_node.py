import logging
from typing import Any, Dict, Generator, Tuple

import psycopg2
from dify_plugin import Tool
from dify_plugin.config.logger_format import plugin_logger_handler
from dify_plugin.entities.tool import ToolInvokeMessage
from jinja2 import Template
from sqlglot import exp, parse_one

from provider import dbcn_provider
from tools.api import SQLType, typeOf

logger = logging.getLogger(__name__)
logger.addHandler(plugin_logger_handler)


class RedshiftNode(Tool):

    def __init__(self, runtime, session):
        super().__init__(runtime, session)
        try:
            credentials = self.runtime.credentials or runtime.credentials
            self.db_config, config = dbcn_provider.get_config(credentials)
            self.max_fetched_rows = config["max_fetched_rows"]
            if not self.max_fetched_rows:
                self.max_fetched_rows = 100
        except Exception as e:
            logger.error(f"Failed to initialize database conn: {str(e)}")

    def _check_conn(self):
        """
        插件短生命周期无法建立连接池
        """
        db_conn = psycopg2.connect(**self.db_config)
        logger.warning(f"Initialized database conn: {db_conn}")
        return db_conn

    def _check_query(self, query: str) -> Tuple[SQLType, str]:
        """
        1. 进行sql语法分析ast 找到参数变量后替换为psycopg2的命名参数
        2. 基于语法分析ast 确定该sql的DML类型
        """
        if not query:
            raise ValueError("SQL query is required")

        try:
            ast = parse_one(query, dialect="postgres")  # Ex.
        except BaseException as ex:
            # maybe ex is pyo3_runtime.PanicException
            raise ValueError(f"SQL syntax error, query={query}. caused by={ex}")

        # logger.warning(f"SQL exp={ast} type={type(ast)}")
        for p in ast.find_all(exp.Placeholder):
            raise ValueError("Not allowed Placeholder -> `?`, Should use `$arg0~N`")
        for p in ast.find_all(exp.Parameter):
            raise ValueError("Parameters are not allowed in Redshift Reader")
        return typeOf(ast), ast.sql()  # Ex.

    def _invoke(
        self, parameters: Dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        query: str = parameters.get("query")

        sql_type, sql_exp = self._check_query(query)
        
        # 仅支持SELECT操作
        if sql_type != SQLType.SELECT:
            raise ValueError("Only SELECT operations are allowed in Redshift Reader plugin")
            
        conn = self._check_conn()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql_exp)
            columns = [cn[0] for cn in cursor.description]
            results = cursor.fetchmany(self.max_fetched_rows)

            logger.warning(f"SQL-select exp={sql_exp}, count={len(results)}")
            yield self.create_variable_message("data", results)
            yield self.create_variable_message("columns", columns)
            data = [dict(zip(columns, row)) for row in results]
            yield self.create_json_message({"data": data})

        except Exception as ex:
            logger.exception(f"SQL={sql_exp}, casued by={type(ex)}: {ex}")
            raise RuntimeError(f"{type(ex)}: {ex}") from ex

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()