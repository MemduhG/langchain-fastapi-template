# langchain-fastapi-template
This is a simple RAG API built with FastAPI and LangChain.


## Generating the Vector Store

## Running and Querying the API
Run the API with 
```bash
fastapi run main.py
```

If we wanted to find out which countries the company can't sell to, we could 
query the API this way:
```bash
$ curl -X POST localhost:8000/question -H "Content-Type: application/json" -d '{"input": "Which countries are on our no sale list?", "detailed": false}'
```
This should give you something like the following output.
```
"Spain, Italy, Germany, and Sweden are on the no sale list."%       
```
Set the field `detailed` to `true` instead of `false` to get more 
information like the document retrieved. Since we are only working with one
document, this is probably not so important in our case.
