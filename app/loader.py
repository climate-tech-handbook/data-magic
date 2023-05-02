import openai
import os
from dotenv import load_dotenv
import csv
import yaml
import requests

load_dotenv()

unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")

api_key = os.getenv("OPENAI_SECRET_KEY")
openai.api_key = api_key
