# langchain-fastapi-template
This is a simple RAG API built with FastAPI and LangChain.

## Quick Demo
The docker image is currently running on Railway and the url can be used for 
queries like so:
```bash
curl -X POST https://langchain-fastapi-template-production.up.railway.app/question -H "Content-Type: application/json" -d '{"input": "Why not trade with Sweden?", "detailed": false}'
```



## Run Locally

### 1. Set the API Key
The `.env` file has a single environment variable to set,
currently defined as `OPENAI_API_KEY=xxxx`. 
Please change the `xxxx` value to your own OpenAI API key.
### 2. Install the python requirements
```bash
pip install -r requirements.txt
```

### 3. Generate the Vector Store
The vector database is already provided as part of this repo,
but if the user prefers, it will be enough to run the command below to generate the vector
database.
```bash
python rag.py --repopulate
```
The directories for the documents and where the vector database
will be saved can be specified, but the API currently assumes
they are in their default locations.

### 4. Run and Query the API
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

This query along with two more can be found in the `sample.sh` 
file. 
Running this file should produce outputs like the following
```
$ bash sample.sh 
"Sweden is not included in the list of countries where sales are not conducted due to ethical and environmental concerns. Some of the products do not meet Sweden's high environmental standards, and there are concerns raised about the ethical sourcing of materials used in the products. Until full compliance with Sweden's ethical and environmental standards can be ensured, sales will not be conducted in this market."
"You should contact the Compliance Department for information about sales restrictions."
"Spain, Italy, Germany, and Sweden are on the company's no sale list."%    
```

## Docker
**Note: The OpenAI API key still needs to be set before using Docker.**


The provided dockerfile will create an image that will include
vectors if generated, and generate them if not. Simply
build the image with the following command.
```bash
docker build . -t rag 
```

Run the image once it's built with the following, please do not
omit the port option as it is necessary to send requests to the
container.
```bash
docker run -p 8000:8000 rag
```

After building and running, sending requests as shown above will return 
the desired results.

