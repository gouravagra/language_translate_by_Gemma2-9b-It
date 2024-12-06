from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Create ChatGroq model
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Define input model for the API
class TranslationInput(BaseModel):
    language: str
    text: str

# Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Define output parser
parser = StrOutputParser()

# Create chain
chain = prompt_template | model | parser

# Define FastAPI app
app = FastAPI(
    title="Langchain Server",
    description="A simple API server using Langchain runnable interfaces"
)

from fastapi import Request

@app.post("/chain")
async def translate(input: TranslationInput, request: Request):
    raw_body = await request.json()  # Log the raw JSON body received
    print(f"Raw request body: {raw_body}")
    try:
        print(f"Received payload: {input}")
        result = chain.invoke({
            "language": input.language,
            "text": input.text
        })
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
