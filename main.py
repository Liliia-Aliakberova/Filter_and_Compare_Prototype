# import streamlit as st
# from app.ui.ui_upload import file_upload_ui
# from app.ui.ui_mapping import column_mapping_ui
# from app.ui.ui_query_visualization import case_filter_ui
#
# st.set_page_config(page_title="Home", layout="wide")
#
# if "page" not in st.session_state:
#     st.session_state.page = "upload"
#
# st.title("Event Log Analyzer")
#
# if st.session_state.page == "upload":
#     file_upload_ui()
#
# elif st.session_state.page == "mapping":
#     if "df" not in st.session_state:
#         st.warning("Please upload a file first.")
#         st.button("Back to Upload", on_click=lambda: st.session_state.update({"page": "upload"}))
#     else:
#         column_mapping_ui()
#         st.button("Back", on_click=lambda: st.session_state.update({"page": "upload"}))
#
# elif st.session_state.page == "query_and_visualization":
#     case_filter_ui()
import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Event Log Analyzer", layout="wide")

# Title of the page
st.title("Event Log Analyzer")

# Navigation Links using st.page_link
#st.markdown("### Steps:")
pages = (
    st.Page("pages/1_Upload.py", title="Upload File"),
    st.Page("pages/2_Mapping.py", title="Map Columns"),
    st.Page("pages/3_Filter_Visualization.py", title="Filter and Visualize"),
    st.Page("pages/4_Data_Provenance.py", title="Data Provenance")
)

pg = st.navigation(pages)

pg.run()

