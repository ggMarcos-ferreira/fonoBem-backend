import logging
from logging import handlers

# Configuração do logger
logger = logging.getLogger(__name__)

# Criando manipuladores de log
fileHandler = handlers.RotatingFileHandler("my_log.log", maxBytes=2000, backupCount=10)
consoleHandler = logging.StreamHandler()  # Adicionando o console handler

# Definindo o formato de log
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

# Configurando o nível de log
logger.setLevel(logging.INFO)
fileHandler.setLevel(logging.INFO)
consoleHandler.setLevel(logging.INFO)

# Adicionando manipuladores ao logger
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

