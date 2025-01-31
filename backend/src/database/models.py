from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class JoinCondition:
    """Configuração para JOINs entre tabelas."""
    table: str
    left_column: str
    right_column: str
    join_type: str = 'inner'  # inner, left, right, full

    def validate(self) -> None:
        """Valida as configurações do JOIN."""
        valid_types = {'inner', 'left', 'right', 'full'}
        if self.join_type not in valid_types:
            raise ValueError(f"Tipo de JOIN inválido. Deve ser um de: {valid_types}")

@dataclass
class QueryFilter:
    """Filtro para cláusula WHERE."""
    column: str
    operator: str
    value: Any
    connector: str = 'AND'

    def validate(self) -> None:
        """Valida o filtro."""
        valid_operators = {'=', '>', '<', '>=', '<=', '<>', 'LIKE', 'IN', 'NOT IN'}
        if self.operator not in valid_operators:
            raise ValueError(f"Operador inválido. Deve ser um de: {valid_operators}")

@dataclass
class QueryConfig:
    """Configuração completa para construção de queries."""
    db_type: str
    user: str
    password: str
    host: str
    db_name: str
    main_table: str
    columns: List[str]
    joins: List[JoinCondition]
    filters: Optional[List[QueryFilter]] = None
    group_by: Optional[List[str]] = None
    order_by: Optional[List[str]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> None:
        """Valida toda a configuração da query."""
        # Valida joins
        for join in self.joins:
            join.validate()

        # Valida filtros
        if self.filters:
            for filter in self.filters:
                filter.validate()

        # Valida limit e offset
        if self.limit is not None and self.limit <= 0:
            raise ValueError("Limit deve ser maior que zero")
        if self.offset is not None and self.offset < 0:
            raise ValueError("Offset não pode ser negativo")

@dataclass
class QueryResult:
    """Resultado da execução da query."""
    success: bool
    data: List[Dict[str, Any]]
    query: str
    execution_time: float
    total_rows: int
    error: Optional[str] = None
    details: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)