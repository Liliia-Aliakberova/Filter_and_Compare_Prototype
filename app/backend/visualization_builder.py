# import pandas as pd
# import plotly.express as px
#
# def get_exclusive_activities(result_set, complement_set, activity_col):
#     result_activities = set(result_set[activity_col].unique())
#     complement_activities = set(complement_set[activity_col].unique())
#
#     result_exclusive = result_activities - complement_activities
#     complement_exclusive = complement_activities - result_activities
#
#     return result_exclusive, complement_exclusive
#
#
# def plot_attribute_distribution(attribute, result_set, complement_set):
#     fig, fig2 = None, None
#
#     # Numeric attribute distribution visualization
#     if pd.api.types.is_numeric_dtype(result_set[attribute]):
#         fig = px.histogram(result_set, x=attribute, title=f"Distribution of {attribute} in Result Set")
#         fig.update_layout(title=f"Distribution of {attribute} in Result Set")
#         fig2 = px.histogram(complement_set, x=attribute, title=f"Distribution of {attribute} in Complement Set")
#         fig2.update_layout(title=f"Distribution of {attribute} in Complement Set")
#
#     # Categorical attribute distribution visualization
#     elif pd.api.types.is_object_dtype(result_set[attribute]):
#         fig = px.bar(result_set[attribute].value_counts().reset_index(), x="index", y=attribute,
#                      title=f"Value Counts of {attribute} in Result Set")
#         fig2 = px.bar(complement_set[attribute].value_counts().reset_index(), x="index", y=attribute,
#                       title=f"Value Counts of {attribute} in Complement Set")
#
#     return fig, fig2

import altair as alt
import pandas as pd

def build_activity_distribution_chart(df):
    # Melt the DataFrame into long format
    subset_columns = [col for col in df.columns if col != 'Activity']

    df_long = df.melt(id_vars='Activity',
                      value_vars=subset_columns,
                      var_name='Subset',
                      value_name='Count')

    # Define color map for subsets
    color_map = {
        'Result Set': '#1f77b4',
        'Complement Set': '#ff7f0e',
        'Full Log': '#e6e6e6'
    }

    # Color scale for subsets
    color_scale = alt.Scale(
        domain=subset_columns,
        range=[color_map[s] for s in subset_columns]
    )

    # Define interactive multi-selection bound to legend
    # Allow only 2 selections
    selection = alt.selection_multi(fields=['Subset'], bind='legend', toggle='true')

    # Chart with condition to highlight only selected Subset values
    chart = alt.Chart(df_long).mark_bar().encode(
        x=alt.X('Activity:N',
                sort=alt.EncodingSortField(field='Activity', order='ascending'),
                axis=alt.Axis(labelAngle=-90)),
        y=alt.Y('Count:Q', title='Number of Cases'),
        color=alt.condition(selection,
                            alt.Color('Subset:N', scale=color_scale),
                            alt.value('lightgray')),  # Dim others that are not selected
        xOffset='Subset:N',
        tooltip=['Activity', 'Subset', 'Count']
    ).add_params(
        selection
    ).transform_filter(
            selection
    ).properties(
        #title="Activity Distribution (Select Two Subsets)",
        width='container'
    ).interactive()

    return chart

def build_numeric_distribution_chart(df, column, color, title, x_scale=None, y_scale=None):
    return alt.Chart(df).mark_bar().encode(
        alt.X(f'{column}:Q', scale=x_scale),
        alt.Y('count()', scale=y_scale),
        color=alt.value(color)
    ).properties(
        title=title
    ).interactive()


