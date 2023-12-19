FROM python:3.12

RUN apt-get install wget
RUN pip install pandas psycopg2 sqlalchemy pyarrow fastparquet 

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python","ingest_data.py"]