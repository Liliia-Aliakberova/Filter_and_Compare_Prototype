import streamlit as st
from app.backend.file_upload_handler import process_uploaded_file

#st.subheader("Upload Event Log File")

# Set a flag to detect if it's the first time the user visits the upload page
if "visited_upload" not in st.session_state:
    st.session_state["visited_upload"] = True
    first_time = True
else:
    first_time = False

# Handle file upload
uploaded_file = st.file_uploader("Upload an event log file in CSV or XES formats", type=["csv", "xes"],
                                 accept_multiple_files=False)

# Only clear session state if:
# 1. No file is uploaded
# 2. It's the first time on this page
# 3. The file was explicitly deleted by the user (by checking uploaded_file is None)
if uploaded_file is None and first_time:
    st.session_state.pop("df", None)
    st.session_state.pop("uploaded_filename", None)

# If a new file is uploaded and it's different from the one in session state
if uploaded_file and uploaded_file.name != st.session_state.get("uploaded_filename"):
    with st.spinner("Processing file..."):
        process_uploaded_file(uploaded_file)

# Show previously uploaded file info if available and user has visited the page before
elif "df" in st.session_state:
    st.info(f"Using previously uploaded file: {st.session_state.uploaded_filename}. "
            f"To use different log upload a new file")
    st.dataframe(st.session_state["df"].head(5))

# Show the "Next" button after the file is uploaded or loaded from session state
if "df" in st.session_state:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("Next", type="primary", key="Next_to_mapping"):
            st.session_state["navigate_to_mapping"] = "pages/2_Mapping.py"
            st.rerun()

# Handle navigation to the next page (Mapping)
if "navigate_to_mapping" in st.session_state:
    st.switch_page(st.session_state.pop("navigate_to_mapping"))
