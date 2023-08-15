import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import os
import json
import redis
import random
import requests
import time

from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: str = os.getenv("REDIS_PORT")
REDIS_INPUT_LIST_NAME: str = os.getenv("REDIS_INPUT_LIST_NAME")
STAC_FASTAPI_READ_HOST: str = os.getenv("STAC_FASTAPI_READ_HOST")
STAC_FASTAPI_WRITE_HOST: str = os.getenv("STAC_FASTAPI_WRITE_HOST")
NUM_RETRIES: int = int(os.getenv("NUM_RETRIES", 5))


def random_step_time(min_time=5000, max_time=10000, step_size=200):
    return random.choice(range(min_time, max_time + 1, step_size))


def update_operation(url, payload):
    logging.info(f"Updating {url}")
    random_timeout = random_step_time(min_time=100, max_time=1000, step_size=100)
    logging.info(f"Waiting {random_timeout} milliseconds before updating {url}")
    time.sleep(random_timeout / 1000)
    logging.info(f"Timeout done. Updating {url}")
    response = requests.put(url, data=json.dumps(payload),
                            headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        logging.info(f"{url} updated")
    else:
        logging.error(f"{url} could not be updated")
        logging.error(f"Response: {response.text}, status code: {response.status_code}")
        raise Exception(f"{url} could not be updated")

    return response


def create_operation(url, payload):
    logging.info(f"Creating {url}")
    random_timeout = random_step_time(min_time=100, max_time=1000, step_size=100)
    logging.info(f"Waiting {random_timeout} milliseconds before creating {url}")
    time.sleep(random_timeout / 1000)
    logging.info(f"Timeout done. Creating {url}")
    response = requests.post(url, data=json.dumps(payload),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        logging.info(f"{url} created")
    else:
        logging.error(f"{url} could not be created")
        logging.error(f"Response: {response.text}, status code: {response.status_code}")
        raise Exception(f"{url} could not be created")

    return response


if __name__ == "__main__":
    redis_client = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT)
    if redis_client.ping():
        logging.info("Connected to Redis")
    else:
        logging.error("Could not connect to Redis")
        exit(1)
    while True:
        item = redis_client.blpop(REDIS_INPUT_LIST_NAME, timeout=1)
        if item:
            _, item_payload = item
            logging.info("Timing start")
            body = json.loads(item_payload)
            collection = body.get("collection")
            stac_payload = body.get("stac")
            stac_item_id = stac_payload.get("id")

            item_url_on_read_server = urljoin(STAC_FASTAPI_READ_HOST,
                                              f"/collections/{collection}/items/{stac_item_id}")
            logging.info(f"Checking if {item_url_on_read_server} exists")
            response = requests.get(item_url_on_read_server)
            if response.status_code == 200:
                logging.info(f"{item_url_on_read_server} exists, will update")
                item_url_on_write_server_with_id = urljoin(STAC_FASTAPI_WRITE_HOST,
                                                           f"/collections/{collection}/items/{stac_item_id}")
                for i in range(1, NUM_RETRIES + 1):
                    try:
                        response = update_operation(item_url_on_write_server_with_id, stac_payload)
                        logging.info(f"Updated {item_url_on_write_server_with_id} on the try number {i}")
                        break
                    except Exception as e:
                        logging.error(f"Error updating {item_url_on_write_server_with_id}: {e}")
                        if i == NUM_RETRIES:
                            raise e
                        else:
                            time_for_next_retry_ms = random_step_time(5000, max_time=10000 * i, step_size=200 * i)
                            logging.info(
                                f"Retrying update of {item_url_on_write_server_with_id} in {time_for_next_retry_ms} milliseconds")
                            time.sleep(time_for_next_retry_ms / 1000)

            elif response.status_code == 404:
                logging.info(f"{item_url_on_read_server} does not exist, will create")
                item_url_on_write_server = urljoin(STAC_FASTAPI_WRITE_HOST, f"/collections/{collection}/items")
                for i in range(1, NUM_RETRIES + 1):
                    try:
                        response = create_operation(item_url_on_write_server, stac_payload)
                        logging.info(f"Created {item_url_on_write_server} on the try number {i}")
                        break
                    except Exception as e:
                        logging.error(f"Error creating {item_url_on_write_server}: {e}")
                        if i == NUM_RETRIES:
                            raise e
                        else:
                            time_for_next_retry_ms = random_step_time(5000, max_time=10000 * i, step_size=200 * i)
                            logging.info(
                                f"Retrying create of {item_url_on_write_server} in {time_for_next_retry_ms} milliseconds")
                            time.sleep(time_for_next_retry_ms / 1000)
            else:
                logging.error(f"Error checking if {item_url_on_read_server} exists")
                raise Exception(f"Error checking if {item_url_on_read_server} exists, status code {response.status_code}")
            logging.info("Timing end")
