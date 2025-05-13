import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

from app.backend.query_processor import (
    filter_cases_by_condition,
    get_numeric_attributes_distribution_initial_state, get_numeric_attributes_distribution_last_state
)

from app.backend.visualization_builder import (
    build_activity_distribution_chart,
    build_numeric_distribution_chart
)

event_log = st.session_state.get("df")
df = st.session_state.get("df")
mapping = st.session_state.get("column_mapping")

case_col = mapping["caseID"]
activity_col = mapping["activity"]
timestamp_col = mapping["timestamp"]
resource_col = mapping.get("resource")

def apply_filter(df, condition, case_column):
    try:
        #st.write(f"Condition: {condition}")
        result_set, complement_set = filter_cases_by_condition(df, condition, case_column)



        st.write(f"Number of cases in result set: {result_set[case_col].nunique()}")
        with st.expander("Result Set"):
            st.dataframe(result_set)

        st.write(f"Number of cases in complement set: {complement_set[case_col].nunique()}")
        with st.expander("Complement Set"):
            st.dataframe(complement_set)

        st.session_state["result_set"] = result_set
        st.session_state["complement_set"] = complement_set

    except Exception as e:
        st.error(f"Error applying filter: {e}")

def show_dashboard(result_set, complement_set):

    col1, col2 = st.columns(2)
    # shared_y = alt.Scale(domain=[0, max(activities["Result Set (Cases)"].max(), activities["Complement Set (Cases)"].max())])

    with col1:
        show_activity_distribution(result_set, complement_set)
    with col2:
        show_attribute_distribution(result_set, complement_set)


def show_activity_distribution(result_set, complement_set):
    st.subheader("Activity Exclusivity")

    # event_log = st.session_state.get("df")

    if event_log is None or mapping is None:
        st.error("Event log or column mapping not found in session state.")
        return

    result_activities = result_set[[case_col, activity_col]].drop_duplicates().groupby(activity_col)[case_col].nunique()
    complement_activities = complement_set[[case_col, activity_col]].drop_duplicates().groupby(activity_col)[
        case_col].nunique()
    full_activities = event_log[[case_col, activity_col]].drop_duplicates().groupby(activity_col)[case_col].nunique()

    # Build combined DataFrame
    activity_data = pd.DataFrame({
        "Activity": full_activities.index,
        "Full Log": full_activities,
        "Result Set": result_activities.reindex(full_activities.index, fill_value=0),
        "Complement Set": complement_activities.reindex(full_activities.index, fill_value=0),
    }).reset_index(drop=True)

    # Build and show the interactive chart
    chart = build_activity_distribution_chart(activity_data)
    st.altair_chart(chart, use_container_width=True)

def show_attribute_distribution(result_set, complement_set):
    st.subheader("Distribution of Numeric Attribute")

    # mapping = st.session_state.get("column_mapping")
    if not mapping:
        st.error("Column mapping not found.")
        return

    numeric_columns = result_set.select_dtypes(include=["number"]).columns
    if len(numeric_columns) == 0:
        st.warning("No numeric columns available for visualization.")
        return

    selected_column = st.selectbox("Select a numeric attribute to visualize", numeric_columns)
    if selected_column:
        event_state = st.radio(
            "Select the state of the event attribute for visualization",
            ["First", "Latest"], horizontal=True,
            captions=[
                "Attribute value for the first event in the case",
                "Attribute value for the last event in the case"
            ],
        )

        if event_state == "Latest":
            result_df = get_numeric_attributes_distribution_last_state(result_set, case_col, timestamp_col,
                                                                       selected_column)
            complement_df = get_numeric_attributes_distribution_last_state(complement_set, case_col, timestamp_col,
                                                                           selected_column)
        else:
            result_df = get_numeric_attributes_distribution_initial_state(result_set, case_col, timestamp_col,
                                                                          selected_column)
            complement_df = get_numeric_attributes_distribution_initial_state(complement_set, case_col, timestamp_col,
                                                                              selected_column)

        min_val = min(result_df[selected_column].min(), complement_df[selected_column].min())
        max_val = max(result_df[selected_column].max(), complement_df[selected_column].max())

        max_count = max(
            result_df[selected_column].value_counts().max(),
            complement_df[selected_column].value_counts().max()
        )

        x_shared = alt.Scale(domain=[min_val, max_val])
        y_shared = alt.Scale(domain=[0, max_count])

        chart_result = build_numeric_distribution_chart(result_df, selected_column, "#1f77b4", "Result Set", x_shared,
                                                        y_shared)
        chart_complement = build_numeric_distribution_chart(complement_df, selected_column, "#ff7f0e", "Complement Set",
                                                            x_shared, y_shared)

        st.altair_chart(chart_result, use_container_width=True)
        st.altair_chart(chart_complement, use_container_width=True)


def case_filter_ui():
    st.header("Case Filter")

    if "has_visited_filter_page" not in st.session_state:
        st.session_state["has_visited_filter_page"] = True
        st.session_state["filter_applied"] = False
        st.session_state["last_filter_condition"] = None
        st.session_state["result_set"] = None
        st.session_state["complement_set"] = None

    #df = st.session_state.get("df")
    st.session_state["df"] = df
    column_mapping = st.session_state.get("column_mapping")

    if df is None or column_mapping is None:
        st.warning("Please upload and map your data first.")
        return

    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)
    st.subheader("Build Filter")

    selected_column = st.selectbox("Choose a column to filter", df.columns)
    if selected_column not in df.columns:
        st.warning("Selected column not found in data.")
        return

    condition = None
    previous_condition = st.session_state.get("last_filter_condition")

    if pd.api.types.is_datetime64_any_dtype(df[selected_column]):
        min_date = df[selected_column].min()
        max_date = df[selected_column].max()

        start_date = st.date_input("Select start date", min_date, max_value=max_date)
        end_date = st.date_input("Select end date", max_date, min_value=min_date)

        start_time = st.time_input("Select start time", min_date.time())
        end_time = st.time_input("Select end time", max_date.time())

        start_dt = datetime.combine(start_date, start_time).astimezone(pd.Timestamp('UTC').tzinfo)
        end_dt = datetime.combine(end_date, end_time).astimezone(pd.Timestamp('UTC').tzinfo)

        condition = f"('{start_dt}' <= {selected_column}) and ({selected_column} <= '{end_dt}')"


    elif df[selected_column].dtype == object:
        values = sorted(df[selected_column].dropna().unique().tolist())
        selected_vals = st.multiselect("Select values", values)
        if selected_vals:
            formatted_vals = ", ".join([repr(v) for v in selected_vals])
            condition = f"`{selected_column}` in [{formatted_vals}]"

    elif pd.api.types.is_numeric_dtype(df[selected_column]):
        values = sorted(df[selected_column].dropna().unique())
        selected_vals = st.multiselect("Select values", values)
        if selected_vals:
            formatted_vals = ", ".join(map(str, selected_vals))
            condition = f"`{selected_column}` in [{formatted_vals}]"

    elif df[selected_column].dropna().isin([True, False]).all():
        val = st.selectbox("Choose value", df[selected_column].dropna().unique())
        condition = f"`{selected_column}` == {val}"

    else:
        st.warning("Unsupported column type.")

    # if condition and st.button("Apply Filter"):
    #     apply_filter(df, condition, case_col)
    #
    # if st.session_state.get("show_dashboard", False):
    #     show_dashboard(st.session_state["result_set"], st.session_state["complement_set"])
    #
    # if st.button("Show Dashboard"):
    #     st.session_state.show_dashboard = True
    #     st.rerun()

    if condition:
        if condition != previous_condition:
            st.session_state["filter_applied"] = False
            st.session_state["last_filter_condition"] = condition

        if st.button("Apply Filter", type="primary"):
            apply_filter(df, condition, case_col)
            st.session_state["filter_applied"] = True

    if st.session_state.get("filter_applied", False) and \
            st.session_state.get("result_set") is not None and \
            st.session_state.get("complement_set") is not None:
        show_dashboard(st.session_state["result_set"], st.session_state["complement_set"])

    if st.button("Back", type="secondary", key="Back_to_mapping"):
        st.switch_page("pages/2_Mapping.py")
case_filter_ui()
