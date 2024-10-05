import streamlit as st
import pandas as pd

# Step 1: Load the CSV files from the GitHub repository with the specified encoding
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

# New columns based on your provided information
bi_columns = [
    'Sector',
    'Dimension/ Learning Area',
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

programmes_columns = [
    'Programme',
    'Entry Type (New/ Recurring)',
    'Sector',
    'Dimension',
    'Learning Area',
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
    'Operation Support Officer [OSO]',
    'Application Basis (Sign up/ Nomination)',
    'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
    'E-learning link',
    'Estimated Month of Programme',
    'Remarks'
]

# Step 2: Create a single set of checkboxes in the sidebar for role selection (initially unticked)
st.sidebar.header("Select Roles to Display")
selected_columns = []

# Role names derived from the hardcoded columns
role_columns_full = {
    'Vice Principal (Admin) [VP(A)]': 'Vice Principal (Admin) [VP(A)]',
    'Adminstrative Manager [AM]': 'Adminstrative Manager [AM]',
    'Operation Manager [OM]': 'Operation Manager [OM]',
    'Assistant Operation Manager/SLT [Assistant OM/SLT]': 'Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'ICT Manager': 'ICT Manager',
    'Cluster ICT Manager': 'Cluster ICT Manager',
    'STEM Instructor (Workshop)': 'STEM Instructor (Workshop)',
    'STEM Instructor (Laboratory)': 'STEM Instructor (Laboratory)',
    'Corporate Support Officer [CSO]': 'Corporate Support Officer [CSO]',
    'Admin Executive [AE]': 'Admin Executive [AE]',
    'Technical Support Officer (Audio Visual) [TSO (AV)]': 'Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Operation Support Officer [OSO]': 'Operation Support Officer [OSO]'
}

for full_column, simple_column in role_columns_full.items():
    if st.sidebar.checkbox(simple_column, value=False):
        selected_columns.append(full_column)

# Step 3: If no roles are selected, display a warning
if not selected_columns:
    st.warning("Please select at least one role to display.")
else:
    # Create multi-index for Behavioural Indicators DataFrame
    bi_columns_with_headers = pd.MultiIndex.from_tuples(
        [('Sector', ''), ('Dimension/ Learning Area', '')] + 
        [(col, 'Behavioural Indicator') for col in selected_columns]
    )
    
    # Filter the Behavioural Indicators DataFrame
    filtered_bi_df = bi_df[['Sector', 'Dimension/ Learning Area'] + selected_columns]
    filtered_bi_df.columns = bi_columns_with_headers

    # Display the filtered Behavioural Indicators DataFrame with multi-index headers
    st.write("### Filtered Behavioural Indicators Data")
    st.dataframe(filtered_bi_df)

    # Create multi-index for Programmes DataFrame
    programmes_columns_with_headers = pd.MultiIndex.from_tuples(
        [('Programme', ''), ('Entry Type (New/ Recurring)', ''), ('Sector', ''), ('Dimension', ''), ('Learning Area', '')] +
        [(col, 'Type of Courses') for col in selected_columns] +
        [('Application Basis (Sign up/ Nomination)', ''), 
         ('Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)', ''),
         ('E-learning link', ''), 
         ('Estimated Month of Programme', ''), 
         ('Remarks', '')]
    )

    # Filter the Programmes DataFrame
    filtered_programmes_df = programmes_df[['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + selected_columns +
                                             ['Application Basis (Sign up/ Nomination)', 'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)', 
                                              'E-learning link', 'Estimated Month of Programme', 'Remarks']]
    filtered_programmes_df.columns = programmes_columns_with_headers

    # Display the filtered Programmes DataFrame with multi-index headers
    st.write("### Filtered Programmes Data")
    st.dataframe(filtered_programmes_df)