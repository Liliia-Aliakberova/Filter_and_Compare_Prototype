import streamlit as st
import graphviz

# ------------------------------------------------------------
# This file is dedicated to visualizing the user's exploration history of saved filters as a Graphviz diagram.
# ------------------------------------------------------------

st.subheader("Exploration Tracker")

if "saved_filters" not in st.session_state or not st.session_state["saved_filters"]:
    st.warning("No filters saved yet.")
else:
    dot = graphviz.Digraph()
    dot.node("Full Log")

    prev_node = "Full Log"
    for name, step in st.session_state["saved_filters"].items():
        filter_node = name
        condition_node = f"{name}_cond"

        dot.node(filter_node, label=name, shape="ellipse", style="filled", fillcolor="#cce5ff")

        dot.node(condition_node, label=step["condition"], shape="note", fontsize="10")

        dot.edge(prev_node, filter_node)

        dot.edge(filter_node, condition_node, style="dotted")

        prev_node = filter_node

    st.graphviz_chart(dot)
