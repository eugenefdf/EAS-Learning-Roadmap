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
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

# Clean the DataFrames
programmes_df = clean_dataframe(programmes_df)
bi_df = clean_dataframe(bi_df)

# Function to clean up CSV text values
def clean_text(text):
    text = text.encode('latin1', 'replace').decode('utf-8', 'ignore')
    text = text.replace('�', '')  
    text = text.replace('?', '')   
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
unique_sectors = bi_df['Sector'].unique()
unique_sectors = ['Select All Sectors'] + unique_sectors.tolist()  
selected_sector = st.selectbox("Select Sector", options=unique_sectors)

# Filter Dimension/Learning Area based on the selected Sector
filtered_dimension = bi_df[bi_df['Sector'] == selected_sector.replace("Select All Sectors", "")]['Dimension/ Learning Area'].unique()
filtered_dimension = ['Select All Dimension/Learning Areas'] + filtered_dimension.tolist()  
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

    # Filter and structure the Behavioural Indicators DataFrame
    bi_columns = ['Sector', 'Dimension/ Learning Area'] + selected_columns
    filtered_bi_df = bi_df[(bi_df['Sector'] == selected_sector.replace("Select All Sectors", "")) & 
                            (bi_df['Dimension/ Learning Area'] == selected_dimension.replace("Select All Dimension/Learning Areas", ""))][bi_columns]

    # Display the filtered Behavioural Indicators in a scrollable format
    if not filtered_bi_df.empty:
        with st.expander("Click to display Behavioural Indicators"):
            st.write("### Behavioural Indicators")
            for col in selected_columns:
                bi_column_text = filtered_bi_df[col].dropna().apply(clean_text).tolist()  
                bi_column_text = "\n\n".join(bi_column_text)  

                if not bi_column_text.strip():  
                    bi_column_text = "No data available for this role."

                role_header = f"**{col}:**"
                st.markdown(role_header)  
                st.markdown(f"<div style='max-height: 200px; overflow-y: auto; white-space: pre-wrap;'>{bi_column_text}</div><br>", unsafe_allow_html=True)  
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

    min_month_abbr = month_abbreviations[min_month_index - 1]  
    max_month_abbr = month_abbreviations[max_month_index - 1]  

    st.write(f"Selected month range: {min_month_abbr} to {max_month_abbr}")

    # Function to check if any month in the list falls within the selected range
    def is_month_in_range(months, min_index, max_index, month_map):
        if "All year round" in months:
            return True
        month_indices = [month_map[month.strip()] for month in months if month.strip() in month_map]
        return any(min_index <= index <= max_index for index in month_indices)

    # Filter based on the selected month range
    filtered_programmes_df = filtered_programmes_df[
        filtered_programmes_df['Estimated Month of Programme'].apply(lambda x: is_month_in_range(x.split(','), min_month_index, max_month_index, month_map))
    ]

    # Filter based on the selected course type
    if selected_course_type != "Select All Courses":
        course_mask = filtered_programmes_df[selected_columns].isin([selected_course_type]).any(axis=1)
        filtered_programmes_df = filtered_programmes_df[course_mask]

    # Filter based on the selected roles, only if any role is selected
    if selected_columns:
        role_mask = filtered_programmes_df[selected_columns].notna().any(axis=1)
        filtered_programmes_df = filtered_programmes_df[role_mask]

    # Display the filtered Programmes DataFrame
    if not filtered_programmes_df.empty:
        st.write("### Available Programmes")
        st.dataframe(filtered_programmes_df[programmes_columns])
    else:
        st.warning("No Programmes found matching the filter query.")