import streamlit as st
import tiktoken

# Token counting constants
TOKEN_PRICE = 0.00000015  # Updated price per token in USD for OpenAI

# Use the tokenizer for the specific model
def get_tokenizer():
    return tiktoken.encoding_for_model("gpt-4o-mini")

def count_tokens(prompt):
    """Count the number of tokens in a prompt using the GPT-4o-mini tokenizer."""
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(prompt))

def estimate_cost(tokens_used):
    """Estimate the cost based on tokens used."""
    return tokens_used * TOKEN_PRICE

def clear_token_log():
    """Clear the token log."""
    st.session_state['token_log'] = []
    st.success("Token log has been cleared.")

def display_token_counter():
    """Display the token counter page and log."""
    # Initialize session state for token log if it doesn't exist
    if 'token_log' not in st.session_state:
        st.session_state['token_log'] = []

    st.write("### Token Usage Log")
    
    # Add a button to clear the log
    if st.button("Clear Token Log"):
        clear_token_log()

    if st.session_state['token_log']:
        for entry in st.session_state['token_log']:
            st.write(f"**User Input:** {entry['user_input']}")
            st.write(f"**Malicious Check:** {entry['malicious_check']}")
            st.write(f"**Summary and Questions:** {entry['summary_and_questions']}")
            st.write(f"**Tokens Used:** {entry['tokens_used']}")
            st.write(f"**Estimated Cost:** ${entry['estimated_cost']:.8f}")  # Adjusted decimal places for clarity
            st.write(f"**Assistant Response:** {entry['response']}")
            st.write("---")  # Separator for readability
    else:
        st.write("No token usage data available yet.")

def log_token_usage(user_input, response, summary_and_questions):
  """Log the token usage for each conversation along with additional data."""
  tokens_used = count_tokens(user_input) + count_tokens(response) + count_tokens(summary_and_questions)
  estimated_cost = estimate_cost(tokens_used)

  # Log the entry
  st.session_state['token_log'].append({
      "user_input": user_input,
      "malicious_check": "No",  # Change this if malicious input is detected
      "summary_and_questions": summary_and_questions,
      "tokens_used": tokens_used,
      "estimated_cost": estimated_cost,
      "response": response
  })

  # Keep only the last 5 entries in the log
  if len(st.session_state['token_log']) > 5:
      st.session_state['token_log'] = st.session_state['token_log'][-5:]