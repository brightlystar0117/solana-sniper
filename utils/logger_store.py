import logging, os
from utils.webhook import sendWebhook


log_file = os.path.join('data', f"logs.txt")
logging.basicConfig(level=logging.INFO, filename=log_file, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',datefmt='%d-%b-%y %I:%M:%S %p')

def print_message(text,alert_type):
    logging.info(text)
    sendWebhook(alert_type,text)
