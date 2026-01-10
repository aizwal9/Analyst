# Text-to-Action Analyst

A powerful AI-driven data analyst agent built with **FastAPI**, **LangChain**, and **LangGraph**. This application translates natural language queries into SQL, executes them against a PostgreSQL database (Olist E-commerce dataset), generates visualization specifications, and drafts actionable emails—all with a human-in-the-loop approval workflow.

## 🚀 Features

-   **Natural Language to SQL**: Converts user questions into optimized SQL queries.
-   **Data Visualization**: Automatically generates Recharts-compatible JSON specifications for charts when appropriate.
-   **Actionable Insights**: Drafts professional emails based on data analysis results.
-   **Human-in-the-Loop**: Includes an approval mechanism for sensitive actions (like sending emails).
-   **Session History**: Tracks chat history and context using thread IDs.

## 📸 Examples

![Example 1](img.png)
![Example 2](img_1.png)
![Example 3](img_2.png)

## 🛠️ Tech Stack

-   **Framework**: FastAPI
-   **Orchestration**: LangGraph, LangChain
-   **LLM**: OpenAI GPT-4o
-   **Database**: PostgreSQL (Olist Dataset)
-   **ORM/SQL Tooling**: SQLAlchemy, psycopg2

## 🗄️ Database Schema

![Database Schema](schema.png)

## 📋 Prerequisites

-   Python 3.10+
-   PostgreSQL database loaded with the [Olist E-commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
-   OpenAI API Key.

## ⚙️ Setup & Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd data_analyst
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=postgresql://user:password@host:port/database_name
    ```

## 🏃‍♂️ Running the Application

Start the FastAPI server:

```bash
python main.py
```
The server will start at `http://0.0.0.0:8000`.

## 🔌 API Endpoints

### Chat
-   **POST** `/chat`
    -   Initiates analysis or continues a conversation.
    -   **Body**: `{"message": "Show top 5 customers", "thread_id": "123"}`

### Approval
-   **POST** `/approve`
    -   Approves or rejects a pending action (e.g., sending an email).
    -   **Body**: `{"thread_id": "123", "approved": true}`

### History
-   **GET** `/history` - List all sessions.
-   **GET** `/history/{thread_id}` - Get full history for a specific thread.

## 📂 Project Structure

```
data_analyst/
├── main.py              # FastAPI entry point
├── requirements.txt     # Project dependencies
├── src/
│   ├── db_config.py     # Database connection setup
│   ├── db_history.py    # Chat history management
│   ├── graph.py         # LangGraph workflow definition
│   ├── nodes.py         # Agent nodes (SQL, Chart, Marketing)
│   └── state.py         # State definition for the graph
└── ...
```
