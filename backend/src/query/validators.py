from typing import List, Dict, Any
from ..database.models import QueryConfig, JoinCondition, QueryFilter

class QueryValidator:
    """Validador para configurações de query."""

    @staticmethod
    def validate_table_name(table_name: str) -> bool:
        """Valida o nome de uma tabela."""
        # Remove esquema se existir
        if '.' in table_name:
            schema, table = table_name.split('.')
            table_name = table

        # Regras básicas para nomes de tabela
        return (
            table_name.isalnum() or 
            all(c.isalnum() or c == '_' for c in table_name)
        )

    @staticmethod
    def validate_column_name(column_name: str) -> bool:
        """Valida o nome de uma coluna."""
        # Remove tabela se especificada
        if '.' in column_name:
            table, column = column_name.split('.')
            column_name = column

        # Regras básicas para nomes de coluna
        return (
            column_name.isalnum() or 
            all(c.isalnum() or c == '_' for c in column_name)
        )

    @classmethod
    def validate_query_config(cls, config: QueryConfig) -> List[str]:
        """Valida toda a configuração da query."""
        errors = []

        # Valida tabela principal
        if not cls.validate_table_name(config.main_table):
            errors.append(f"Nome de tabela inválido: {config.main_table}")

        # Valida colunas
        for column in config.columns:
            if not cls.validate_column_name(column):
                errors.append(f"Nome de coluna inválido: {column}")

        # Valida joins
        for join in config.joins:
            if not cls.validate_table_name(join.table):
                errors.append(f"Nome de tabela inválido no join: {join.table}")
            if not cls.validate_column_name(join.left_column):
                errors.append(f"Nome de coluna inválido no join: {join.left_column}")
            if not cls.validate_column_name(join.right_column):
                errors.append(f"Nome de coluna inválido no join: {join.right_column}")

        return errors

    @classmethod
    def sanitize_query_config(cls, config: QueryConfig) -> QueryConfig:
        """Sanitiza a configuração da query para prevenir SQL injection."""
        # Cria uma cópia da config para não modificar a original
        sanitized = QueryConfig(
            db_type=config.db_type,
            user=config.user,
            password=config.password,
            host=config.host,
            db_name=config.db_name,
            main_table=config.main_table,
            columns=[],
            joins=[],
            filters=config.filters,
            group_by=config.group_by,
            order_by=config.order_by,
            limit=config.limit,
            offset=config.offset
        )

        # Sanitiza colunas
        sanitized.columns = [
            column for column in config.columns 
            if cls.validate_column_name(column)
        ]

        # Sanitiza joins
        sanitized.joins = [
            join for join in config.joins
            if (cls.validate_table_name(join.table) and
                cls.validate_column_name(join.left_column) and
                cls.validate_column_name(join.right_column))
        ]

        return sanitized