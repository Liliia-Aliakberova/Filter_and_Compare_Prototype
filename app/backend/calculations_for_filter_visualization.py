def calculate_case_duration(df, case_col, timestamp_col):
    """
        Calculation of cases durations

        Parameters:
        - df: The DataFrame containing the event log.
        - case_col: Selected column for Case ID.
        - timestamp_col: Selected column for Timestamp.(for the current implementation one timestamp)

        Returns:
        - column with duration of cases.
        """
    #duration = (latest timestamp - first timestamp)
    case_durations = df.groupby(case_col).agg(
        first_event_timestamp=(timestamp_col, 'min'),
        last_event_timestamp=(timestamp_col, 'max')
    ).reset_index()

    #duration in hours
    case_durations['duration'] = (case_durations['last_event_timestamp'] - case_durations['first_event_timestamp']).dt.total_seconds() / 3600  # Convert seconds to hours

    return case_durations
