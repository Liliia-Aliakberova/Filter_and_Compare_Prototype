# import streamlit as st
#
# def column_selection_ui(df):
#     st.header("Select Event Log Attribute Columns")
#
#     st.dataframe(df.head())
#
#     columns = df.columns.tolist()
#
#     with st.form("column_mapping_form"):
#         case_col = st.selectbox("Select Case ID column", columns,
#                                 index=columns.index("case:concept:name") if "case:concept:name" in columns else 0)
#         activity_col = st.selectbox("Select Activity column", columns,
#                                     index=columns.index("concept:name") if "concept:name" in columns else 1)
#         timestamp_col = st.selectbox("Select Timestamp column", columns,
#                                      index=columns.index("time:timestamp") if "time:timestamp" in columns else 2)
#         resource_col = st.selectbox("Select Resource column (optional)", ["(None)"] + columns,
#                                     index=(columns.index("org:resource") + 1) if "org:resource" in columns else 0)
#
#         submitted = st.form_submit_button("Confirm", type="primary")
#
#     if submitted:
#         return {
#             "caseID": case_col,
#             "activity": activity_col,
#             "timestamp": timestamp_col,
#             "resource": None if resource_col == "(None)" else resource_col
#         }
#
#     return None

# event_log_attributes_mapper.py

def map_event_log_columns(df, case_col, activity_col, timestamp_col, resource_col):
    """
    Processes the mapping of event log columns.

    Parameters:
    - df: The DataFrame containing the event log.
    - case_col: Selected column for Case ID.
    - activity_col: Selected column for Activity.
    - timestamp_col: Selected column for Timestamp.
    - resource_col: Selected column for Resource (optional).

    Returns:
    - A dictionary with the mapped columns.
    """
    mapping = {
        "caseID": case_col,
        "activity": activity_col,
        "timestamp": timestamp_col,
        "resource": None if resource_col == "(None)" else resource_col
    }
    return mapping

