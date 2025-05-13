
# 2_Mapping.py

# import streamlit as st
# from app.backend.event_log_attributes_mapper import map_event_log_columns
#
# st.header("Event Log Column Mapping")
#
# df = st.session_state.get("df")
#
# if df is not None:
#     st.dataframe(df.head())
#
#     columns = df.columns.tolist()
#
#     with st.form("column_mapping_form"):
#         case_col = st.selectbox(
#             "Select Case ID column",
#             columns,
#             index=columns.index("case:concept:name") if "case:concept:name" in columns else 0
#         )
#         activity_col = st.selectbox(
#             "Select Activity column",
#             columns,
#             index=columns.index("concept:name") if "concept:name" in columns else 1
#         )
#         timestamp_col = st.selectbox(
#             "Select Timestamp column",
#             columns,
#             index=columns.index("time:timestamp") if "time:timestamp" in columns else 2
#         )
#         resource_col = st.selectbox(
#             "Select Resource column (optional)",
#             ["(None)"] + columns,
#             index=(columns.index("org:resource") + 1) if "org:resource" in columns else 0
#         )
#
#         submitted = st.form_submit_button("Confirm", type="primary")
#
#     if submitted:
#         mapping = map_event_log_columns(df, case_col, activity_col, timestamp_col, resource_col)
#         st.session_state["column_mapping"] = mapping
#         st.success("Columns successfully mapped!")
#
#         st.subheader("Mapped Attributes")
#         st.table({
#             "Event Log Attribute": ["CaseID", "Activity", "Timestamp", "Resource"],
#             "Selected Column": [
#                 mapping["caseID"],
#                 mapping["activity"],
#                 mapping["timestamp"],
#                 mapping["resource"] or "(None)"
#             ]
#         })
#
#         # #st.session_state["navigate_to_filter_visualization"] = True
#         # st.button("Next", type="primary", key="Next_to_query_visualization")
#         # st.session_state["navigate_to_filter_and_visualization"] = "pages/3_Filter_Visualization.py"
#         # st.rerun()
#
# else:
#     st.warning("Please upload a file first on the Upload page.")
#
# col1, col2, col3 = st.columns([1, 6, 1])
#
# with col1:
#     if st.button("Back", type="secondary", key="Back_to_upload"):
#         st.switch_page("pages/1_Upload.py")
# with col3:
#     if st.button("Next", type="primary", key="Next_to_query_visualization"):
#         st.session_state["navigate_to_filter_and_visualization"] = "pages/3_Filter_Visualization.py"
#         st.rerun()
# if "navigate_to_filter_and_visualization" in st.session_state:
#     st.switch_page(st.session_state.pop("navigate_to_filter_and_visualization"))

import streamlit as st
from app.backend.event_log_attributes_mapper import map_event_log_columns

st.header("Event Log Column Mapping")

df = st.session_state.get("df")

if df is not None:
    if "column_mapping" in st.session_state:
        mapping = st.session_state["column_mapping"]
        st.success("Columns already mapped!")

        st.subheader("Mapped Attributes")
        st.table({
            "Event Log Attribute": ["CaseID", "Activity", "Timestamp", "Resource"],
            "Selected Column": [
                mapping["caseID"],
                mapping["activity"],
                mapping["timestamp"],
                mapping["resource"] or "(None)"
            ]
        })
        if st.button("Edit Mapping"):
            del st.session_state["column_mapping"]
            st.rerun()
    else:
        st.dataframe(df.head())

        columns = df.columns.tolist()

        with st.form("column_mapping_form"):
            case_col = st.selectbox(
                "Select Case ID column",
                columns,
                index=columns.index("case:concept:name") if "case:concept:name" in columns else 0
            )
            activity_col = st.selectbox(
                "Select Activity column",
                columns,
                index=columns.index("concept:name") if "concept:name" in columns else 1
            )
            timestamp_col = st.selectbox(
                "Select Timestamp column",
                columns,
                index=columns.index("time:timestamp") if "time:timestamp" in columns else 2
            )
            resource_col = st.selectbox(
                "Select Resource column (optional)",
                ["(None)"] + columns,
                index=(columns.index("org:resource") + 1) if "org:resource" in columns else 0
            )

            submitted = st.form_submit_button("Confirm", type="primary")

        if submitted:
            mapping = map_event_log_columns(df, case_col, activity_col, timestamp_col, resource_col)
            st.session_state["column_mapping"] = mapping
            st.success("Columns successfully mapped!")

            st.subheader("Mapped Attributes")
            st.table({
                "Event Log Attribute": ["CaseID", "Activity", "Timestamp", "Resource"],
                "Selected Column": [
                    mapping["caseID"],
                    mapping["activity"],
                    mapping["timestamp"],
                    mapping["resource"] or "(None)"
                ]
            })

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("Back", type="secondary", key="Back_to_upload"):
            st.switch_page("pages/1_Upload.py")
    with col3:
        if "column_mapping" in st.session_state:
            if st.button("Next", type="primary", key="Next_to_query_visualization"):
                st.switch_page("pages/3_Filter_Visualization.py")
else:
    st.warning("Please upload a file first on the Upload page.")
