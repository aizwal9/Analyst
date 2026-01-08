from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from src.db_config import get_database, get_schema_info
from src.state import AgentState

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def clean_data_for_llm(data):
    """
    Helper to convert complex Python objects (UUID, Decimal)
    into a string format that is easier for the LLM to read.
    """
    if isinstance(data, list):
        # Convert list of tuples/objects to string, replacing specific types
        clean_str = str(data)
        clean_str = clean_str.replace("UUID(", "").replace(")", "")
        clean_str = clean_str.replace("Decimal(", "").replace(")", "")
        return clean_str
    return str(data)

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

def chart_generator_node(state: AgentState):
    """
    Analyzes the query result and user question to decide if a chart is needed.
    Generates a Recharts-compatible JSON spec if yes.
    """
    print("--- CHART GENERATOR NODE ---")
    data = state.get("query_result")
    question = state["messages"][-1].content

    if not data or "Error" in str(data):
        print("No valid data to visualize.")
        return {"visualization_spec" : None}

    template = """
    You are a Data Visualization Expert.
    Given the following dataset and user question, decide if a chart is appropriate.
    
    User Question: {question}
    Data: {data}
    
    If the data is suitable for a chart (e.g., time series, comparison, distribution):
    1. Determine the best chart type ("bar","line","area","pie").
    2. Generate a JSON configuration compatible with Recharts (React).
    3. The JSON must have:
    - `type` : The chart type
    - `data` : The data array formatted for the chart
    - `xKey` : The key for the X-axis
    - `series` : Array of objects for Y-axis data (e.g. ,[ {{ "dataKey":"total_spend", "color":"#8884d8"}}])
    - `title` : A title for the chart
    
    If no chart is needed (e.g., single number results), return an empty JSON {{}}.
    
    Return ONLY valid JSON.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "Generate the chart config.")
    ])

    chain = prompt | llm | JsonOutputParser()

    try:
        chart_config = chain.invoke({"question":question, "data":str(data)[:3000]}) #Truncating to avoid token limit

        if chart_config and chart_config.get('type'):
            print(f"Chart Type: {chart_config.get('type')}")
            return {"visualization_spec" : chart_config}
        else:
            print("No chart needed.")
            return {"visualization_spec" : None}

    except Exception as ex:
        print(f"Chart generation failed:{ex}")
        return {"visualization_spec" : None}

def marketing_agent_node(state: AgentState):
    """
    Checks if the user request implies an action (email,report,etc.).
    If yes, drafts the content.
    """
    print("--- MARKETING AGENT NODE ---")
    raw_data = state.get("query_result")
    question = state["messages"][-1].content.lower()

    triggers = ["email","draft","send","write to","contact"]
    if not any(trigger in question for trigger in triggers):
        return {"email_draft" : None , "needs_approval":False}

    # Clean data for email context
    data_str = clean_data_for_llm(raw_data)

    template = """
    You are a CRM Marketing Expert.
    The user wants to send an email based on the following data query results.
    
    User Question: {question}
    Data : {data}
    
    Task:
    Write a professional, personalized email draft.
    If the data contains customer names, use placeholders like [Customer Name].
    Keep it concise and action-oriented.
    
    Return ONLY the email text.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
    ])
    chain = prompt | llm | StrOutputParser()

    try:
        email_draft = chain.invoke({"question":question, "data":str(data_str)[:3000]})
        print(f"Email Drafted: {email_draft}")

        return {
            "email_draft" : email_draft,
            "needs_approval" : True
        }

    except Exception as ex:
        print(f"Email draft failed: {ex}")
        return {"email_draft" : None , "needs_approval":False}

def send_mail_node(state: AgentState):
    """
    This is the FINAL action node.
    We interrupt BEFORE this node executes.
    """

    print("--- SEND EMAIL NODE ---")
    email_draft = state.get("email_draft")

    print(f"\n🚀 Sending Email ...\n Content : {email_draft[:100]}...\n")

    return {
        "messages" : [HumanMessage(content="✅ Email sent!")]
    }