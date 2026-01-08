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

    # 2. Chart Agent Outputs
    visualization_spec: Optional[Dict]  # Chart.js or Recharts configuration

    # 3. Marketing Agent Outputs
    email_draft: Optional[str]  # The generated email text

    # Control Flags
    needs_approval: bool  # If True, pause before sending email