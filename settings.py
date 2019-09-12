import os
from dotenv import load_dotenv,find_dotenv
from utils import logger
# load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
load_dotenv(find_dotenv())

# Create or get the logger
LOGGER=logger()

HOST=os.environ["MONGODB_HOST"]
PORT=os.environ["MONGODB_PORT"]
DATABASE=os.environ["MONGODB_DATABASE"]
USER=os.environ["MONGODB_USER_NAME"] if 'MONGODB_USER_NAME' in os.environ else None
PWD=os.environ["MONGODB_PASSWORD"] if 'MONGODB_PASSWORD' in os.environ else None