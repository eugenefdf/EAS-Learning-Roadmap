import streamlit as st
import pandas as pd
import json

# Load the configuration data from the JSON file
with open('path/to/eas_learning_roadmap_config.json') as json_file:  # Adjust the path as needed
    config = json.load(json_file)

# Load the CSV files
programmes_df = pd.read_csv(config["programmes_url"], encoding='ISO-8859-1')
bi_df = pd.read_csv(config["bi_url"], encoding='ISO-8859-1')

# Define the role columns
role_columns = config["role_columns"]

# Set the title of the app
st.title("EAS Learning Roadmap")

# Introduction text
st.markdown(
    '<div class="intro-text" style="color: black; font-family: Lato; font-size: 18px;">As an MOE EAS officer, you manage a varied spectrum of work so that our schools and HQ divisions can operate effectively and efficiently.<br><br> \
    This requires you to be equipped with both core and functional competencies in order to perform your best at work and to thrive well in an increasingly complex operating environment.<br><br> \
    This Learning Roadmap focuses on learning provisions to equip you with the required functional competencies expected of SATs.<br><br> \
    For more info on Our Core Competencies (OCC), you may refer to the OCC Guide book and the SAT Competency Framework.<br><br> </div>',
    unsafe_allow_html=True
)

# Create filters for Sector and Dimension/Learning Area below the title
# Get unique sectors from the DataFrame
unique_sectors = bi_df['Sector'].unique()
unique_sectors = ['Select All Sectors'] + unique_sectors.tolist()  # Add "Select All" option
selected_sector = st.selectbox("Select Sector", options=unique_sectors)

# Filter Dimension/Learning Area based on the selected Sector
filtered_dimension = bi_df[bi_df['Sector'] == selected_sector.replace("Select All Sectors", "")]['Dimension/ Learning Area'].unique()
filtered_dimension = ['Select All Dimension/Learning Areas'] + filtered_dimension.tolist()  # Add "Select All" option
selected_dimension = st.selectbox("Select Dimension/Learning Area", options=filtered_dimension)

# Sidebar for role selection
st.sidebar.header("Select Roles to Display")
selected_columns = []
for full_column in role_columns:
    if st.sidebar.checkbox(full_column, value=False):
        selected_columns.append(full_column)

# Check if any roles are selected
if not selected_columns:
    st.warning("Please select at least one role to display.")
else:
    # Create a copy of the original programmes_df for filtering
    filtered_programmes_df = programmes_df.copy()

    # Check if "Select All" is selected for Sector or Dimension
    if selected_sector != "Select All Sectors":
        filtered_programmes_df = filtered_programmes_df[filtered_programmes_df['Sector'] == selected_sector.replace("Select All Sectors", "")]
    
    if selected_dimension != "Select All Dimension/Learning Areas":
        filtered_programmes_df = filtered_programmes_df[filtered_programmes_df['Dimension'] == selected_dimension.replace("Select All Dimension/Learning Areas", "")]

    # Filter and structure the Behavioural Indicators DataFrame
    bi_columns = ['Sector', 'Dimension/ Learning Area'] + selected_columns
    filtered_bi_df = bi_df[(bi_df['Sector'] == selected_sector.replace("Select All Sectors", "")) & 
                            (bi_df['Dimension/ Learning Area'] == selected_dimension.replace("Select All Dimension/Learning Areas", ""))][bi_columns]

    # Display the filtered Behavioural Indicators in a scrollable format
    if not filtered_bi_df.empty:
        with st.expander("Click to display Behavioural Indicators"):
            st.write("### Behavioural Indicators")
            for col in selected_columns:
                # Extract the text for the current role column
                bi_column_text = filtered_bi_df[col].dropna().to_string(index=False)
                if not bi_column_text.strip():  # Check if the text is empty
                    bi_column_text = "No data available for this role."
                    
                # Replace new lines for better readability
                bi_column_text = bi_column_text.replace("\n", " \n")

                # Use st.markdown for long text with scrolling
                st.markdown(f"**{col}:**")
                st.markdown(f"<div style='max-height: 200px; overflow-y: auto; white-space: pre-wrap;'>{bi_column_text}</div>", unsafe_allow_html=True)
    else:
        st.warning("Select a sector and dimension/learning area to display the Behavioural Indicator.")

    # Create columns for Programmes DataFrame
    programmes_columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + selected_columns + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]

    # Month mapping
    month_map = config["month_map"]

    # Create a list of month abbreviations
    month_abbreviations = config["month_abbreviations"]

    # Add a slider to filter the Programmes DataFrame by a range of months
    min_month_index, max_month_index = st.slider(
        "Select month range",
        1,
        12,
        (1, 12),
        format="%d"
    )

    # Convert the indices to month abbreviations for display
    min_month_abbr = month_abbreviations[min_month_index - 1]  # Adjust index for 0-based list
    max_month_abbr = month_abbreviations[max_month_index - 1]  # Adjust index for 0-based list

    # Display the selected month range as abbreviations
    st.write(f"Selected month range: {min_month_abbr} to {max_month_abbr}")

    # Convert text months to numeric values in the Programmes DataFrame for filtering
    filtered_programmes_df['Month_Number'] = filtered_programmes_df['Estimated Month of Programme'].map(month_map)

    # Filter based on the selected month range
    filtered_programmes_df = filtered_programmes_df[
        (filtered_programmes_df['Month_Number'] >= min_month_index) & 
        (filtered_programmes_df['Month_Number'] <= max_month_index)
    ]

    # Display the filtered Programmes DataFrame
    if not filtered_programmes_df.empty:
        st.write("### Available Programmes")
        st.dataframe(filtered_programmes_df[programmes_columns])
    else:
        st.warning("No Programmes found matching the filter query.")