from loguru import logger
import sys


logger.add(sys.stdout, serialize=True)
