import streamlit as st
# Main application file for the Event Log Analyzer.
# Configures the Streamlit page layout and defines navigation between Upload, Mapping, Visualization, and Exploration pages.

st.set_page_config(page_title="Event Log Analyzer", layout="wide")

st.title("Event Log Analyzer")
pages = (
    st.Page("pages/1_Upload.py", title="Upload File"),
    st.Page("pages/2_Mapping.py", title="Map Columns"),
    st.Page("pages/3_Filter_Visualization.py", title="Filter and Visualize"),
    st.Page("pages/4_Exploration_Tracker.py", title="Data Provenance")
)

pg = st.navigation(pages)

pg.run()

