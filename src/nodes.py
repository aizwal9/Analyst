import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import HumanMessage
from src.db_config import get_database, get_schema_info
from src.state import AgentState

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)


def sql_analyst_node(state: AgentState):
    """
    1. Analyzes the user's request.
    2. Fetches the DB Schema.
    3. Writes a SQL Query.
    4. Executes the Query.
    5. Returns data to the state.
    """
    print("--- SQL ANALYST NODE ---")

    user_question = state['messages'][-1].content
    schema = get_schema_info()

    template = """
    You are an expert PostgreSQL Data Analyst.
    Your task is to generate a syntactically correct PostgreSQL query to answer the user's question.

    Use the following database schema:
    {schema}

    Guidelines:
    1. Return ONLY the SQL query. No markdown formatting (```sql), no explanations.
    2. Use the `customers`, `orders`, `order_items`, `products`, and `order_payments` tables.
    3. When checking dates, assume the current date is 2018-10-17 (The Olist dataset ends around 2018).
    4. Cast monetary values to numeric/float if needed for aggregation.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{question}")
    ])

    sql_generator_chain = prompt | llm | StrOutputParser()

    try:
        generated_sql = sql_generator_chain.invoke({"schema": schema, "question": user_question})
        clean_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        print(f"Generated SQL: {clean_sql}")

        db = get_database()
        result = db.run(clean_sql)

        print(f"Query Result: {result}")

        return {
            "sql_query": clean_sql,
            "query_result": result
        }

    except Exception as e:
        return {
            "sql_query": "ERROR",
            "query_result": f"Error executing query: {str(e)}"
        }
