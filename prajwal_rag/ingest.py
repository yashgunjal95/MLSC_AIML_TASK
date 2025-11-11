# ingest.py
import os
import argparse
import pickle
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from utils import load_pdf_text, load_url_text, chunk_text, embed_texts

def main(args):
    data_folder = Path(args.data_folder)
    model_name = args.model
    chunk_size = args.chunk_size
    overlap = args.chunk_overlap
    out_folder = Path("vectorstore")
    out_folder.mkdir(exist_ok=True)

    print("Loading embedding model:", model_name)
    model = SentenceTransformer(model_name)

    docs = []   # list of texts (chunks)
    metadatas = []  # for each chunk store origin info

    # Process PDFs in folder
    for pdf in data_folder.glob("*.pdf"):
        print("Processing PDF:", pdf)
        text = load_pdf_text(str(pdf))
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        for i, c in enumerate(chunks):
            docs.append(c)
            metadatas.append({"source": str(pdf.name), "page_chunk": i})

    # Process .html files optionally
    for html in data_folder.glob("*.html"):
        print("Processing HTML:", html)
        text = html.read_text(encoding="utf-8")
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        for i, c in enumerate(chunks):
            docs.append(c)
            metadatas.append({"source": str(html.name), "chunk": i})

    # Optionally: single URL ingestion
    if args.url:
        print("Processing URL:", args.url)
        url_text = load_url_text(args.url)
        chunks = chunk_text(url_text, chunk_size=chunk_size, overlap=overlap)
        for i, c in enumerate(chunks):
            docs.append(c)
            metadatas.append({"source": args.url, "chunk": i})

    if len(docs) == 0:
        print("No documents found in", data_folder)
        return

    print("Embedding", len(docs), "chunks ...")
    embeddings = embed_texts(model, docs).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product -> cosine if normalized
    # normalize to unit length for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    # save index + metadata + docs
    faiss.write_index(index, str(out_folder / "index.faiss"))
    with open(out_folder / "metadatas.pkl", "wb") as f:
        pickle.dump(metadatas, f)
    with open(out_folder / "docs.pkl", "wb") as f:
        pickle.dump(docs, f)

    print("Saved vectorstore to", out_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_folder", default="data", help="folder with PDFs or html")
    parser.add_argument("--model", default="all-MiniLM-L6-v2")
    parser.add_argument("--chunk_size", type=int, default=800)
    parser.add_argument("--chunk_overlap", type=int, default=150)
    parser.add_argument("--url", default=None, help="optional single url to ingest")
    args = parser.parse_args()
    main(args)
