import os
from dotenv import load_dotenv

# This command loads the variables from your .env file into the environment
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DB_CONNECTION_STRING = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

# knowledge paths
KNOWLEDGE_BASE_PATH = "/project/app/knowledge_base" ## do not ever do that in production, absolute path is brittle
KRB_KB_PATH = os.path.join(KNOWLEDGE_BASE_PATH, "КРБ/База знаний")
MMB_KB_PATH = os.path.join(KNOWLEDGE_BASE_PATH, "ММБ/База знаний")
KRB_COLLECTION_NAME = "kbr_knowledge"
MMB_COLLECTION_NAME = "mmb_knowledge"