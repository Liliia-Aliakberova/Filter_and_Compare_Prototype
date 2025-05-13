import streamlit as st
import graphviz

st.subheader("Data Provenance Visualization")

if "saved_filters" not in st.session_state or not st.session_state["saved_filters"]:
    st.warning("No filters saved yet.")
else:
    dot = graphviz.Digraph()
    dot.node("Full Log")

    prev_node = "Full Log"
    for name, step in st.session_state["saved_filters"].items():
        filter_node = name
        condition_node = f"{name}_cond"

        # Main filter node (Filter 3, Filter 4, etc.)
        dot.node(filter_node, label=name, shape="ellipse", style="filled", fillcolor="#cce5ff")

        # Separate node for the condition
        dot.node(condition_node, label=step["condition"], shape="note", fontsize="10")

        # Solid edge from previous filter step to this filter node
        dot.edge(prev_node, filter_node)

        # Dotted edge from the filter name node to the condition node
        dot.edge(filter_node, condition_node, style="dotted")

        prev_node = filter_node

    st.graphviz_chart(dot)
