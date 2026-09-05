from netguard.db.mongo import MongoPredictionLogger

def test_mongo_logger_fallback():
    # Attempt logging to unreachable server address to test safe offline fallback
    logger = MongoPredictionLogger(uri="mongodb://localhost:27018/", timeout_ms=300)
    success, msg = logger.log_prediction({"test": "data"})
    assert success is False
    assert "MongoDB is not connected" in msg
