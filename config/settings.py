from pathlib import Path
import os
from dotenv import load_dotenv

#Project roots
BASE_DIR = Path(__file__).resolve().parent.parent

#load environment
load_dotenv(BASE_DIR/ ".env")

#data directories
DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR/ "external"

#RAG directories
RAG_DIR = BASE_DIR / "rag"
DOCUMENTS_DIR = RAG_DIR / "documents"
EMBEDDINGS_DIR = RAG_DIR / "embeddings"
VECTORSTORE_DIR = RAG_DIR/ "vectorstore"

#application
APP_NAME = "InvestIQ"
VERSION = "0.1.0"

#ENVIRONMENT
ENVIRONMENT = os.getenv("ENVIRONMENT", "developement")