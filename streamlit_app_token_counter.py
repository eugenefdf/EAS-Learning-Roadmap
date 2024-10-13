import streamlit as st
import tiktoken

# Token counting constants
INPUT_TOKEN_PRICE = 0.150 / 1_000_000  # Price per input token in USD
OUTPUT_TOKEN_PRICE = 0.600 / 1_000_000  # Price per output token in USD

# Function definitions for token counting
def get_tokenizer():
    return tiktoken.encoding_for_model("gpt-4o-mini")

def count_tokens(prompt):
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(prompt))

def estimate_cost(input_tokens_used, output_tokens_used):
    return (input_tokens_used * INPUT_TOKEN_PRICE) + (output_tokens_used * OUTPUT_TOKEN_PRICE)

def log_token_usage(user_input, summary_and_questions, response):
    input_tokens_used = count_tokens(user_input)
    output_tokens_used = count_tokens(response)
    estimated_cost = estimate_cost(input_tokens_used, output_tokens_used)

    if 'token_log' not in st.session_state:
        st.session_state['token_log'] = []  # Initialize if it doesn't exist
    
    st.session_state['token_log'].append({
        "user_input": user_input,
        "summary_and_questions": summary_and_questions,
        "input_tokens_used": input_tokens_used,
        "output_tokens_used": output_tokens_used,
        "estimated_cost": estimated_cost
    })

    # Keep only the last 5 entries
    if len(st.session_state['token_log']) > 5:
        st.session_state['token_log'] = st.session_state['token_log'][-5:]

def clear_token_log():
    st.session_state['token_log'] = []

def display_token_counter():
    if st.button("Clear Log", key="clear_log_button"):
        clear_token_log()
        st.success("Token log cleared.")

    st.write("### Token Usage Log")
    if 'token_log' in st.session_state and st.session_state['token_log']:
        for entry in st.session_state['token_log']:
            st.write(f"**User Input:** {entry.get('user_input', 'N/A')}")
            st.write(f"**Summary and Questions:** {entry.get('summary_and_questions', 'N/A')}")
            st.write(f"**Input Tokens Used:** {entry.get('input_tokens_used', 0)}")
            st.write(f"**Output Tokens Used:** {entry.get('output_tokens_used', 0)}")
            st.write(f"**Estimated Cost:** ${entry.get('estimated_cost', 0):.8f}")
            st.write("---")
    else:
        st.write("No token usage data available yet.")

# Initialize selected_columns to avoid NameError
if 'selected_columns' not in st.session_state:
    st.session_state['selected_columns'] = []  # or set a default value as needed

# Call the display function to render the token counter
display_token_counter()
