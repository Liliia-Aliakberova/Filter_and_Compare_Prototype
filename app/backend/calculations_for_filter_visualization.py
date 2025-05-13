def calculate_case_duration(df, case_col, timestamp_col):
    # Group by case and calculate duration (last timestamp - first timestamp)
    case_durations = df.groupby(case_col).agg(
        first_event_timestamp=(timestamp_col, 'min'),
        last_event_timestamp=(timestamp_col, 'max')
    ).reset_index()

    # Calculate the duration in hours
    case_durations['duration'] = (case_durations['last_event_timestamp'] - case_durations['first_event_timestamp']).dt.total_seconds() / 3600  # Convert seconds to hours

    return case_durations
