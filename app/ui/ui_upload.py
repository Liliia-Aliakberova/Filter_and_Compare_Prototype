# import streamlit as st
# from app.backend.file_upload_handler import handle_csv_upload, handle_xes_upload
#
# def file_upload_ui():
#     st.header("Upload Event Log File")
#     uploaded_file = st.file_uploader("Upload an event log file in CSV or XES formats", type=["csv", "xes"])
#
#     # Clear session state if file is removed
#     if uploaded_file is None:
#         st.session_state.pop("df", None)
#         st.session_state.pop("uploaded_filename", None)
#         return
#
#     if uploaded_file.name != st.session_state.get("uploaded_filename"):
#         with st.spinner("Processing file..."):
#             if uploaded_file.name.endswith(".csv"):
#                 df = handle_csv_upload(uploaded_file)
#             elif uploaded_file.name.endswith(".xes"):
#                 df = handle_xes_upload(uploaded_file)
#             else:
#                 st.error("Unsupported file type.")
#                 return
#
#         if df is not None:
#             st.session_state["df"] = df
#             st.session_state["uploaded_filename"] = uploaded_file.name
#             st.success(f"File {uploaded_file.name} uploaded successfully!")
#             st.dataframe(df)
#
#
#     elif "df" in st.session_state:
#         #st.info(f"Using previously uploaded file: {st.session_state.uploaded_filename}")
#         st.info(f"Using previously uploaded file: {st.session_state.uploaded_filename}")
#         st.dataframe(st.session_state["df"].head())
#
#     if "df" in st.session_state:
#         col1, col2, col3 = st.columns([1, 6, 1])
#
#         with col3:
#             st.button("Next", on_click=lambda: st.session_state.update({"page": "mapping"}),
#                       type="primary")

# import streamlit as st
# from app.backend.file_upload_handler import handle_csv_upload, handle_xes_upload
#
#
# def file_upload_ui():
#     st.header("Upload Event Log File")
#
#     # Check if there's already an uploaded file in the session state
#     if "df" in st.session_state:
#         st.info(f"Using previously uploaded file: {st.session_state.uploaded_filename}")
#         st.dataframe(st.session_state["df"].head())
#         st.button("Next", on_click=lambda: st.session_state.update({"page": "mapping"}), type="primary")# Show the first few rows of the uploaded file
#
#     # If the file is removed, clear the session state
#     uploaded_file = st.file_uploader("Upload an event log file in CSV or XES formats", type=["csv", "xes"])
#
#     # If no file is uploaded, remove any file stored in session state
#     if uploaded_file is None:
#         if "df" in st.session_state:
#             st.session_state.pop("df", None)
#             st.session_state.pop("uploaded_filename", None)
#         return  # Stop further processing if no file is uploaded
#
#     # If the uploaded file is different from the one stored in session state, process it
#     if uploaded_file.name != st.session_state.get("uploaded_filename"):
#         with st.spinner("Processing file..."):
#             # Handle CSV and XES files separately
#             if uploaded_file.name.endswith(".csv"):
#                 df = handle_csv_upload(uploaded_file)
#             elif uploaded_file.name.endswith(".xes"):
#                 df = handle_xes_upload(uploaded_file)
#             else:
#                 st.error("Unsupported file type.")
#                 return  # Exit if the file type is not supported
#
#         # Save the processed DataFrame and filename to session state
#         if df is not None:
#             st.session_state["df"] = df
#             st.session_state["uploaded_filename"] = uploaded_file.name
#             st.success(f"File {uploaded_file.name} uploaded successfully!")
#             st.dataframe(df)
#
#     # Show the "Next" button to go to the column mapping page if a file is uploaded
#     if "df" in st.session_state:
#         col1, col2, col3 = st.columns([1, 6, 1])
#
#         with col3:
#             st.button("Next", on_click=lambda: st.session_state.update({"page": "mapping"}), type="primary")

import streamlit as st
from app.backend.file_upload_handler import handle_csv_upload, handle_xes_upload

def file_upload_ui():
    st.header("Upload Event Log File")

    # Check if there's already an uploaded file in the session state
    if "df" in st.session_state:
        st.info(f"Using previously uploaded file: {st.session_state.uploaded_filename}")
        st.dataframe(st.session_state["df"].head())  # Show the first few rows of the uploaded file


    # File upload input for new files
    uploaded_file = st.file_uploader("Upload an event log file in CSV or XES formats", type=["csv", "xes"])

    # If no file is uploaded, remove any file from session state
    if uploaded_file is None:
        if "df" in st.session_state:
            st.session_state.pop("df", None)
            st.session_state.pop("uploaded_filename", None)
        return  # Exit if no file is uploaded

    # If the uploaded file is different from the one stored in session state, process it
    if uploaded_file.name != st.session_state.get("uploaded_filename"):
        with st.spinner("Processing file..."):
            # Handle CSV and XES files separately
            if uploaded_file.name.endswith(".csv"):
                df = handle_csv_upload(uploaded_file)
            elif uploaded_file.name.endswith(".xes"):
                df = handle_xes_upload(uploaded_file)
            else:
                st.error("Unsupported file type.")
                return  # Exit if the file type is not supported

        # Save the processed DataFrame and filename to session state
        if df is not None:
            st.session_state["df"] = df
            st.session_state["uploaded_filename"] = uploaded_file.name
            st.success(f"File {uploaded_file.name} uploaded successfully!")
            st.dataframe(df)

            # Show the "Next" button after file is uploaded
            col1, col2, col3 = st.columns([1, 6, 1])
            with col3:
                st.button("Next", on_click=lambda: st.session_state.update({"page": "mapping"}), key="next_button")

