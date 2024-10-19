import streamlit as st

def display_methodology():
    st.title("Methodology")
    st.write("""
      Please refer to the methodology below for a detailed breakdown.
    """)
    
    # Add an image
    st.image("https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Project%20Flow%20Chart%20(v2).jpg", caption="Flow Chart", use_column_width=True)