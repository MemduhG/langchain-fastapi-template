from pydantic import BaseModel

from fastapi import FastAPI
from rag import get_retrieval_chain

chain = get_retrieval_chain()
app = FastAPI()


class Query(BaseModel):
    input: str
    detailed: bool  # If True, return whole output rather than just the answer


@app.post("/question")
def answer_question(query: Query):
    output = chain.invoke({"input": query.input})
    if query.detailed:
        return output
    else:
        return output["answer"]
