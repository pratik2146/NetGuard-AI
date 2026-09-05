import os
from datetime import datetime
from typing import Dict, Any, Tuple, List, Optional
from pymongo import MongoClient

from netguard.config import MONGODB_URI, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME
from netguard.utils.logger import logger

class MongoPredictionLogger:
    """
    MongoDB client wrapper for prediction telemetry logging and history retrieval.
    """
    def __init__(
        self,
        uri: str = MONGODB_URI,
        db_name: str = MONGODB_DB_NAME,
        collection_name: str = MONGODB_COLLECTION_NAME,
        timeout_ms: int = 1500
    ):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.timeout_ms = timeout_ms

    def test_connection(self) -> bool:
        """
        Check if MongoDB server is reachable.
        """
        try:
            client = MongoClient(self.uri, serverSelectionTimeoutMS=self.timeout_ms)
            client.admin.command("ping")
            client.close()
            return True
        except Exception:
            return False

    def log_prediction(self, record: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Save prediction record to MongoDB.
        """
        try:
            client = MongoClient(self.uri, serverSelectionTimeoutMS=self.timeout_ms)
            client.admin.command("ping")
            
            db = client[self.db_name]
            collection = db[self.collection_name]
            
            if "timestamp" not in record:
                record["timestamp"] = datetime.now().isoformat()
                
            collection.insert_one(record)
            client.close()
            
            logger.info("Successfully saved prediction to MongoDB.")
            return True, "Prediction saved successfully to MongoDB."
        except Exception as exc:
            logger.warning(f"MongoDB connection unavailable: {exc}")
            return False, "MongoDB is not connected. The prediction result remains fully valid."

    def get_recent_predictions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve recent saved prediction logs from MongoDB.
        """
        try:
            client = MongoClient(self.uri, serverSelectionTimeoutMS=self.timeout_ms)
            db = client[self.db_name]
            collection = db[self.collection_name]
            
            records = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
            client.close()
            return records
        except Exception as exc:
            logger.warning(f"Failed to fetch history from MongoDB: {exc}")
            return []
