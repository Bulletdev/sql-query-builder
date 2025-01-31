import logging
import logging.config
import os
from datetime import datetime

def setup_logger():
    """Configura o logger com rotação de arquivos diária."""
    # Cria diretório de logs se não existir
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Nome do arquivo de log com data
    log_file = os.path.join(
        log_dir, 
        f'app_{datetime.now().strftime("%Y%m%d")}.log'
    )

    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

# Cria logger global
logger = setup_logger()