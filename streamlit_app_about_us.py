import streamlit as st

def display_about_us():
    st.title("About Us")

    st.subheader("Project Scope & Objective")
    st.write("""Develop an intuitive, user-friendly digital platform to present personalised learning opportunities for the School Administrative Team (SAT), to support their professional learning and development.
                \n The developed solution needs to meet these objectives:
                \n 1. User-Centricity: Create a comprehensive digital platform with an intuitive interface that centralises all learning opportunities and competency information, presenting complex data clearly and concisely for users with varying digital literacy levels.
                \n 2. Personalisation: Implement an intelligent recommendation system that provides tailored learning opportunities based on each officer's roles and interest in competency area.
                \n 3. Efficiency Enhancement: Streamline the process of finding and organising professional learning opportunities, significantly reducing time spent on these tasks.
    """)

st.subheader("Data Sources")
st.write("""We refer to the competency framework and learning roadmap provided by HR and the EAS Professional Development Unit.
        """)

st.subheader("Features")
st.write("""The resultant product includes the following features:
            \n 1. Ability for user to look at courses for multiple officer groups (this may be helpful for SAT who are in a supervisory role).
            \n 2. Ability for user to look at specific selector, learning dimension, course type and preferred month of learning. This would help the user quickly narrow their search options.
            \n 3. Ability for user to include other considerations that they may have to better refine options according to their needs.
            """)

#Welcome to the EAS Learning Roadmap! 
        #Our platform is designed to help EAS officers navigate their professional development journey with ease.
        
        #Here, you can find courses and training programmes that align with your role and learning preferences. 
        #Our goal is to ensure every officer has access to the resources they need to excel in their roles and contribute effectively to their teams.
        
        #Feel free to explore and let us know how we can assist you in your learning journey.
