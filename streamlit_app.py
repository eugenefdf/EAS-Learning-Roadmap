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
# Get unique sectors from the DataFrame and add "Select All" option
unique_sectors = ["Select All Sectors"] + bi_df['Sector'].unique().tolist()
selected_sector = st.selectbox("Select Sector", options=unique_sectors)

# Filter Dimension/Learning Area based on the selected Sector
if selected_sector == "Select All Sectors":
    filtered_dimension = ["Select All Dimension/Learning Areas"] + bi_df['Dimension/ Learning Area'].unique().tolist()
else:
    filtered_dimension = ["Select All Dimension/Learning Areas"] + bi_df[bi_df['Sector'] == selected_sector]['Dimension/ Learning Area'].unique().tolist()

selected_dimension = st.selectbox("Select Dimension/Learning Area", options=filtered_dimension)

# Sidebar for role selection
st.sidebar.header("Select Roles to Display")
selected_columns = []
for full_column in role_columns:
    if st.sidebar.checkbox(full_column, value=False):
        selected_columns.append(full_column)

# Filter Behavioural Indicators DataFrame based on Sector and Dimension/Learning Area
if selected_sector == "Select All Sectors":
    filtered_bi_df = bi_df.copy()  # No sector filtering
else:
    filtered_bi_df = bi_df[bi_df['Sector'] == selected_sector]

if selected_dimension != "Select All Dimension/Learning Areas":
    filtered_bi_df = filtered_bi_df[filtered_bi_df['Dimension/ Learning Area'] == selected_dimension]

# Filter the Programmes DataFrame based on Sector and Dimension filters
if selected_sector == "Select All Sectors":
    filtered_programmes_df = programmes_df.copy()
else:
    filtered_programmes_df = programmes_df[programmes_df['Sector'] == selected_sector]

if selected_dimension != "Select All Dimension/Learning Areas":
    filtered_programmes_df = filtered_programmes_df[filtered_programmes_df['Dimension'] == selected_dimension]

# Display the filtered Behavioural Indicators in a scrollable format using text_area within an expander
if not filtered_bi_df.empty:
    with st.expander("Click to display Behavioural Indicators"):
        st.write("### Behavioural Indicators")
        for col in selected_columns:
            # Extract the text for the current role column
            bi_column_text = filtered_bi_df[col].dropna().to_string(index=False)
            if not bi_column_text.strip():  # Check if the text is empty
                bi_column_text = "No data available for this role."
            
            # Use st.text_area for long text with scrolling, ensuring height is set for scrolling
            st.text_area(f"**{col}:**", value=bi_column_text.replace("\n", " "), height=300, key=col, max_chars=None)
else:
    st.warning("No Behavioural Indicators found for the selected filters.")

# Programmes DataFrame columns for display
programmes_columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + selected_columns + [
    'Application Basis (Sign up/ Nomination)',
    'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
    'E-learning link',
    'Estimated Month of Programme',
    'Remarks'
]

# Function to filter Programmes DataFrame based on a query
def filter_dataframe(df, query):
    query = query.lower()
    return df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]

# Add a text input for filtering the Programmes DataFrame
filter_query = st.text_input("Filter Programmes Data by any keyword", "")

# Apply the filter function to the Programmes DataFrame if there is a query
if filter_query:
    filtered_programmes_df = filter_dataframe(filtered_programmes_df[programmes_columns], filter_query)
else:
    filtered_programmes_df = filtered_programmes_df[programmes_columns]

# Display the filtered Programmes DataFrame
if not filtered_programmes_df.empty:
    st.write("### Filtered Programmes Data")
    st.dataframe(filtered_programmes_df)
else:
    st.warning("No Programmes found matching the filter query.")