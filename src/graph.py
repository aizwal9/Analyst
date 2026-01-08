from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import sql_analyst_node
from dotenv import load_dotenv
load_dotenv()

# 1. Initialize the Graph with our State definition
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("sql_analyst", sql_analyst_node)

# 3. Define Edges (The flow of execution)
# Entry point -> SQL Analyst
workflow.set_entry_point("sql_analyst")

# SQL Analyst -> End (For now, we stop here)
workflow.add_edge("sql_analyst", END)

# 4. Compile the graph
app = workflow.compile()

if __name__ == "__main__":
    # Simple test to verify the SQL node works
    from langchain_core.messages import HumanMessage

    # A sample question relevant to the Olist dataset
    test_input = {
        "messages": [HumanMessage(content="Show me the top 3 customers by total spend")]
    }

    print("🚀 Starting Graph...")
    result = app.invoke(test_input)
    print("🏁 Graph Finished.")
    print(f"Final State SQL: {result.get('sql_query')}")
    print(f"Final State Data: {result.get('query_result')}")