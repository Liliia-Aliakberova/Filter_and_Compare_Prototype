# import streamlit as st
# import pandas as pd
# import altair as alt
# from datetime import datetime
# from app.backend.query_processor import filter_cases_by_condition
#
#
# # Function to apply the filter and generate result sets
# def apply_filter(df, condition, case_column):
#     try:
#         # Apply filter using the existing function in query_processor
#         result_set, complement_set = filter_cases_by_condition(df, condition, case_column)
#
#         case_col = st.session_state["column_mapping"]["caseID"]
#
#         num_cases_result = result_set[case_col].nunique()
#         num_cases_complement = complement_set[case_col].nunique()
#
#         # st.write(f"Number of unique cases in result set: {num_cases_result}")
#         # st.write(f"Number of unique cases in complement set: {num_cases_complement}")
#
#         # Check if the filtering was successful by printing the sizes
#         st.write(f"Number of cases in result set: {num_cases_result}")
#         with st.expander("Result Set"):
#             st.dataframe(result_set)
#
#         st.write(f"Number of cases in complement set: {num_cases_complement}")
#         with st.expander("Complement Set"):
#             st.dataframe(complement_set)
#
#         # Store the filtered data in session state
#         st.session_state["result_set"] = result_set
#         st.session_state["complement_set"] = complement_set
#
#         # Display the filtered data
#         #st.success(f"Filtered {len(result_set)} cases that match the filter criteria.")
#         #st.success(f"Filtered {len(complement_set)} cases that don't match the filter criteria.")
#
#     except Exception as e:
#         st.error(f"Error applying filter: {e}")
#
#
# # Function to display the activity exclusivity dashboard
# def show_dashboard(result_set, complement_set):
#     st.subheader("Activity Exclusivity")
#
#     # Get full event log and column mapping
#     event_log = st.session_state.get("df")
#     mapping = st.session_state.get("column_mapping")
#
#     if event_log is None or mapping is None:
#         st.error("Event log or column mapping not found in session state.")
#         return
#
#     case_col = mapping["caseID"]
#     activity_col = mapping["activity"]
#
#     # Get case IDs from result and complement sets
#     result_case_ids = result_set.index if result_set.index.name == case_col else result_set[case_col]
#     complement_case_ids = complement_set.index if complement_set.index.name == case_col else complement_set[case_col]
#
#     # Filter event log to get relevant event-level data
#     result_events = event_log[event_log[case_col].isin(result_case_ids)]
#     complement_events = event_log[event_log[case_col].isin(complement_case_ids)]
#
#     # Compute activity distributions based on unique cases per activity
#     result_activities = (
#         result_events[[case_col, activity_col]]
#         .drop_duplicates()
#         .groupby(activity_col)[case_col]
#         .nunique()
#     )
#
#     complement_activities = (
#         complement_events[[case_col, activity_col]]
#         .drop_duplicates()
#         .groupby(activity_col)[case_col]
#         .nunique()
#     )
#
#     # Combine into one DataFrame
#     activities = pd.DataFrame({
#         "Activity": result_activities.index,
#         "Result Set (Cases)": result_activities.values,
#         "Complement Set (Cases)": complement_activities.reindex(result_activities.index, fill_value=0).values
#     })
#
#     st.write("Number of unique cases per activity:")
#     st.dataframe(activities)
#
#     # Plot: Result Set
#     #shared scale
#     shared_y_scale = alt.Scale(
#         domain=[0, max(activities["Result Set (Cases)"].max(), activities["Complement Set (Cases)"].max())])
#
#     col1, col2 = st.columns(2)
#
#     with col1:
#         # Chart: Result Set
#         st.markdown("#### Activity Presence - Result Set")
#         chart_result = alt.Chart(activities).mark_bar().encode(
#             x='Activity:N',
#             y=alt.Y('Result Set (Cases):Q', scale=shared_y_scale),
#             color='Activity:N'
#         ).interactive()
#         st.altair_chart(chart_result, use_container_width=True)
#
#         # Chart: Complement Set
#         st.markdown("#### Activity Presence - Complement Set")
#         chart_complement = alt.Chart(activities).mark_bar().encode(
#             x='Activity:N',
#             y=alt.Y('Complement Set (Cases):Q', scale=shared_y_scale),
#             color='Activity:N'
#         ).interactive()
#         st.altair_chart(chart_complement, use_container_width=True)
#
#     # Continue with attribute distribution
#     with col2:
#         show_attribute_distribution(result_set, complement_set)
#
# # Function to display distribution of selected attribute
# def show_attribute_distribution(result_set, complement_set):
#     st.subheader("Distribution of Numeric Attribute")
#
#     # Retrieve mapping and necessary columns
#     mapping = st.session_state.get("column_mapping")
#     if not mapping:
#         st.error("Column mapping not found.")
#         return
#
#     case_col = mapping["caseID"]
#     timestamp_col = mapping["timestamp"]
#
#     # Identify numeric columns
#     numeric_columns = result_set.select_dtypes(include=["number"]).columns
#
#     if len(numeric_columns) == 0:
#         st.warning("No numeric columns available for visualization.")
#         return
#
#     selected_column = st.selectbox("Select a numeric attribute to visualize", numeric_columns)
#
#     if selected_column:
#         # Prepare copies to avoid modifying session data
#         result_set = result_set.copy()
#         complement_set = complement_set.copy()
#
#         # Ensure timestamp column is datetime
#         result_set[timestamp_col] = pd.to_datetime(result_set[timestamp_col], errors='coerce', utc=True)
#         complement_set[timestamp_col] = pd.to_datetime(complement_set[timestamp_col], errors='coerce', utc=True)
#
#         # Sort and get last non-null value per case
#         result_df = (
#             result_set.dropna(subset=[selected_column])
#             .sort_values(by=[case_col, timestamp_col])
#             .groupby(case_col)
#             .last()
#             .reset_index()
#         )
#
#         complement_df = (
#             complement_set.dropna(subset=[selected_column])
#             .sort_values(by=[case_col, timestamp_col])
#             .groupby(case_col)
#             .last()
#             .reset_index()
#         )
#
#         min_val = min(result_df[selected_column].min(), complement_df[selected_column].min())
#         max_val = max(result_df[selected_column].max(), complement_df[selected_column].max())
#
#         max_count = max(
#             result_df[selected_column].value_counts().max(),
#             complement_df[selected_column].value_counts().max()
#         )
#
#         # Shared x and y scales
#         x_shared = alt.Scale(domain=[min_val, max_val])
#         y_shared = alt.Scale(domain=[0, max_count])
#
#         # Chart for result set
#         chart_result_set = alt.Chart(result_df).mark_bar().encode(
#             alt.X(f'{selected_column}:Q', scale=x_shared),
#             alt.Y('count()', scale=y_shared),
#             color=alt.value('#1f77b4')
#         ).properties(
#             title=f"{selected_column} Distribution - Result Set"
#         ).interactive()
#
#         # Chart for complement set
#         chart_complement_set = alt.Chart(complement_df).mark_bar().encode(
#             alt.X(f'{selected_column}:Q', scale=x_shared),
#             alt.Y('count()', scale=y_shared),
#             color=alt.value('#ff7f0e')
#         ).properties(
#             title=f"{selected_column} Distribution - Complement Set"
#         ).interactive()
#
#         # Display separately but with same scales
#         st.altair_chart(chart_result_set, use_container_width=True)
#         st.altair_chart(chart_complement_set, use_container_width=True)
#
#         # # Altair Chart - Result Set
#         # chart_result_set = alt.Chart(result_df).mark_bar().encode(
#         #     alt.X(f'{selected_column}:Q', bin=False),
#         #     y='count()'
#         # ).properties(title=f"{selected_column} Distribution - Result Set").interactive()
#         #
#         # # Altair Chart - Complement Set
#         # chart_complement_set = alt.Chart(complement_df).mark_bar().encode(
#         #     alt.X(f'{selected_column}:Q', bin=False),
#         #     y='count()'
#         # ).properties(title=f"{selected_column} Distribution - Complement Set").interactive()
#         #
#         # st.altair_chart(chart_result_set, use_container_width=True)
#         # st.altair_chart(chart_complement_set, use_container_width=True)
#     else:
#         st.warning("No numeric columns available for visualization.")
#
# # UI for case filtering
# def case_filter_ui():
#     st.header("Case Filter")
#
#     # Get the uploaded DataFrame and column mapping
#     df = st.session_state.get("df")
#     column_mapping = st.session_state.get("column_mapping")
#
#     if df is None or column_mapping is None:
#         st.warning("Please upload and map your data first.")
#         return
#
#     case_col = column_mapping["caseID"]
#     timestamp_col = column_mapping["timestamp"]
#
#     # Ensure timestamp is in datetime format and convert it to UTC if necessary
#     df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)
#
#     st.subheader("Build Filter")
#
#     # Select a column to filter on
#     selected_column = st.selectbox("Choose a column to filter", df.columns)
#
#     if selected_column not in df.columns:
#         st.warning("Selected column not found in data.")
#         return
#
#     # Apply datetime conversion only to datetime-like columns (not categorical or numeric)
#     col_dtype = df[selected_column].dtype
#     condition = None
#
#     if pd.api.types.is_datetime64_any_dtype(df[selected_column]):
#         # Apply to datetime columns only
#         min_date = df[selected_column].min()
#         max_date = df[selected_column].max()
#
#         #a date-time range selector for datetime columns (date + time)
#         start_datetime = st.date_input("Select start date", min_date, max_value=max_date)
#         end_datetime = st.date_input("Select end date", max_date, min_value=min_date)
#
#         min_time = df[selected_column].min().time()
#         max_time = df[selected_column].max().time()
#
#         start_time = st.time_input("Select start time", min_time)
#         end_time = st.time_input("Select end time", max_time)
#
#         start_datetime = datetime.combine(start_datetime, start_time).astimezone(pd.Timestamp('UTC').tzinfo)
#         end_datetime = datetime.combine(end_datetime, end_time).astimezone(pd.Timestamp('UTC').tzinfo)
#
#         # Filter condition with datetime comparison in UTC
#         condition = f"('{start_datetime}' <= `{selected_column}`) and (`{selected_column}` <= '{end_datetime}')"
#
#     # Other types of columns (boolean, categorical, numeric) are handled similarly
#     elif df[selected_column].dtype == object:
#         # Allow searching for multiple categorical values
#         values = sorted(df[selected_column].dropna().unique().tolist())
#         selected_vals = st.multiselect("Select one or more values", values)
#         if selected_vals:
#             formatted_vals = ", ".join([repr(v) for v in selected_vals])
#             condition = f"`{selected_column}` in [{formatted_vals}]"
#
#     elif pd.api.types.is_numeric_dtype(df[selected_column]):
#         unique_vals = sorted(df[selected_column].dropna().unique())
#         selected_vals = st.multiselect("Select one or more values", unique_vals)
#         if selected_vals:
#             formatted_vals = ", ".join([str(v) for v in selected_vals])
#             condition = f"`{selected_column}` in [{formatted_vals}]"
#
#     elif df[selected_column].dropna().isin([True, False]).all():
#         val = st.selectbox("Choose value", df[selected_column].dropna().unique())
#         condition = f"`{selected_column}` == {val}"
#
#     else:
#         st.warning("Unsupported column type")
#
#     if condition and st.button("Apply Filter"):
#         apply_filter(df, condition, case_col)
#
#     if "show_dashboard" in st.session_state and st.session_state.get("show_dashboard", False):
#         show_dashboard(st.session_state["result_set"], st.session_state["complement_set"])
#
#     # Show button for triggering the dashboard visualization
#     if st.button("Show Dashboard"):
#         st.session_state.show_dashboard = True
#         st.rerun()
#
