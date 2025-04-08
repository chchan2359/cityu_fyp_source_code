# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Main - API Hosting (RAG System)

import requests
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import os
import time
from flask import Flask, Response, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Vector DB - Initialization & Save
def initialize_and_save_vector_db(json_dir="./recommendtation_system_dataset_json", 
                                 index_file="plant_index.faiss", 
                                 metadata_file="plant_metadata.json"):
    print("Generating new vector database...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    documents = []
    doc_metadata = []
    
    json_files = Path(json_dir).glob("*.json")
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    documents.append(item["content"])
                    doc_metadata.append(item)
            else:
                documents.append(data["content"])
                doc_metadata.append(data)
    
    embeddings = model.encode(documents, show_progress_bar=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    
    faiss.write_index(index, index_file)
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({"documents": documents, "doc_metadata": doc_metadata}, f, ensure_ascii=False)
    
    print(f"Vector database initialized and saved to '{index_file}' and '{metadata_file}'.")
    return model, index, documents, doc_metadata

# Vector DB - Load Existing .faiss and metadata
def load_vector_db(index_file="plant_index.faiss", metadata_file="plant_metadata.json"):
    print("Loading existing vector database...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"FAISS index file '{index_file}' not found.")
    index = faiss.read_index(index_file)
    
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"Metadata file '{metadata_file}' not found.")
    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        documents = data["documents"]
        doc_metadata = data["doc_metadata"]
    
    print(f"Vector database loaded with {index.ntotal} documents.")
    return model, index, documents, doc_metadata

# Vector DB - Set up for System
def setup_vector_db(json_dir="./recommendtation_system_dataset_json", 
                    index_file="plant_index.faiss", 
                    metadata_file="plant_metadata.json"):
    if os.path.exists(index_file) and os.path.exists(metadata_file):
        return load_vector_db(index_file, metadata_file)
    else:
        return initialize_and_save_vector_db(json_dir, index_file, metadata_file)

# Load keywords with aliases
def load_keywords(keyword_file="./keywords.json"):
    with open(keyword_file, 'r', encoding='utf-8') as f:
        data = json.load(f)["keywords"]
    
    keyword_to_main = {}
    main_keywords = set()
    main_to_first_alias = {}
    for main_kw, aliases in data.items():
        main_keywords.add(main_kw)
        main_to_first_alias[main_kw] = aliases[0].lower()
        for alias in aliases:
            keyword_to_main[alias.lower()] = main_kw
    
    return keyword_to_main, main_keywords, main_to_first_alias

# Replace aliases with the main keyword (key)
def replace_keywords_in_question(question, keyword_to_main, main_to_first_alias):
    question_lower = question.lower()
    # keyword_to_main is already a mapping from alias to key from load_keywords()
    for alias, key in keyword_to_main.items():
        if alias in question_lower:
            question_lower = question_lower.replace(alias, key)
    return question_lower

# RAG - Retrieve documents from Vector DB
def retrieve_documents(question, model, index, documents, doc_metadata, keyword_to_main, main_keywords, top_k=5, max_tokens=512):
    question_words = set(question.lower().split())
    matched_main_kws = set(word for word in question_words if word in main_keywords)
    has_plant_name = bool(matched_main_kws)
    
    question_embedding = model.encode([question])[0]
    distances, indices = index.search(np.array([question_embedding], dtype=np.float32), top_k * 5)
    
    scored_docs = []
    for idx, distance in zip(indices[0], distances[0]):
        doc = doc_metadata[idx]
        doc_id = doc.get("id", "").lower()
        doc_matches_question = any(main_kw in doc_id for main_kw in matched_main_kws) if has_plant_name else False
        doc_has_plant = any(main_kw in doc_id for main_kw in main_keywords)
        
        # Keyword Filtering
        vector_score = 1 / (1 + distance)
        if has_plant_name and doc_has_plant:
            total_score = vector_score + (1.0 if doc_matches_question else 0.5)
        elif not has_plant_name and not doc_has_plant:
            total_score = vector_score + 1.0
        else:
            total_score = vector_score
        
        scored_docs.append((total_score, doc))
    
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    selected_docs = []
    total_tokens = 0
    for score, doc in scored_docs[:top_k]:
        content = doc["content"]
        tokens = len(content.split())
        if total_tokens + tokens <= max_tokens:
            selected_docs.append(doc)
            total_tokens += tokens
        else:
            break
    
    return selected_docs

# Ollama API with non-streaming support
def query_ollama(question, retrieved_docs):
    context = "\n\n".join([doc["content"] for doc in retrieved_docs])
    prompt = f"Based on the following information:\n{context}\n\nAnswer the question: {question}"
    
    data = {
        "model": "yasserrmd/Qwen2.5-7B-Instruct-1M:latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False  # Non-streaming
    }
    url = "http://localhost:11434/api/chat"
    
    try:
        response = requests.post(url, json=data, timeout=20)
        response.raise_for_status()
        response_json = json.loads(response.text)
        return response_json["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error querying Ollama API: {e}"

# Initialize vector DB and load keywords once
print("Setting up vector database...")
model, index, documents, doc_metadata = setup_vector_db()
keyword_to_main, main_keywords, main_to_first_alias = load_keywords()

# API endpoint for staged response
@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    if not data or 'question' not in data:
        return Response("No question provided", status=400)
    
    question = data['question']
    
    def generate():
        # Step 1: Send Modified Question
        modified_question = replace_keywords_in_question(question, keyword_to_main, main_to_first_alias)
        yield f"data: {json.dumps({'modified_question': modified_question})}\n\n"
        time.sleep(1)

        # Step 2: Send Retrieved Documents
        retrieved_docs = retrieve_documents(modified_question, model, index, documents, doc_metadata, keyword_to_main, main_keywords, top_k=5, max_tokens=512)
        retrieved_doc_ids = [doc.get("id", "Unnamed Document") for doc in retrieved_docs] if retrieved_docs else []
        yield f"data: {json.dumps({'retrieved_docs': retrieved_doc_ids})}\n\n"
        time.sleep(1)

        # Step 3: Send LLM Reply
        answer = query_ollama(modified_question, retrieved_docs) if retrieved_docs else "No relevant information found in the database."
        yield f"data: {json.dumps({'ollama_answer': answer})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)