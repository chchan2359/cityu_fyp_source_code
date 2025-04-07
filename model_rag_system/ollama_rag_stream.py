# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Testing - LLM Streaming Reply

import requests
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import os
import sys

# Vector DB - Initialization & Save
def initialize_and_save_vector_db(json_dir="!!PATH-TO-JSON-DIR!!", 
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
def setup_vector_db(json_dir="E:/FYP/dataset/recommendtation_files", 
                    index_file="plant_index.faiss", 
                    metadata_file="plant_metadata.json"):
    if os.path.exists(index_file) and os.path.exists(metadata_file):
        return load_vector_db(index_file, metadata_file)
    else:
        return initialize_and_save_vector_db(json_dir, index_file, metadata_file)

# Load keywords with aliases
def load_keywords(keyword_file="keywords.json"):
    # Open and read the keyword file
    with open(keyword_file, 'r', encoding='utf-8') as f:
        data = json.load(f)["keywords"]
    
    keyword_to_main = {}  # Mapping from aliases to main keyword
    main_keywords = set()  # Set of main keywords
    main_to_first_alias = {}  # Mapping from main keyword to first alias
    for main_kw, aliases in data.items():
        main_keywords.add(main_kw)
        main_to_first_alias[main_kw] = aliases[0].lower()  # First alias as default
        for alias in aliases:
            keyword_to_main[alias.lower()] = main_kw  # Convert to lowercase for consistency
    
    return keyword_to_main, main_keywords, main_to_first_alias

# Replace aliases with the first alias (default naming)
def replace_keywords_in_question(question, keyword_to_main, main_to_first_alias):
    question_lower = question.lower()
    for alias, main_kw in keyword_to_main.items():
        if alias in question_lower and alias != main_to_first_alias[main_kw]:  # Avoid replacing if alias is already the first alias
            question_lower = question_lower.replace(alias, main_to_first_alias[main_kw])
    return question_lower

# RAG - Retrieve documents from Vector DB
def retrieve_documents(question, model, index, documents, doc_metadata, keyword_to_main, main_keywords, top_k=5, max_tokens=512):
    # Split the question into words (already transformed in main)
    question_words = set(question.lower().split())
    
    # Check if the question contains any main keywords
    matched_main_kws = set()
    for word in question_words:
        if word in main_keywords:
            matched_main_kws.add(word)
    has_plant_name = bool(matched_main_kws)  # Does the question contain plant-related terms?
    
    # Vector search: Use the provided question for embedding
    question_embedding = model.encode([question])[0]
    distances, indices = index.search(np.array([question_embedding], dtype=np.float32), top_k * 5)  # Fetch more candidates
    
    # Rank documents based on whether the question contains plant names
    scored_docs = []
    for idx, distance in zip(indices[0], distances[0]):
        doc = doc_metadata[idx]
        doc_id = doc.get("id", "").lower()
        # Check if document ID contains any of the matched main keywords from the question
        doc_matches_question = any(main_kw in doc_id for main_kw in matched_main_kws) if has_plant_name else False
        # Check if document ID contains any main keyword (for general plant detection)
        doc_has_plant = any(main_kw in doc_id for main_kw in main_keywords)
        
        # Simple scoring logic
        vector_score = 1 / (1 + distance)  # Vector similarity score
        if has_plant_name and doc_has_plant:
            # If question contains plant name and document contains a plant name
            if doc_matches_question:
                total_score = vector_score + 1.0  # Exact match with question's mapped keyword, add full bonus
            else:
                total_score = vector_score + 0.5  # Document has a plant name but not the exact match, add smaller bonus
        elif not has_plant_name and not doc_has_plant:
            total_score = vector_score + 1.0  # Question and document both lack plant names, add bonus
        else:
            total_score = vector_score  # No bonus for mismatch
        
        scored_docs.append((total_score, doc))
    
    # Sort by score and filter
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

# Ollama API with streaming support
def query_ollama(question, retrieved_docs):
    context = "\n\n".join([doc["content"] for doc in retrieved_docs])
    prompt = f"Based on the following information:\n{context}\n\nAnswer the question: {question}"
    
    data = {
        "model": "qwen2.5:7b-instruct-8k",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # Enable streaming
    }
    url = "http://localhost:11434/api/chat"
    
    try:
        # Send request with streaming enabled
        response = requests.post(url, json=data, stream=True, timeout=20)
        response.raise_for_status()
        
        full_answer = ""
        print("Answer: ", end="", flush=True)  # Print "Answer: " prefix immediately
        
        # Process the streaming response line by line
        for line in response.iter_lines():
            if line:  # Ignore empty lines
                chunk = json.loads(line.decode('utf-8'))
                content = chunk.get("message", {}).get("content", "")
                if content:
                    full_answer += content
                    print(content, end="", flush=True)  # Print each chunk immediately
        print()  # Newline after streaming completes
        return full_answer
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error querying Ollama API: {e}"
        print(error_msg, flush=True)
        return error_msg

if __name__ == "__main__":
    json_dir = "E:/FYP/dataset/recommendtation_files"
    index_file = "plant_index.faiss"
    metadata_file = "plant_metadata.json"
    keyword_file = "keywords.json"
    
    # Set up the vector database
    print("Setting up vector database...", flush=True)
    model, index, documents, doc_metadata = setup_vector_db(json_dir, index_file, metadata_file)
    
    # Load keywords and aliases
    keyword_to_main, main_keywords, main_to_first_alias = load_keywords(keyword_file)
    
    number_of_questions = 1000
    question_number = 0
    
    print("\nWelcome to the Houseplant RAG System!", flush=True)
    
    while question_number < number_of_questions:
        question = input("Question: ")
        sys.stdout.flush()  # Flush input prompt
        
        # Replace aliases with the first alias before retrieval
        modified_question = replace_keywords_in_question(question, keyword_to_main, main_to_first_alias)
        print(f"Modified Question: {modified_question}", flush=True)
        
        # Retrieve relevant documents using the modified question
        retrieved_docs = retrieve_documents(modified_question, model, index, documents, doc_metadata, keyword_to_main, main_keywords, top_k=5, max_tokens=512)
        if not retrieved_docs:
            print("No relevant information found in the database.", flush=True)
            question_number += 1
            continue
        
        # Display retrieved documents immediately
        print("Retrieved Documents:", flush=True)
        for doc in retrieved_docs:
            doc_name = doc.get("id", "Unnamed Document")
            print(f"- {doc_name}", flush=True)
        
        # Query Ollama with streaming and display answer
        ai_reply = query_ollama(modified_question, retrieved_docs)
        print()  # Extra newline after streaming answer
        
        question_number += 1
    
    print("Thank you for using the Houseplant RAG System!", flush=True)