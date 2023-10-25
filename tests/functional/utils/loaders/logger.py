import logging


backoff_logger = logging.getLogger('back_off_logger')
_back_off_handler = logging.StreamHandler()
backoff_logger.addHandler(_back_off_handler)
backoff_logger.setLevel(logging.INFO)
