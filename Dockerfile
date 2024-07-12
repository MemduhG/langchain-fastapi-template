FROM python:3.12-slim

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
COPY ./vector[s] /code/vectors
COPY ./documents /code/documents
COPY ./.env /code/.env
COPY ./main.py /code/main.py
COPY ./rag.py /code/rag.py

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
CMD ["fastapi", "run", "main.py", "--port", "8000"]

EXPOSE 8000