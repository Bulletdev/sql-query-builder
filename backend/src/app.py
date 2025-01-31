from flask import Flask, request, jsonify
from datetime import datetime
import time
import logging.config
import yaml
from database.manager import DatabaseManager
from database.models import QueryConfig, QueryResult
from query.builder import QueryBuilder

# Configuração do app
app = Flask(__name__)
db_manager = DatabaseManager('config.yml')

# Configuração de logging
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config['logging'])

logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde da API."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/query', methods=['POST'])
def execute_query():
    """Endpoint principal para execução de queries."""
    try:
        start_time = time.time()
        
        # Valida e cria configuração
        config = QueryConfig(**request.json)
        config.validate()

        # Obtém conexão e executa query
        with db_manager.get_connection(
            config.db_type, config.user, config.password, 
            config.host, config.db_name
        ) as connection:
            # Obtém metadados e constrói query
            metadata = db_manager.get_metadata(connection)
            query_builder = QueryBuilder(metadata)
            query = query_builder.build_query(config)

            # Executa query e processa resultados
            result = connection.execute(query)
            data = [dict(row) for row in result]

            # Cria resultado
            execution_time = time.time() - start_time
            query_result = QueryResult(
                success=True,
                data=data,
                query=str(query),
                execution_time=execution_time,
                total_rows=len(data)
            )

            return jsonify(query_result.__dict__)

    except Exception as e:
        logger.error(f"Erro ao executar query: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e.__class__.__name__),
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(
        host=config['api']['host'],
        port=config['api']['port'],
        debug=config['api']['debug']
    )