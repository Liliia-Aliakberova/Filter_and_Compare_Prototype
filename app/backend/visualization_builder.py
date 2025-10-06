import altair as alt

def build_activity_distribution_chart(df):
    """
        Builds an interactive Altair bar chart showing activity distribution
        across different subsets of the event log (result set, complement set, full log)

        Parameters:
        - df: A DataFrame where each row is an activity and each column (except 'Activity')
        represents a subset with counts.

        Returns:
        - alt.Chart: An interactive Altair bar chart with subset selection.
        """
    subset_columns = [col for col in df.columns if col != 'Activity']

    df_long = df.melt(id_vars='Activity',
                      value_vars=subset_columns,
                      var_name='Subset',
                      value_name='Count')
    color_map = {
        'Result Set': '#1f77b4',
        'Complement Set': '#ff7f0e',
        'Full Log': '#e6e6e6'
    }

    color_scale = alt.Scale(
        domain=subset_columns,
        range=[color_map[s] for s in subset_columns]
    )
    selection = alt.selection_multi(fields=['Subset'], bind='legend', toggle='true')

    chart = (alt.Chart(df_long).mark_bar().encode(
        x=alt.X('Activity:N',
                sort=alt.EncodingSortField(field='Activity', order='ascending'),
                axis=alt.Axis(labelAngle=-90)),
        y=alt.Y('Count:Q', title='Number of Cases'),
        color=alt.condition(selection,
                            alt.Color('Subset:N', scale=color_scale),
                            alt.value('black')),
        xOffset='Subset:N',
        tooltip=['Activity', 'Subset', 'Count']
    ).add_params(
        selection
    ).transform_filter(
            selection
    ).configure_axis(
        labelColor='black',
        titleColor='black'
    ).configure_legend(
        labelColor='black',
        titleColor='black'
    ).configure_title(
        color='blackact'
    )
             .properties(
        #title="Activity Distribution (Select Two Subsets)",
        width='container'
    ).interactive())

    return chart

def build_combined_numeric_distribution_chart(df, column, x_scale=None, y_scale=None):
    """
            Builds an interactive Altair bar chart showing the distribution of a numeric
            attribute across different subsets of the event log (result set, complement set, full log).

            Parameters:
            - df: A DataFrame containing the numeric attribute,
            a 'Subset' column indicating group, and optional additional metadata.
            - x_scale (alt.Scale, optional): Custom X-axis scale (e.g., domain or type).
            - y_scale (alt.Scale, optional): Custom Y-axis scale.

            Returns:
            - alt.LayerChart: An interactive layered bar chart showing numeric distribution.
            """
    subset_columns = ['Full Log', 'Result Set', 'Complement Set']
    color_map = {
        'Full Log': '#e6e6e6',
        'Result Set': '#1f77b4',
        'Complement Set': '#ff7f0e'
    }

    case_counts = df.groupby('Subset')[column].count().reset_index()
    case_counts = case_counts.set_index('Subset')
    case_counts = case_counts.reindex(subset_columns)
    case_counts = case_counts.fillna(0)

    sorted_subsets = case_counts.sort_values(by=column, ascending=False).index.tolist()

    color_scale = alt.Scale(
        domain=sorted_subsets,
        range=[color_map[s] for s in sorted_subsets]
    )

    selection = alt.selection_multi(fields=['Subset'], bind='legend', toggle='true')

    layers = []

    for subset in sorted_subsets:
        subset_df = df[df['Subset'] == subset]
        opacity = 0.7 if subset != 'Full Log' else 0.5  # Slightly less opaque for Full Log

        layer = alt.Chart(subset_df).mark_bar(opacity=opacity).encode(
            x=alt.X(f'{column}:Q', scale=x_scale, title=column),  # No binning, just raw values
            y=alt.Y('count()', stack=None, scale=y_scale, title="Number of Cases"),
            color=alt.Color('Subset:N', scale=color_scale),
            xOffset='Subset:N',  # Offset to avoid overlap
            tooltip=[column, 'Subset', 'count()']
        ).add_params(
            selection
        ).transform_filter(
            selection
        )

        layers.append(layer)

    chart = alt.layer(*layers)

    chart = chart.properties(
        width='container',
        title=f"Distribution of '{column}' by Subset"
    ).interactive()

    return chart

def build_case_duration_chart(df):
    """
        Builds an interactive Altair chart showing the distribution of case durations
        across different subsets of the event log (result set, complement set, full log).

        Parameters:
        - df: A DataFrame with at least the columns 'duration' (numeric, in hours)
          and 'Subset' (categorical indicating group membership).

        Returns:
        - alt.LayerChart: An interactive layered bar chart visualizing case durations.
        """
    color_map = {
        'Full Log': '#e6e6e6',
        'Result Set': '#1f77b4',
        'Complement Set': '#ff7f0e'
    }

    selection = alt.selection_multi(fields=['Subset'], bind='legend', toggle='true')

    case_counts = df.groupby('Subset')['duration'].count().reset_index()
    case_counts = case_counts.set_index('Subset')
    case_counts = case_counts.reindex(['Full Log', 'Result Set', 'Complement Set'])
    case_counts = case_counts.fillna(0)

    sorted_subsets = case_counts.sort_values(by='duration', ascending=False).index.tolist()

    color_scale = alt.Scale(
        domain=sorted_subsets,
        range=[color_map[s] for s in sorted_subsets]
    )

    layers = []
    for subset in sorted_subsets:
        subset_df = df[df['Subset'] == subset]
        opacity = 0.7 if subset != 'Full Log' else 0.5

        layer = alt.Chart(subset_df).mark_bar(opacity=opacity).encode(
            x=alt.X('duration:Q', title="Duration (hours)", scale=alt.Scale(domain=[0, df['duration'].max()])),  # Raw values with no binning
            y=alt.Y('count():Q', title="Number of Cases"),
            color=alt.Color('Subset:N', scale=color_scale),
            tooltip=['duration:Q', 'count():Q', 'Subset:N']
        ).add_params(
            selection
        ).transform_filter(
            selection
        )

        layers.append(layer)

    chart = alt.layer(*layers)

    chart = chart.properties(
        width='container',
    ).interactive()

    return chart