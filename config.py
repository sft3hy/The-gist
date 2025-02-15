from datetime import datetime
import os

AZURE_API_KEY=os.environ.get("GH_ACCESS_TOKEN", None)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", None)

AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

CHUNK_SIZE = 18000


GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.3-70b-specdec",
    "llama-3.1-70b-versatile",
    "llama3-70b-8192",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
    "llama-3.1-8b-instant"
]

GOOGLE_MODELS = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini"
]


# ALL_MODELS = OPENAI_MODELS + GOOGLE_MODELS + GROQ_MODELS
ALL_MODELS=["llama-3.1-8b-instant", "llama3-8b-8192", "gemma2-9b-it"]

DOC_SUMMARY_SYS_PROMPT = """You are a document summarizer. You will be given a textual representation of a document (PDF, TXT, or PPTX), and you will output a detailed and structured summary of the document."""

def get_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')