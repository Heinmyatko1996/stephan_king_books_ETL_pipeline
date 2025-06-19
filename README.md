# 📚 Stephen King Books ETL Pipeline

This is an end-to-end ETL pipeline project that extracts data from the **Google Books API** (focused on Stephen King’s works), processes it using **Python**, and loads the data into a **PostgreSQL** database, all orchestrated via **Apache Airflow**. Optionally, data can be visualized in **Apache Superset**.

---

## 🔧 Tech Stack

- 🐳 Docker
- ⛓️ Docker Compose
- 🐘 PostgreSQL
- 🌀 Apache Airflow (optional: add to Docker setup)
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
```

### 2. Run the Docker Stack

```bash
docker-compose up --build
```

- PostgreSQL will run in a container with DB name `superset`, user `superset`, and password `superset`.

---

## 🐍 Run ETL Script Manually

Make sure your virtualenv is active, or install dependencies with:

```bash
pip install requests psycopg2-binary
```

Then run:

```bash
python app.py
```

> This script connects to the running Postgres container and loads data into a table (e.g., `stephen_king_books`).

---

## 🧪 Example Output Table (PostgreSQL)

| title                         | authors        | publisher       | published_date |
|------------------------------|----------------|------------------|----------------|
| The Shining                  | Stephen King   | Doubleday        | 1977-01-28     |
| IT                           | Stephen King   | Viking           | 1986-09-15     |
| ...                          | ...            | ...              | ...            |

---

## 📊 Optional: Visualize with Superset

Once data is loaded, you can:
1. Log into Superset at `http://localhost:8088/dash` (username: `admin`, password: `admin`)
2. Connect to the `superset` Postgres DB
3. Explore or create charts using the `stephen_king_books` table

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
- Integration between Airflow (or cron), PostgreSQL, and Superset

---

## 📄 License

MIT License. See [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

Thanks to Google Books API and Stephen King for being prolific enough to build pipelines on!
