# loads environment variables from a .env file
import os
from dotenv import load_dotenv

load_dotenv()

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
CareerCritter_LLM_KEY = os.getenv("CareerCritter_LLM_KEY")