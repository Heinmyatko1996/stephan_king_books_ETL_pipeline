# 📚 Stephen King Books ETL Pipeline

This is an end-to-end ETL pipeline project that extracts data from the **Google Books API** (focused on Stephen King’s works), processes it using **Python**, and loads the data into a **PostgreSQL** database, all orchestrated via **Apache Airflow**. Optionally, data can be visualized in **Apache Superset**.

---

## 🔧 Tech Stack

- 🐳 Docker
- ⛓️ Docker Compose
- 🐘 PostgreSQL
- 🌀 Apache Airflow
- 🔍 Google Books API
- 🐍 Python (`requests`, `json`, etc.)
- 📊 Apache Superset (optional)

---

## 📁 Project Structure

```
stephan_king_books_ETL_pipeline/
├── app.py                # Main ETL script (extract-transform-load)
├── dags/                 # Airflow DAGs (if applicable)
├── config/               # Configuration files
├── plugins/              # Airflow plugins (optional)
├── logs/                 # Airflow logs
├── docker-compose.yml    # Superset + Postgres stack
├── venv/                 # Local Python virtual environment (excluded from Docker)
└── README.md             # This file
```

---

## 🚀 How It Works

1. **Extract**: Query the [Google Books API](https://developers.google.com/books) to retrieve books authored by Stephen King.
2. **Transform**: Clean and structure the JSON response.
3. **Load**: Insert structured data into a PostgreSQL database inside Docker.

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Heinmyatko1996/stephan_king_books_ETL_pipeline
cd stephan_king_books_ETL_pipeline
venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Docker Stack

```bash
docker compose up -d
```

- PostgreSQL will run in a container with `stephan_king_books_etl_pipeline-postgres-1`.

---

## 🐍 Run ETL Script Manually (if virtual environment is already on, there is no need to run it manually, all data will be loaded)

Make sure your virtualenv is active, or install dependencies with:

```bash
pip install requests psycopg2-binary
```

Then run:

```bash
python app.py
```

> This script connects to the running Postgres container and loads data into a table (e.g., `books`).

---

## 🧪 Example Output Table (PostgreSQL)

![image](https://github.com/user-attachments/assets/ac82f07e-a178-4ec4-a40b-25f9136aeccd)

---

## 🛬 Airflow

Data is already been loaded using airflow dag. See the app.py python script for invoking api and loading data into postgres table.
Postgres database name: google_books

schema name: public

table name: books

---

## 📚 Data Source

- **Google Books API**  
  Docs: https://developers.google.com/books/docs/v1/using  
  Example Endpoint:  
  `https://www.googleapis.com/books/v1/volumes?q=inauthor:Stephen+King`

---

## 🧠 Key Learnings

- Dockerized development with multiple services
- ETL development and orchestration using Python
- API extraction and data normalization
- Integration between Airflow (or cron), PostgreSQL

---

## 📄 License

MIT License. See [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

Thanks to Google Books API and Stephen King for being prolific enough to build pipelines on!
