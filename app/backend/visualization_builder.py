import altair as alt

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

def build_combined_numeric_distribution_chart(df, column, x_scale=None, y_scale=None):
    # Define the color mapping for subsets
    subset_columns = ['Full Log', 'Result Set', 'Complement Set']
    color_map = {
        'Full Log': '#e6e6e6',  # Light grey for Full Log
        'Result Set': '#1f77b4',  # Blue for Result Set
        'Complement Set': '#ff7f0e'  # Orange for Complement Set
    }

    # Calculate the number of cases for each subset (Full Log, Result Set, Complement Set)
    case_counts = df.groupby('Subset')[column].count().reset_index()
    case_counts = case_counts.set_index('Subset')
    case_counts = case_counts.reindex(subset_columns)  # Ensure all subsets are included even if empty
    case_counts = case_counts.fillna(0)  # Fill any missing subset with 0 count

    # Sort subsets by the number of cases (ascending)
    sorted_subsets = case_counts.sort_values(by=column, ascending=False).index.tolist()

    # Create a color scale based on subsets
    color_scale = alt.Scale(
        domain=sorted_subsets,
        range=[color_map[s] for s in sorted_subsets]
    )

    # Define the selection to allow users to filter by Subset using the legend
    selection = alt.selection_multi(fields=['Subset'], bind='legend', toggle='true')

    # Create the layered chart
    layers = []

    # Iterate through subsets and create each layer
    for subset in sorted_subsets:
        subset_df = df[df['Subset'] == subset]
        opacity = 0.7 if subset != 'Full Log' else 0.5  # Slightly less opaque for Full Log

        # Create a bar layer for this subset
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

    # Combine all the layers (the subset with the most cases will be in the back)
    chart = alt.layer(*layers)

    # Set the chart properties
    chart = chart.properties(
        width='container',
        title=f"Distribution of '{column}' by Subset"
    ).interactive()

    return chart

def build_case_duration_chart(df):
    # Define color mapping for subsets
    color_map = {
        'Full Log': '#e6e6e6',  # Light grey for Full Log
        'Result Set': '#1f77b4',  # Blue for Result Set
        'Complement Set': '#ff7f0e'  # Orange for Complement Set
    }

    # Define the selection to allow users to filter by Subset using the legend
    selection = alt.selection_multi(fields=['Subset'], bind='legend', toggle='true')

    # Calculate the number of cases for each subset (Full Log, Result Set, Complement Set)
    case_counts = df.groupby('Subset')['duration'].count().reset_index()
    case_counts = case_counts.set_index('Subset')
    case_counts = case_counts.reindex(['Full Log', 'Result Set', 'Complement Set'])  # Ensure all subsets are included
    case_counts = case_counts.fillna(0)  # Fill any missing subset with 0 count

    # Sort subsets by the number of cases (ascending)
    sorted_subsets = case_counts.sort_values(by='duration', ascending=False).index.tolist()

    # Create a color scale based on subsets
    color_scale = alt.Scale(
        domain=sorted_subsets,
        range=[color_map[s] for s in sorted_subsets]
    )

    # Create the histogram chart with custom opacity and no binning (raw values)
    layers = []
    for subset in sorted_subsets:
        subset_df = df[df['Subset'] == subset]
        opacity = 0.7 if subset != 'Full Log' else 0.5  # Slightly less opaque for Full Log

        # Create a bar layer for this subset
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

    # Combine all the layers (the subset with the most cases will be in the back)
    chart = alt.layer(*layers)

    # Set the chart properties
    chart = chart.properties(
        width='container',
    ).interactive()

    return chart
