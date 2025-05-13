import pandas as pd
import streamlit as st
import pm4py
import tempfile

def handle_csv_upload(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Could not read CSV file: {e}")
        return None


def handle_xes_upload(file):
    try:
        with tempfile.NamedTemporaryFile(suffix=".xes", delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        log = pm4py.read_xes(tmp_path)
        df = pm4py.convert_to_dataframe(log)

        return df

    except Exception as e:
        st.error(f"Could not read XES file: {e}")
        return None

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = handle_csv_upload(uploaded_file)
        elif uploaded_file.name.endswith(".xes"):
            df = handle_xes_upload(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        if df is not None:
            st.session_state["df"] = df
            st.session_state["uploaded_filename"] = uploaded_file.name
            st.session_state.pop("column_mapping", None)
            st.success(f"File {uploaded_file.name} uploaded successfully!")
            st.dataframe(df)