import logging

# Configure logger
logger = logging.getLogger(__name__)

class Common:
    @staticmethod
    def create_payload(status, message, error, data):
        payload = {
            "status": status,
            "message": message,
            "error": error,
            "data": data
        }
        return payload