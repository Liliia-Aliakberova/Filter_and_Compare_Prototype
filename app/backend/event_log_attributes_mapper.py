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

