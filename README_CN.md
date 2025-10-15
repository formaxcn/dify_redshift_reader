# Dify的Redshift读取器插件

Redshift读取器是一个Dify插件，为工作流节点提供从Amazon Redshift数据仓库读取数据的能力。该插件允许您对Redshift集群执行SQL SELECT查询，并检索结果以在您的Dify工作流中使用。它使用PostgreSQL协议而不是AWS原生认证来连接Redshift。

## 功能特点

- 通过PostgreSQL协议安全连接Amazon Redshift集群
- 执行SQL查询并内置安全检查
- 支持参数化查询
- 可配置行数限制的数据检索
- JSON格式输出，便于与Dify工作流集成

## 前提条件

- 访问Amazon Redshift集群
- 有效的数据库凭证（主机、端口、数据库名、用户名、密码）
- Dify平台实例

## 安装

1. 根据Dify插件规范打包插件
2. 将插件上传到您的Dify实例
3. 使用您的Redshift连接凭证配置插件

## 配置

插件需要以下配置参数：

- **主机地址**：Redshift集群的主机地址
- **端口**：Redshift集群的端口号（默认：5439）
- **数据库名**：Redshift数据库的名称
- **用户名**：Redshift用户名
- **密码**：Redshift密码
- **最大获取行数**：要获取的最大行数（默认：100）

## 使用方法

配置完成后，您可以在Dify工作流中使用Redshift读取器工具：

1. 将"Redshift读取器"工具添加到您的工作流中
2. 提供SQL SELECT查询作为输入
3. 工具将执行查询并返回：
   - `data`：行数据数组
   - `columns`：列名数组
   - 包含列值映射的JSON对象

### 示例

```sql
SELECT customer_id, customer_name, email 
FROM customers 
WHERE registration_date >= '2024-01-01'
LIMIT 10
```

## 实现参考

本插件的实现在数据库连接和查询处理模式方面参考了[db-client-node](https://github.com/spance/db-client-node)项目。

## 安全性

- 仅允许SELECT操作（不允许INSERT、UPDATE、DELETE等）
- 支持参数化查询以防止SQL注入
- 连接凭证安全存储
- 插件不收集或存储任何个人用户信息

## 限制

- 仅支持SELECT查询
- 最大行数限制可配置但有性能上限
- 通过PostgreSQL协议连接而非AWS原生认证
- 不支持事务或存储过程

## 许可证

有关详细信息，请参阅LICENSE文件。