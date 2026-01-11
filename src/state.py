from typing import TypedDict, List, Optional, Any, Dict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Defines the shared state of the graph.
    Each agent (node) can read from and write to this state.
    """

    # The conversation history (User inputs + AI responses)
    messages: List[BaseMessage]

    # 1. SQL Agent Outputs
    sql_query: Optional[str]  # The generated SQL
    query_result: Optional[Any]  # The raw data returned from the DB (List of dicts or string)

    error: Optional[str]  # Stores the DB error message if any
    retry_count: int  # Tracks how many times we've tried to fix it

    # Chart & Marketing Outputs
    visualization_spec: Optional[Dict]
    email_draft: Optional[str]
    needs_approval: bool