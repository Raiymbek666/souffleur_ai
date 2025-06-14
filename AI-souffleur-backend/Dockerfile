FROM python:3.11-slim-bullseye
WORKDIR /project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader punkt

COPY ./app/ /project/app
COPY ./entrypoint.sh /project/entrypoint.sh
RUN chmod +x /project/entrypoint.sh

EXPOSE 8000