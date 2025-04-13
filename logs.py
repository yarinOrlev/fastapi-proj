import logging
import logging.handlers as handlers

logging.basicConfig(level=logging.DEBUG, filename= "blogs.log", filemode= "w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

formatter = logging.Formatter("%(asctime)s - %(name)s -  %(levelname)s - %(message)s")

file_handler = handlers.TimedRotatingFileHandler('test.log', when="midnight",interval=1,backupCount=3)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARN)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)



