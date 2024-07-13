FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# copy over the vectors if available
COPY ./vector[s] /code/vectors

COPY ./documents /code/documents
COPY ./.env /code/.env
COPY ./main.py /code/main.py
COPY ./rag.py /code/rag.py


ENV OPENAI_API_KEY=""
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# generate vectors if not available
RUN python rag.py

CMD ["fastapi", "run", "main.py", "--port", "8000"]

EXPOSE 8000