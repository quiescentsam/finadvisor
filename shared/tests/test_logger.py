from shared.utils.logger import get_logger

def test_logger_creates_instance():
    logger = get_logger("test")
    assert logger.name == "test"
    assert logger.level == 20  # INFO