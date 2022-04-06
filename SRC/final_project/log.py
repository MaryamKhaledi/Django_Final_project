import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('user.log')
file_handler.setLevel(level=logging.INFO)

file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
file_handler.setFormatter(file_format)

logger.addHandler(file_handler)
