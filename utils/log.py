import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Capture all levels of logs

# Formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Info log handler
info_handler = logging.FileHandler('logs/info.log')
info_handler.setLevel(logging.INFO)  # Only capture INFO and above (INFO, WARNING, ERROR, CRITICAL)
info_handler.setFormatter(formatter)

# Error log handler
error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)  # Only capture ERROR and above (ERROR, CRITICAL)
error_handler.setFormatter(formatter)

# Console log handler (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

# # Example usage
# logger.debug("This is a debug message")  # Won't be written to files but shown in console
# logger.info("This is an info message")   # Written to info.log and console
# logger.warning("This is a warning message")  # Written to info.log and console
# logger.error("This is an error message")  # Written to error.log, info.log, and console
# logger.critical("This is a critical message")  # Written to error.log, info.log, and console
