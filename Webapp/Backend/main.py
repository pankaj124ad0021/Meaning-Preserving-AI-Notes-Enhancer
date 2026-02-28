from fastapi import FastAPI,Query,HTTPException
from langchain import final_runnable
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def base():
    return {"response":"You have reached Meaning-Preserving-AI-Notes-Enhancer Navigate to /enhance to enhance your text or to /docs to see the documentation"}

@app.get("/enhance")
def enhance_text(original_text:str=Query(...,description="Enter your text here")):
    try:
        res=final_runnable.invoke({"prompt":original_text})
        return res
    except Exception as E:
        print("AN ERROR OCCURED in enhance text function")
        print(E)
        raise HTTPException(status_code=400)
        
if __name__=="__main__":
    uvicorn.run(app,port=8000,host="0.0.0.0")