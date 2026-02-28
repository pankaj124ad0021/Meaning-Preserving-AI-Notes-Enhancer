from langchain_huggingface import (
    HuggingFaceEmbeddings,
    ChatHuggingFace,
    HuggingFaceEndpoint,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
import numpy as np
from dotenv import load_dotenv

# loading enviorment variables
load_dotenv()

# loading models
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-4-Scout-17B-16E-Instruct", task="text-generation"
)
enhancer_model = ChatHuggingFace(llm=llm)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Creating Prompt Template
chat_template = ChatPromptTemplate(
    [
        (
            "system",
            """You are a precise writing enhancement assistant. Your ONLY job is to improve the expression of text — not its ideas.
You MUST:
- Correct grammatical errors and spelling mistakes.
- Improve sentence structure for clarity and readability.
- Improve logical flow between sentences where necessary.
- Preserve the original meaning completely.

You MUST NOT:
- Add new ideas, arguments, or information not present in the original text.
- Remove any core meaning or factual claim from the original.
- Change the factual intent of any sentence .
- Expand content beyond style and grammatical improvement.
- Add preambles like "Here is the improved text" — return ONLY the enhanced text.
- Ask any further questions to user just enhance the text and return it.
- Produce output that a reasonable reader would interpret differently from the original.""",
        ),
        (
            "human",
            """Below is a example of how to enhance text:
         
Input: I am doing project on AI which is very good and it help many people in future.
Output: I am working on an AI project that has strong potential to help many people in the future.

Now enchance the following text

Input: {prompt}
Output:""",
        ),
    ]
)

# String output parser
parser = StrOutputParser()


# Cosine Similarity Function
def cosine_similarity(arr1, arr2):
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    num = (arr1 * arr2).sum()
    den = np.sqrt((arr1**2).sum()) * np.sqrt((arr2**2).sum())
    return num / den


# utility function
def generate_embedding(embedding_model, text):
    embedding = embedding_model.embed_query(text)
    return embedding


# Runnables
generator_runnable = RunnableParallel(
    {
        "enhanced_text": chat_template | enhancer_model | parser,
        "original_text": RunnableLambda(lambda x: x["prompt"]),
    }
)

embedding_generator_runnable = RunnableParallel(
    {
        "enhanced_embedding": RunnableLambda(
            lambda x: generate_embedding(embedding_model, x["enhanced_text"])
        ),
        "original_embedding": RunnableLambda(
            lambda x: generate_embedding(embedding_model, x["original_text"])
        ),
        "enhanced_text": RunnableLambda(lambda x: x["enhanced_text"]),
    }
)

similarity_score_runnable = RunnableParallel(
    {
        "enhanced_text": RunnableLambda(lambda x: x["enhanced_text"]),
        "similarity_score": RunnableLambda(
            lambda x: cosine_similarity(
                x["enhanced_embedding"], x["original_embedding"]
            )
        ),
    }
)

final_runnable = (
    generator_runnable | embedding_generator_runnable | similarity_score_runnable
)
