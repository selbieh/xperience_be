import requests
import logging
from json.decoder import JSONDecodeError
from rest_framework import status
import logging


logger = logging.getLogger(__name__)


# handle logging here
def handle_request(method="POST", url="", payload={}, headers={}, tag="Sending Request"):
    try:
        logger.debug(f"[{tag}]: Method:[{method}]\n url:[{url}]\n payload:{payload}\n headers:{headers}")
        response = requests.request(method=method, url=url, json=payload, headers=headers)
        json_resposne = response.json()
        logger.debug(f"[StatusCode]: {response.status_code}")
        logger.debug(f"[Resposne]: {json_resposne}")
        if response.status_code != status.HTTP_200_OK:
            return False, response.text
    except requests.exceptions.Timeout:
        logger.debug(f"[Resposne]: Timed Out")
        return False, "Gateway Timed out"
    except JSONDecodeError as e:
        logger.debug(f"[Resposne]: {response.text}")
        return False, "gateway response not json"
    return True, response
