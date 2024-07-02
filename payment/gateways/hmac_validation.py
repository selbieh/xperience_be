import hashlib
import hmac
import json
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


SERVER_KEY = settings.PAYTABS.get("PAYTABS_AUTH", "")


def hmac_validate(signature, payload):
    payload_str = json.dumps(payload, separators=(",", ":"))
    calc_signature = hmac.new(SERVER_KEY.encode("utf-8"), payload_str.encode("utf-8"), hashlib.sha256).hexdigest()

    if hmac.compare_digest(signature, calc_signature):
        logger.debug("Hmac validated successfully")
        return True
    else:
        logger.critical("Hmac validation failed")
        logger.critical(f"Payload: {payload}")
        logger.critical(f"signature: {signature}")
        return False
