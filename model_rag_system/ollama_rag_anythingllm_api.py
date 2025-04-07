# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Testing - API Calling (AnythingLLM API)

import requests
import json

def ask_anythingllm(question, workspace_name, api_key):
    url = f"http://localhost:3001/api/v1/workspace/{workspace_name}/chat"    
    headers = {        
        "Authorization": f"Bearer {api_key}",        
        "Content-Type": "application/json",        
        "accept": "application/json"    
    }    
    data = {        
        "message": question,        
        "mode": "query"
    }    
    
    response = requests.post(url, headers=headers, json=data)    
    if response.status_code == 200:        
        result = response.json()                
        answer = result['textResponse'].strip()        
        sources = result.get('sources', [])        
        return answer, sources    
    else:        
        return f'Error: {response.text}', []
    
api_key = "PYP3JNK-GVFMRR4-JHQAC42-GM9QN4W"
workspace = "plant"
question = "List 5 common pests"
answer, sources = ask_anythingllm(question, workspace, api_key)
print("REPLY:", answer)
print("SORUCES:", [src['title'] for src in sources])