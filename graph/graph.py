from langgraph.graph import StateGraph, START, END
from graph.state import graph_state
from graph.node import retrieve_nodes, generate_answer_nodes



def build_graph():
    graph = StateGraph(graph_state) #state graph is a graph that is built using the state of the graph
    graph.add_node("retrieve_nodes", retrieve_nodes)
    graph.add_node("generate_answer_nodes", generate_answer_nodes)
    graph.set_entry_point("retrieve_nodes")
    graph.add_edge("retrieve_nodes", "generate_answer_nodes")
    graph.add_edge("generate_answer_nodes", END)

    return graph.compile()