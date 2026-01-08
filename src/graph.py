from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import sql_analyst_node, chart_generator_node, marketing_agent_node, send_mail_node
from dotenv import load_dotenv
load_dotenv()

workflow = StateGraph(AgentState)

workflow.add_node("sql_analyst", sql_analyst_node)
workflow.add_node("chart_generator",chart_generator_node)
workflow.add_node("marketing_agent",marketing_agent_node)
workflow.add_node("send_email",send_mail_node)

workflow.set_entry_point("sql_analyst")
workflow.add_edge("sql_analyst", "chart_generator")
workflow.add_edge("chart_generator","marketing_agent")


def should_continue(state: AgentState):
    if state.get("needs_approval"):
        return "send_email"
    return END

workflow.add_conditional_edges(
    "marketing_agent",
    should_continue,
    {
        "send_email" : "send_email",
        END : END
    }
)

workflow.add_edge("send_email",END)
memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["send_email"]
)

if __name__ == "__main__":
    # Simple test to verify the SQL node works
    from langchain_core.messages import HumanMessage

    config = {"configurable" : {"thread_id" : "demo_thread_1"}}
    user_query = "Find the top 5 customers by spend and draft a thank you email for them."

    print("🚀 Starting Graph...")

    inputs = {"messages" : [HumanMessage(content=user_query)]}

    for event in app.stream(inputs,config=config):
        pass

    snapshot = app.get_state(config)
    print("\n⏸️  GRAPH PAUSED FOR HUMAN REVIEW ⏸️")
    print(f"Next Node: {snapshot.next}")
    print(f"Draft Email: {snapshot.values['email_draft'][:100]}...")

    response = input("\nDo you want to send this email? (yes/no):")

    if response.lower() == "yes":
        for event in app.stream(None,config=config):
            for key,value in event.items():
                print(f"Finished Node: {key}")
        print("🏁 Graph Finished.")
    else:
        print("❌ Operation Cancelled")