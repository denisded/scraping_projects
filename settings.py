import os
from dotenv import load_dotenv

load_dotenv('.env')

MY_PASS = os.environ.get("MY_PASS")

print(MY_PASS)