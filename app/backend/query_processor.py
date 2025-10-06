import pandas as pd


def filter_cases_by_condition(df, condition, case_column):
    """
        Filters an event log based on a condition applied to its rows, and returns
        two sets: matching cases (result set) and the remaining cases (complement).

        Parameters:
        - df (pd.DataFrame): The event log DataFrame.
        - condition (str): A query string compatible with pandas' `.query()` method.
        - case_column (str): The name of the column representing case IDs.

        Returns:
        - result_set (pd.DataFrame): Rows belonging to cases that match the condition.
        - complement_set (pd.DataFrame): Rows belonging to cases that do not match the condition.

        Raises:
        - ValueError: If the condition string is invalid.
        """
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
    """
        Computes the distribution of unique cases per activity for two subsets of an event log.

        Parameters:
        - event_log (pd.DataFrame): The complete event log DataFrame.
        - result_set (pd.DataFrame): Subset of the log containing filtered cases.
        - complement_set (pd.DataFrame): Subset of the log with the remaining cases.
        - case_col (str): The name of the column representing case IDs.
        - activity_col (str): The name of the column representing activity names.

        Returns:
        - result_activities (pd.Series): Count of unique cases per activity in the result set.
        - complement_activities (pd.Series): Count of unique cases per activity in the complement set.
        """
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
    """
        Extracts the first observed value of a numeric attribute for each case based on timestamp order.
        This is done to be able to visualize distribution of the first values (states) of numeric attributes
        to compare result set case values and complement set cases

        Parameters:
        - df (pd.DataFrame): The event log DataFrame.
        - case_col (str): Column name representing case IDs.
        - timestamp_col (str): Column name representing timestamps.
        - numeric_col (str): Column name for the numeric attribute.

        Returns:
        - pd.DataFrame: DataFrame containing the first observed value of a numeric attribute for each case.
        """
    df = df.dropna(subset=[numeric_col])
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)

    sorted_df = df.sort_values(by=[case_col, timestamp_col])
    first_values = sorted_df.groupby(case_col).first().reset_index()

    return first_values


def get_numeric_attributes_distribution_last_state(df, case_col, timestamp_col, numeric_col):
    """
            Extracts the last observed value (last state) of a numeric attribute for each case based on timestamp order.
            This is done to be able to visualize distribution of the latest values (states) of numeric attributes
            to compare result set case values and complement set cases

            Parameters:
            - df (pd.DataFrame): The event log DataFrame.
            - case_col (str): Column name representing case IDs.
            - timestamp_col (str): Column name representing timestamps.
            - numeric_col (str): Column name for the numeric attribute.

            Returns:
            - pd.DataFrame: DataFrame containing the last observed value of a numeric attribute for each case.
            """
    df = df.dropna(subset=[numeric_col])
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)

    sorted_df = df.sort_values(by=[case_col, timestamp_col])
    last_values = sorted_df.groupby(case_col).last().reset_index()

    return last_values
