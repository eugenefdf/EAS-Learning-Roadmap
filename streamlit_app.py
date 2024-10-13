# Load the necessary packages and files as before
import streamlit as st
import pandas as pd
import json
import requests
import tiktoken
from streamlit_app_about_us import display_about_us

# Load the configuration JSON file from GitHub
config_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/eas_learning_roadmap_config.json"
config_data = requests.get(config_url).json()

# Load the CSV files
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

# Set the title of the app
st.title("EAS Learning Roadmap")

# Sidebar for navigation
page = st.sidebar.selectbox("Navigate to:", ("Home", "About Us"))

# Only show Home page content if 'Home' is selected
if page == "Home":
    st.write("Welcome to the EAS Learning Roadmap app. Use the sidebar to navigate.")

# Clean the DataFrames (this will run regardless of the selected page)
def clean_dataframe(df):
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

programmes_df = clean_dataframe(programmes_df)
bi_df = clean_dataframe(bi_df)

# Define subpages
if page == "About Us":
    display_about_us()

else:
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
        if not filtered_programmes_df.empty:
            filtered_programmes_df = filtered_programmes_df[
                filtered_programmes_df['Estimated Month of Programme'].apply(lambda x: is_month_in_range(x.split(','), min_month_index, max_month_index, month_map))
            ]

        # Filter based on the selected course type
        if selected_course_type != "Select All Courses":
            if not filtered_programmes_df.empty and selected_columns:
                course_mask = filtered_programmes_df[selected_columns].isin([selected_course_type]).any(axis=1)
                filtered_programmes_df = filtered_programmes_df[course_mask]

            # Filter based on the selected roles, only if any role is selected
        if selected_columns and not filtered_programmes_df.empty:
            # Create a mask to filter the DataFrame based on selected roles
            role_mask = filtered_programmes_df[selected_columns].notna().any(axis=1)
            filtered_programmes_df = filtered_programmes_df[role_mask]

            # Rename the role columns to add the prefix "Type of Course - "
            renamed_columns = {col: f"Type of Course - {col}" for col in selected_columns if col in filtered_programmes_df.columns}
            filtered_programmes_df.rename(columns=renamed_columns, inplace=True)

        # Check if there are still rows after filtering; if empty, display a warning
        if filtered_programmes_df.empty:
            st.warning("No Programmes found matching the filter query.")
        else:
            # Ensure programmes_columns contains only columns present in the DataFrame
            valid_programmes_columns = [col for col in programmes_columns if col in filtered_programmes_df.columns]

            st.write("### Available Programmes")
            st.dataframe(filtered_programmes_df[valid_programmes_columns])

    # Initialize session state for conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    st.chat_message("assistant", avatar=None).write('Hi, I am Charlie! Before we begin, please select the roles and/or learning dimensions that you would like course information on. In the text box below, please provide any additional information (e.g. preferred mode of learning, preferred month) to streamline your search. If you do not have any additional criteria, you can just indicate: "No additional considerations."')
    userinput = st.chat_input(placeholder="Tell us more  ?", key=None, max_chars=None, disabled=False, on_submit=None, args=None, kwargs=None)

    # Handle user input
    if userinput:
        st.session_state['conversation_history'].append(f"User: {userinput}")

        # Prepare the conversation history as part of the prompt
        conversation_context = "\n".join(st.session_state['conversation_history'])

        # prompt using history and new input
        prompt = f"""
            <conversationhistory>
            {conversation_context}
            </conversationhistory>
        
            <userinput>
            {userinput}
            </userinput>

            <programmes>
            {filtered_programmes_df}
            </programmes>

            Your primary role is an assistant chatbot that is to recommend professional development programmes for staff...
        """
        # Generate response from the chatbot
        response = get_completion(prompt)

        st.session_state['conversation_history'].append(f"Assistant: {response}")

        # Display the conversation history
        for message in st.session_state['conversation_history']:
            if message.startswith("User:"):
                st.chat_message("user").write(message[6:])
            elif message.startswith("Assistant:"):
                st.chat_message("assistant").write(message[11:])
        
        # Count tokens for the user's input
        tokens_used = count_tokens(prompt) + count_tokens(response)
        
        # Store token count for this query in the list
        token_counts.append(tokens_used)
        
        # Display token countlist, <REMOVE THIS LATER>
        st.write(token_counts)



