# Meaning Preserving AI-Notes Enhancer By Team FIXIT

Problem Statement No 3

### We have created an AI writing assistant that- 
• Accepts raw, unpolished text as input.
• Improves grammar, spelling, clarity, and sentence structure.
• Preserves the original meaning, without exception.
• Provides a quantitative similarity score to validate meaning preservation.

### Model Used
Llama-4 - for enhancing text
Sentence-transformers/all-MiniLM - for embedding generation

## How It Works
- User enter the raw text in our webapp
- Webapp send raw text to backend
- In backend we send raw text to LLama-4 with system instruction and few shot prompting to generate the enhanced text
- Generate embeddings of enhanced text and original text parallely 
- Calculate similarity score using cosine similarity between enhanced text and original text
- Backend return the Enhanced text and similarity score
- Frontend display the enchanced text and similarity score to user

## Tech Used - 
LangChain - for models
FastApi - for api
Streamlit - for Frontend
Docker - for contanirasation


## Setup Instructions
Step 1 - Clone the Repo
```
git clone https://github.com/pankaj-2708/Neural-Style-Transfer.git
```

Step 2 - Create and activate a virtual enviorment
```
python -m venv gdg
gdg\Scripts\Activate
```

Step 3 - Install Backend Dependencies
```
cd ./Webapp/Backend
pip install -r requirements.txt
```

Step - 4 Start the Backend 
```
python run main.py
```

Step 5 - Install Frontend Dependencies
```
cd ../Frontend
pip install -r requirements.txt
```

Step 6 - Start Frontend
```
streamlit run app.py
```
App is running you can acces it at http://localhost:8501/