import pandas as pd


def filter_cases_by_condition(df, condition, case_column):
    if not condition or case_column not in df.columns:
        return df.copy(), df.iloc[0:0]

    try:
        matching_rows = df.query(condition)
        matching_case_ids = matching_rows[case_column].unique()

        result_set = df[df[case_column].isin(matching_case_ids)]
        complement_set = df[~df[case_column].isin(matching_case_ids)]

        return result_set, complement_set

    except Exception as e:
        raise ValueError(f"Invalid condition: {e}")


def get_activity_distributions(event_log, result_set, complement_set, case_col, activity_col):
    result_ids = result_set[case_col]
    complement_ids = complement_set[case_col]

    result_events = event_log[event_log[case_col].isin(result_ids)]
    complement_events = event_log[event_log[case_col].isin(complement_ids)]

    result_activities = (
        result_events[[case_col, activity_col]]
        .drop_duplicates()
        .groupby(activity_col)[case_col]
        .nunique()
    )

    complement_activities = (
        complement_events[[case_col, activity_col]]
        .drop_duplicates()
        .groupby(activity_col)[case_col]
        .nunique()
    )

    return result_activities, complement_activities

def get_numeric_attributes_distribution_initial_state(df, case_col, timestamp_col, numeric_col):
    df = df.dropna(subset=[numeric_col])
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)

    sorted_df = df.sort_values(by=[case_col, timestamp_col])
    first_values = sorted_df.groupby(case_col).first().reset_index()

    return first_values


def get_numeric_attributes_distribution_last_state(df, case_col, timestamp_col, numeric_col):
    df = df.dropna(subset=[numeric_col])
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)

    sorted_df = df.sort_values(by=[case_col, timestamp_col])
    last_values = sorted_df.groupby(case_col).last().reset_index()

    return last_values
