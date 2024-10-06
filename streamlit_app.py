# Check if "Select All" is selected for Sector or Dimension
if selected_sector == "Select All Sectors" or selected_dimension == "Select All Dimension/Learning Areas":
    st.warning("Please specify a Sector and Dimension/Learning Area instead.")
else:
    # Filter and structure the Behavioural Indicators DataFrame
    bi_columns = ['Sector', 'Dimension/ Learning Area'] + selected_columns
    filtered_bi_df = bi_df[(bi_df['Sector'] == selected_sector.replace("Select All Sectors", "")) & 
                            (bi_df['Dimension/ Learning Area'] == selected_dimension.replace("Select All Dimension/Learning Areas", ""))][bi_columns]

    # Display the filtered Behavioural Indicators in a scrollable format
    if not filtered_bi_df.empty:
        with st.expander("Click to display Behavioural Indicators"):
            st.write("### Behavioural Indicators")
            for col in selected_columns:
                bi_column_text = filtered_bi_df[col].dropna().to_string(index=False)
                if not bi_column_text.strip():
                    bi_column_text = "No data available for this role."
                bi_column_text = bi_column_text.replace("\n", " \n")
                st.markdown(f"**{col}:**")
                st.markdown(f"<div style='max-height: 200px; overflow-y: auto; white-space: pre-wrap;'>{bi_column_text}</div>", unsafe_allow_html=True)
    else:
        st.warning("No Behavioural Indicators found for the selected filters.")

    # Create columns for Programmes DataFrame
    programmes_columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + selected_columns + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]

    # Filter the Programmes DataFrame based on the selected Sector and Dimension/Learning Area
    filtered_programmes_df = programmes_df[
        (programmes_df['Sector'] == selected_sector.replace("Select All Sectors", "")) &
        (programmes_df['Dimension'] == selected_dimension.replace("Select All Dimension/Learning Areas", ""))
    ]

    # Month mapping and filtering by month range
    filtered_programmes_df['Month_Number'] = filtered_programmes_df['Estimated Month of Programme'].map(month_map)
    filtered_programmes_df = filtered_programmes_df[
        (filtered_programmes_df['Month_Number'] >= min_month) & (filtered_programmes_df['Month_Number'] <= max_month)
    ]

    # Add a text input for filtering the Programmes DataFrame
    filter_query = st.text_input("Filter Programmes Table by any keyword", "")
    
    # Apply the filter function to the Programmes DataFrame if there is a query
    filtered_programmes_df = filtered_programmes_df[programmes_columns]
    
    if filter_query:
        filtered_programmes_df = filter_dataframe(filtered_programmes_df, filter_query)

    # Display the filtered Programmes DataFrame
    if not filtered_programmes_df.empty:
        st.write("### Available Programmes")
        st.dataframe(filtered_programmes_df)
    else:
        st.warning("No Programmes found matching the filter query.")