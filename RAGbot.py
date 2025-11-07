import os
import torch
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from gtts import gTTS
import pygame
import time

#update your doc name and other configs here

CONFIG = {
    "PDF_PATH": "./pdfs/[YOUR_DOC_NAME].pdf",  
    "DB_PATH": "./chroma_db",
    "COLLECTION": "pdf_chunks",
    "MODEL_NAME": "google/flan-t5-small",
    "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2",
    "CHUNK_SIZE": 800,
    "CHUNK_OVERLAP": 150,
    "MAX_NEW_TOKENS": 150,
    "TEMPERATURE": 0.7
}

class RAGBot:
    def __init__(self):
        self.collection = None
        self.llm = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def initialize(self):
        print("Initializing...")
        
        try:
            self.collection = self.setup_vector_store()
            
            if not os.path.exists(CONFIG["PDF_PATH"]):
                print(f"Error: PDF file not found: {CONFIG['PDF_PATH']}")
                return False
            
            docs, metas = self.extract_and_chunk_pdfs(CONFIG["PDF_PATH"])
            
            if not docs:
                print("Error: No text could be extracted from the PDF")
                return False
                
            ids = [str(i) for i in range(len(docs))]
            self.collection.add(
                documents=docs, 
                metadatas=metas, 
                ids=ids
            )
            print("PDF processed and stored in database.")
            
            print("Loading language model...")
            self.llm = self.load_llm_pipeline()
            if self.llm is None:
                print("Error: Failed to load LLM")
                return False
            
            pygame.mixer.init()
            
            print("Initialization complete.")
            return True
            
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
    
    def setup_vector_store(self):
        emb_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            CONFIG["EMBEDDING_MODEL"]
        )
        
        client = chromadb.PersistentClient(path=CONFIG["DB_PATH"])
        
        try:
            client.delete_collection(CONFIG["COLLECTION"])
            print("Cleared old database.")
        except:
            pass
            
        collection = client.create_collection(
            name=CONFIG["COLLECTION"], 
            embedding_function=emb_func
        )
        
        return collection
    
    def extract_and_chunk_pdfs(self, pdf_path: str):
        docs, metas = [], []
        
        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            print(f"Processing {total_pages} pages...")
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    chunks = self.chunk_text(text, CONFIG["CHUNK_SIZE"], CONFIG["CHUNK_OVERLAP"])
                    for chunk in chunks:
                        docs.append(chunk)
                        metas.append({"page": i + 1, "chunk_id": len(docs)})
                        
            print(f"Extracted {len(docs)} chunks from {len(reader.pages)} pages")
            return docs, metas
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return [], []
    
    def chunk_text(self, text: str, size: int = 800, overlap: int = 150):
        words = text.split()
        chunks = []
        i = 0
        
        while i < len(words):
            chunk = " ".join(words[i:i + size])
            chunks.append(chunk)
            i += size - overlap
            
        return chunks
    
    def load_llm_pipeline(self):
        try:
            model_name = CONFIG["MODEL_NAME"]
            
            pipeline_obj = pipeline(
                "text2text-generation",
                model=model_name,
                tokenizer=model_name,
                dtype=torch.float32,
                device_map=self.device
            )
            
            print(f"Model loaded on {self.device}")
            return pipeline_obj
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def retrieve(self, query: str, n_results: int = 3):
        try:
            results = self.collection.query(
                query_texts=[query], 
                n_results=n_results, 
                include=["documents", "metadatas"]
            )
            context = "\n\n".join(results["documents"][0])
            return context, results["metadatas"][0]
        except Exception as e:
            print(f"Retrieval error: {e}")
            return "", []
    
    def ask(self, query: str):
        if not query.strip():
            return "Please provide a question.", []
            
        context, metadata = self.retrieve(query)
        
        if not context:
            return "I couldn't find relevant information in the documents.", []
        
        prompt = f"""Answer the following question based only on this context:

Context:
{context}

Question:
{query}

Answer:"""
        
        try:
            response = self.llm(
                prompt,
                max_new_tokens=CONFIG["MAX_NEW_TOKENS"],
                temperature=CONFIG["TEMPERATURE"],
                do_sample=True,
                num_return_sequences=1
            )[0]["generated_text"]
            
            return response.strip(), metadata
            
        except Exception as e:
            print(f"Generation error: {e}")
            return "Sorry, I encountered an error while generating a response.", metadata
    
    def speak(self, text: str):
        if not text.strip():
            return
            
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            audio_file = "temp_audio.mp3"
            tts.save(audio_file)
            
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            os.remove(audio_file)
                
        except Exception as e:
            print(f"TTS error: {e}")

def main():
    bot = RAGBot()
    
    if not bot.initialize():
        print("Failed to initialize RAGBot. Exiting.")
        return
    
    print("\n" + "="*60)
    print("🤖 RAGBot Ready! Type 'exit' to quit.")
    print("="*60)
    
    while True:
        try:
            user_text = input("\n💬 Enter your question: ").strip()
            
            if user_text.lower() == 'exit':
                print("👋 Goodbye!")
                break
                
            if not user_text:
                continue
            
            print("Thinking...")
            answer, sources = bot.ask(user_text)
            
            print(f"\nBot: {answer}")
            if sources:
                pages = sorted(list(set([meta['page'] for meta in sources])))
                print(f"Sources: Pages -> {pages}")
            
            print("🔊 Playing audio response...")
            bot.speak(answer)
            
        except KeyboardInterrupt:
            print("\n⏹️ Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            continue

if __name__ == "__main__":
    main()