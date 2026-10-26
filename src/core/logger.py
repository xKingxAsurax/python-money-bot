import logging
import sys

def setup_logger() -> logging.Logger:
    """
    Configures and returns the central logger for the application.
    """
    logger = logging.getLogger("EcoOfertasBot")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Global logger instance
logger = setup_logger()
