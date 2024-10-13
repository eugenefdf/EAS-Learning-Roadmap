import streamlit as st
import tiktoken
import requests

# Token counting constants
TOKEN_PRICE = 0.0004  # Example: price per token in USD for OpenAI

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

def log_token_usage(user_input, response):
    """Log the token usage for each conversation."""
    tokens_used = count_tokens(user_input) + count_tokens(response)
    estimated_cost = estimate_cost(tokens_used)

    # Log the entry
    if 'token_log' not in st.session_state:
        st.session_state['token_log'] = []
    st.session_state['token_log'].append({
        "user_input": user_input,
        "tokens_used": tokens_used,
        "estimated_cost": estimated_cost,
        "response": response
    })

def get_completion(prompt):
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": st.secrets['OPENAI_MODEL_NAME'],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,  # Adjust based on your needs
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return "I'm sorry, there was an error processing your request."

# Initialize session state for conversation history if it doesn't exist
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

st.chat_message("assistant", avatar=None).write('Hi, I am Charlie! Please select the roles and/or learning dimensions that you would like course information on. In the text box below, provide any additional information (e.g., preferred mode of learning). If none, you can just say: "No additional considerations."')

# Capture user input
userinput = st.chat_input(placeholder="Tell us more  ?", key=None, max_chars=None)

# Handle user input
if userinput:  # Ensure userinput is defined and has a value
    st.session_state['conversation_history'].append(f"User: {userinput}")

    # Prepare the conversation history as part of the prompt
    conversation_context = "\n".join(st.session_state['conversation_history'])
    
    # Assuming filtered_programmes_df is defined earlier in your code
    programmes_string = filtered_programmes_df.to_string(index=False)

    # Prompt using history and new input
    prompt = f"""
        <conversationhistory>
        {conversation_context}
        </conversationhistory>

        <userinput>
        {userinput}
        </userinput>

        <programmes>
        {programmes_string}
        </programmes>

        Your primary role is an assistant chatbot that is to recommend professional development programmes for staff...
    """

    # Generate response from the chatbot
    response = get_completion(prompt)

    # Log token usage
    log_token_usage(userinput, response)

    st.session_state['conversation_history'].append(f"Assistant: {response}")

    # Display the conversation history
    for message in st.session_state['conversation_history']:
        if message.startswith("User:"):
            st.chat_message("user", avatar=None).write(message.replace("User:", "").strip())
        else:
            st.chat_message("assistant", avatar=None).write(message.replace("Assistant:", "").strip())