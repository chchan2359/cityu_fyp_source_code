#   Main Set-up
    Python Version      - 3.10.16 (Anaconda Venv)
    React.js Version    - 11.x
    
    First, install all the required modules
        pip install -r requirements.txt

    Go to folder "main"
    run the python script
        - python api_rag_system.py          | PORT 5000
        - python api_object_detection.py    | PORT 5010
    
    Then, Go to folder "main\web"
    run the website in dev mode [React.js - Vanilla React with JavaScript]
        - npm install (IF first-time run OR node-modules folder is not exist)
        - npm run dev                       | PORT 5173

#   Ollama Setup
    1. Download the Ollama from Offical Website : https://ollama.com/
    2. Turn on the Ollama.exe / ollama serve in terminal
    3. Check the Ollama Connection : localhost:11434
    4. Download the Large-Language Models - Selected Model Qwen2.5-7B_Instruct-1M
        - ollama run yasserrmd/Qwen2.5-7B-Instruct-1M

#   Ollama Setup (Intel GPU)
    1. Visit the GitHub Repo : https://github.com/intel/ipex-llm
    2. Download the latest ollama-ipex-llm-VERSION-win.zip
    3. Extract the zip folder
    4. Go to the Extracted Folder
    5. Type start-ollama.bat in Terminal (CMD/PS/Else)
    6. Check the Ollama Connection : localhost:11434
    7. Download the Large-Language Models - Selected Model Qwen2.5-7B_Instruct-1M
        - ollama run yasserrmd/Qwen2.5-7B-Instruct-1M
    ** Download Higher / Lower LLM Models depend on hardware performance

#   Folder Description
    main                | Folder to run Indoor Plant Query Website
    data_collection     | Image Scrapping Script
    dataset             | Dataset for Object Detection, Recommendation System with different version
    model_rag_system    | Script to test Recommendation System
    model_yolo_model    | Zipped YOLO Models, and Script to test different YOLO Models
    tools               | Tools used for development
    z_document_plantid  | Images used in the Report, PlantId website result
    z_document_prototype| Images used in the Report, Prototype of Indoor Plant Query