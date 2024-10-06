import streamlit as st
import pandas as pd
import json
import requests

# Load the configuration JSON file from GitHub
config_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/eas_learning_roadmap_config.json"
config_data = requests.get(config_url).json()

# Load the CSV files
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

# Function to clean up DataFrame by stripping whitespace from all string columns
def clean_dataframe(df):
    # Strip whitespace from all string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

# Clean the DataFrames
programmes_df = clean_dataframe(programmes_df)
bi_df = clean_dataframe(bi_df)

# Function to clean up CSV text values
def clean_text(text):
    # Replace unwanted characters and decode if necessary
    text = text.encode('latin1', 'replace').decode('utf-8', 'ignore')
    text = text.replace('�', '')  # Remove replacement character if present
    text = text.replace('?', '')   # Remove question marks
    return text.strip()

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
for full_column in config_data['roles']:
    if st.sidebar.checkbox(full_column, value=False):
        selected_columns.append(full_column)

# Filter for Course Types
course_types = ['Select All Courses', 'Mandatory', 'Essential', 'Optional']
selected_course_type = st.selectbox("Select Type of Courses", options=course_types)

# Display explanation for course types
st.markdown("""### Type of Courses
- **Mandatory:** Programmes that officers in the job role must attend, based on broad policy or a statutory requirement.
- **Essential:** Programmes that are key to helping officers perform their core work functions.
- **Optional (Good to Have):** Programmes that will help officers deepen their skills and knowledge in the functional competency.
""")

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

    # Retain all columns except for role-specific ones initially
    role_columns = [
        'Type of Course - Vice Principal (Admin) [VP(A)]', 
        'Type of Course - Administrative Manager [AM]', 
        'Type of Course - Operation Manager [OM]', 
        'Type of Course - Assistant Operation Manager/SLT [Assistant OM/SLT]', 
        'Type of Course - ICT Manager', 
        'Type of Course - Cluster ICT Manager', 
        'Type of Course - STEM Instructor (Workshop)', 
        'Type of Course - STEM Instructor (Laboratory)', 
        'Type of Course - Corporate Support Officer [CSO]', 
        'Type of Course - Admin Executive [AE]', 
        'Type of Course - Technical Support Officer (Audio Visual) [TSO (AV)]', 
        'Type of Course - Operation Support Officer [OSO]'
    ]
    
    # Create a boolean mask for filtering
    mask = pd.Series([True] * len(filtered_programmes_df))  # Start with all True

    # Check each role column; if the role is selected, check for None values
    for role in selected_columns:
        if role in role_columns:
            mask &= filtered_programmes_df[role].notnull()  # Keep rows where the role is not None

    # Apply the mask to filter the DataFrame
    filtered_programmes_df = filtered_programmes_df[mask]

    # Month mapping and abbreviations
    month_map = config_data['months']
    month_abbreviations = config_data['month_abbreviations']

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

    # Filter based on the selected course type
    if selected_course_type != "Select All Courses":
        # Filter for all relevant columns based on selected course type
        filtered_programmes_df = filtered_programmes_df[
            (filtered_programmes_df[role_columns].eq(selected_course_type).any(axis=1))
        ]

    # Display the filtered Programmes DataFrame
    if not filtered_programmes_df.empty:
        st.write("### Available Programmes")
        programmes_columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + selected_columns + [
            'Application Basis (Sign up/ Nomination)',
            'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
            'E-learning link',
            'Estimated Month of Programme',
            'Remarks'
        ]
        st.dataframe(filtered_programmes_df[programmes_columns])  # Ensure all relevant columns are displayed
    else:
        st.warning("No Programmes found matching the filter query.")