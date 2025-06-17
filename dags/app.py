from datetime import datetime, timedelta
from airflow import DAG
import requests
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

def extract_data_from_google_api():
    API_URL = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': 'inauthor:"Stephen King"',
        'maxResults': 40,
        'printType': 'books'
    }

    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    books = []

    for item in data.get('items', []):
        info = item.get('volumeInfo', {})
        
        # Extract ISBN_13 if available
        isbn_13 = None
        for identifier in info.get('industryIdentifiers', []):
            if identifier.get('type') == 'ISBN_13':
                isbn_13 = identifier.get('identifier')
                break

        book = {
            'title': info.get('title'),
            'authors': ", ".join(info.get('authors', [])),  # join list into string
            'publisher': info.get('publisher'),
            'publishedDate': info.get('publishedDate'),
            'description': info.get('description'),
            'pageCount': info.get('pageCount'),
            'categories': ", ".join(info.get('categories', [])),
            'language': info.get('language'),
            'isbn_13': isbn_13,
            'infoLink': info.get('infoLink')
        }
        books.append(book)

    # Create DataFrame
    df = pd.DataFrame(books)

    # Optional: Clean publishedDate to just year (if format is YYYY-MM-DD or YYYY)
    df['publishedYear'] = df['publishedDate'].str[:4]
    return df.to_dict(orient='records')

# Insert function
def insert_book_data_into_postgres(ti):
    book_data = ti.xcom_pull(task_ids='fetch_book_data')
    if not book_data:
        raise ValueError("No book data returned from fetch task")

    postgres_hook = PostgresHook(postgres_conn_id='books_connection')

    insert_query = """
    INSERT INTO books (
        title, authors, publisher, published_date, description,
        page_count, categories, language, isbn_13, info_link, published_year
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for book in book_data:
        postgres_hook.run(insert_query, parameters=(
            book['title'], book['authors'], book['publisher'], book['publishedDate'],
            book['description'], book['pageCount'], book['categories'],
            book['language'], book['isbn_13'], book['infoLink'], book['publishedYear']
        ))

# DAG definition
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_and_store_google_books',
    default_args=default_args,
    description='Fetch Stephen King books from Google Books API and store in Postgres',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Tasks
fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=extract_data_from_google_api,
    dag=dag,
)

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='books_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT,
        authors TEXT,
        publisher TEXT,
        published_date TEXT,
        description TEXT,
        page_count INT,
        categories TEXT,
        language TEXT,
        isbn_13 TEXT,
        info_link TEXT,
        published_year TEXT
    );
    """,
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_postgres,
    dag=dag,
)

# Task dependencies
fetch_book_data_task >> create_table_task >> insert_book_data_task