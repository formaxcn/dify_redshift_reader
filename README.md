# Redshift Reader Plugin for Dify

[The Redshift Reader](https://github.com/formaxcn/dify_redshift_reader) is a Dify plugin that provides workflow nodes with the ability to read data from Amazon Redshift data warehouse. This plugin allows you to execute SQL SELECT queries against your Redshift cluster and retrieve the results for use in your Dify workflows. It connects to Redshift using the PostgreSQL protocol rather than AWS native authentication.

## Features

- Secure connection to Amazon Redshift clusters via PostgreSQL protocol
- SQL query execution with built-in security checks
- Support for parameterized queries
- Data retrieval with configurable row limits
- JSON formatted output for easy integration with Dify workflows

## Prerequisites

- Access to an Amazon Redshift cluster
- Valid database credentials (host, port, database name, username, password)
- Dify platform instance

## Installation

1. Package the plugin according to Dify plugin specifications
2. Upload the plugin to your Dify instance
3. Configure the plugin with your Redshift connection credentials

## Configuration

The plugin requires the following configuration parameters:

- **Host**: The host address of your Redshift cluster
- **Port**: The port number of your Redshift cluster (default: 5439)
- **Database Name**: The name of your Redshift database
- **Username**: Your Redshift username
- **Password**: Your Redshift password
- **Max Fetched Rows**: Maximum number of rows to fetch (default: 100)

## Usage

Once configured, you can use the Redshift Reader tool in your Dify workflows:

1. Add the "Redshift Reader" tool to your workflow
2. Provide a SQL SELECT query as input
3. The tool will execute the query and return:
   - `data`: Array of row data
   - `columns`: Array of column names
   - JSON object with column-value mappings

### Example

```sql
SELECT customer_id, customer_name, email 
FROM customers 
WHERE registration_date >= '2024-01-01'
LIMIT 10
```

## Implementation Reference

This plugin's implementation references the [db-client-node](https://github.com/spance/db-client-node) project for database connectivity and query handling patterns.

## Security

- Only SELECT operations are allowed (no INSERT, UPDATE, DELETE, etc.)
- Parameterized queries are supported to prevent SQL injection
- Connection credentials are securely stored
- No personal user information is collected or stored by the plugin

## Limitations

- Only supports SELECT queries
- Maximum row limit configurable but capped for performance
- Connects via PostgreSQL protocol rather than AWS native authentication
- No support for transactions or stored procedures

## License

See LICENSE file for details.