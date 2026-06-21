from langgraph.graph import StateGraph, END
from state import DisasterState
from agents.intake import intake_agent
from agents.triage import triage_agent
from agents.resource import resource_agent
from agents.coordinator import coordinator_agent
from agents.reporter import reporter_agent

def build_graph():
    graph = StateGraph(DisasterState)

    #Setting nodes
    graph.add_node("intake", intake_agent)
    graph.add_node("triage", triage_agent)
    graph.add_node("resource", resource_agent)
    graph.add_node("coordinator", coordinator_agent)
    graph.add_node("reporter", reporter_agent)

    #Adding Edges
    graph.set_entry_point("intake")
    graph.add_edge("intake","triage")
    graph.add_edge("triage","resource")
    graph.add_edge("resource","coordinator")
    graph.add_edge("coordinator","reporter")
    graph.add_edge("reporter",END)

    return graph.compile()