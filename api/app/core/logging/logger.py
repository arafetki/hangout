import logging
from config import settings
import coloredlogs

logger = logging.getLogger(settings.project_name)
coloredlogs.install(level=logging.INFO, logger=logger, fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
