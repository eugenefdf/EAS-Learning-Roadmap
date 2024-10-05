import streamlit as st
import pandas as pd

# Load the CSV files
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

# Define the role columns
role_columns = [
    'Vice Principal (Admin) [VP(A)]',
    'Adminstrative Manager [AM]',
    'Operation Manager [OM]',
    'Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'ICT Manager',
    'Cluster ICT Manager',
    'STEM Instructor (Workshop)',
    'STEM Instructor (Laboratory)',
    'Corporate Support Officer [CSO]',
    'Admin Executive [AE]',
    'Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Operation Support Officer [OSO]'
]

# Set the title of the app
st.title("SAT Learning Roadmap")

# Create filters for Sector and Dimension/Learning Area below the title
# Get unique sectors from the DataFrame
unique_sectors = bi_df['Sector'].unique()
selected_sector = st.selectbox("Select Sector", options=unique_sectors)

# Filter Dimension/Learning Area based on the selected Sector
filtered_dimension = bi_df[bi_df['Sector'] == selected_sector]['Dimension/ Learning Area'].unique()
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
    # Filter and structure the Behavioural Indicators DataFrame
    bi_columns = ['Sector', 'Dimension/ Learning Area'] + selected_columns
    filtered_bi_df = bi_df[(bi_df['Sector'] == selected_sector) & (bi_df['Dimension/ Learning Area'] == selected_dimension)][bi_columns]

    # Display the filtered Behavioural Indicators in a text area
    if not filtered_bi_df.empty:
        # Assuming the first selected column is the Behavioural Indicator
        bi_texts = []
        for col in selected_columns:
            bi_column_text = filtered_bi_df[col].dropna().to_string(index=False)
            bi_texts.append(f"**{col}:**\n{bi_column_text}\n")

        # Use a text area for the Behavioural Indicators text area
        st.text_area("Behavioural Indicators", value="\n".join(bi_texts), height=300, key="bi_text_area")  # Default height for scrolling
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

    # Filter and structure the Programmes DataFrame
    filtered_programmes_df = programmes_df[programmes_columns]

    # Display the filtered Programmes DataFrame
    st.write("### Filtered Programmes Data")
    st.dataframe(filtered_programmes_df)