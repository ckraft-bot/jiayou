import psycopg2
import streamlit as st
import random
from datetime import datetime



# Connect to NeonDB PostgreSQL
conn = psycopg2.connect(f"{st.secrets['neondb']}") # for deployment
# conn = psycopg2.connect(connection_str) # for local testing
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    user TEXT,
                    text TEXT,
                    timestamp TEXT)''')
conn.commit()

# Function to load messages
def load_messages():
    cursor.execute("SELECT user, text, timestamp FROM messages ORDER BY timestamp ASC")
    return cursor.fetchall()

# Sidebar
st.sidebar.title("Erlanger Chattanooga Marathon")

st.title("💬 Race Chats")
st.write("Chat with others in real time!")

# Load messages
messages = load_messages()

# Display chat messages
for msg in messages:
    st.markdown(f"**{msg[0]}** ({msg[2]}): {msg[1]}")

# Input field for new messages
new_message = st.text_input("Type your message:", key="chat_input")
if st.button("Send") and new_message:
    timestamp = datetime.now().strftime("%I:%M %p")
    cursor.execute("INSERT INTO messages (user, text, timestamp) VALUES (%s, %s, %s)", 
                (st.session_state.username, new_message, timestamp))
    conn.commit()
    st.rerun()
