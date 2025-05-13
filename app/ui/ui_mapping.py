# import streamlit as st
# from app.backend.event_log_attributes_mapper import column_selection_ui
#
# def column_mapping_ui():
#     st.header("Event Log Column Mapping")
#
#     df = st.session_state.get("df")
#
#     if df is not None:
#         mapping = column_selection_ui(df)
#
#         if mapping:
#             st.session_state["column_mapping"] = mapping
#             st.success("Columns successfully mapped!")
#
#             st.subheader("Mapped Attributes")
#             st.table({
#                 "Event Log Attribute": ["CaseID", "Activity", "Timestamp", "Resource"],
#                 "Selected Column": [
#                     mapping["caseID"],
#                     mapping["activity"],
#                     mapping["timestamp"],
#                     mapping["resource"] or "(None)"
#                 ]
#             })
#             col1, col2, col3 = st.columns([1, 6, 1])
#             with col3:
#                 st.button("Next", on_click=lambda: st.session_state.update({"page": "query_and_visualization"}),
#                           type="primary")


