# utils.py
import os
import re
from typing import List
import pdfplumber
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_pdf_text(path: str) -> str:
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                texts.append(txt)
    return "\n".join(texts)

def load_url_text(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    # grab main text
    text = soup.get_text(separator="\n")
    # simple cleanup
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text

def chunk_text(text: str, chunk_size: int=800, overlap: int=150) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def embed_texts(model: SentenceTransformer, texts: List[str]) -> np.ndarray:
    return model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
