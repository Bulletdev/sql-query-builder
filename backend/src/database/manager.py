from typing import Dict, Optional
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
import yaml

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerencia conexões com diferentes tipos de bancos de dados."""
    
    SUPPORTED_DBS = {
        'mysql': 'mysql+pymysql',
        'postgresql': 'postgresql',
        'oracle': 'oracle+cx_oracle',
        'mssql': 'mssql+pyodbc'
    }

    def __init__(self, config_path: str = 'config.yml'):
        self.engines: Dict[str, Engine] = {}
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> dict:
        """Carrega configurações do arquivo YAML."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            raise

    def get_engine(self, db_type: str, user: str, password: str, 
                   host: str, db_name: str) -> Engine:
        """Obtém ou cria uma engine SQLAlchemy para o banco especificado."""
        if db_type not in self.SUPPORTED_DBS:
            raise ValueError(f"Banco de dados não suportado: {db_type}")

        connection_key = f"{db_type}://{user}@{host}/{db_name}"
        
        if connection_key not in self.engines:
            db_config = self.config['databases'].get(db_type, {})
            connection_string = (
                f"{self.SUPPORTED_DBS[db_type]}://"
                f"{user}:{password}@{host}/{db_name}"
            )
            
            self.engines[connection_key] = create_engine(
                connection_string,
                pool_size=db_config.get('pool_size', 5),
                max_overflow=db_config.get('max_overflow', 10),
                pool_timeout=db_config.get('pool_timeout', 30),
                pool_recycle=db_config.get('pool_recycle', 3600)
            )
            
        return self.engines[connection_key]

    @contextmanager
    def get_connection(self, db_type: str, user: str, password: str, 
                      host: str, db_name: str):
        """Context manager para obter uma conexão do pool."""
        engine = self.get_engine(db_type, user, password, host, db_name)
        try:
            connection = engine.connect()
            yield connection
        finally:
            connection.close()

    def get_metadata(self, engine: Engine) -> MetaData:
        """Obtém metadados das tabelas do banco de dados."""
        metadata = MetaData()
        try:
            metadata.reflect(bind=engine)
            return metadata
        except SQLAlchemyError as e:
            logger.error(f"Erro ao obter metadados: {e}")
            raise