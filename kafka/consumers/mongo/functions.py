import logging
from mongo.connect_mongo import collection

# Setting logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs
    ]
)
  
def save_processed_message(processed_message:dict):
    try:
        collection.insert_one(processed_message)
        logging.info(f"Saved to MongoDB: {processed_message}")
            
    except Exception as e:
        logging.error(f"Error saving to MongoDB: {e}")
