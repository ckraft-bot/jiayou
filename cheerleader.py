import psycopg2
import streamlit as st
import random
from datetime import datetime
import os

connection_str = st.secrets["postgres"]["connection_str"]

# Ensure username is initialized
if "username" not in st.session_state:
    st.session_state.username = f"User{random.randint(1000, 9999)}"

# Connect to NeonDB PostgreSQL
conn = psycopg2.connect(connection_str)  
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    username TEXT,
                    text TEXT,
                    timestamp TEXT)''')
conn.commit()

# Function to load messages
def load_messages():
    cursor.execute("SELECT username, text, timestamp FROM messages ORDER BY timestamp ASC")
    return cursor.fetchall()

# Sidebar
st.title("💬 Race Chats")
st.write("Chat with others in real time!")

# Sidebar content
st.sidebar.title("Erlanger Chattanooga Marathon")
st.sidebar.markdown("""## Logistics
- **Date:** March 2, 2025
- **Location:** Chattanooga, TN
- **Start Time:** 7:30 AM
- **Start Location:** First Horizon Pavilion, [1826 Reggie White Blvd, Chattanooga, TN 37408](https://maps.app.goo.gl/irLBHxsJaJ2bh9Dp8)
- **Distance:** 13.1 miles

## Quick Links
- The main [page](https://www.chattanoogamarathon.com/)
- The [schedule](https://www.chattanoogamarathon.com/race/schedule)
- The parking/traffic [info](https://www.chattanoogamarathon.com/race/traffic)
- The half marathon [course map](https://www.chattanoogamarathon.com/assets/pdf/2024-ChattMarathon-Maps.pdf)
- _coming soon_ Runner GPS [tracker]()
""")

# Load messages
messages = load_messages()

# Display chat messages
for msg in messages:
    st.markdown(f"**{msg[0]}** ({msg[2]}): {msg[1]}")

# Input field for new messages
new_message = st.text_input("Type your message:", key="chat_input")
if st.button("Send") and new_message:
    timestamp = datetime.now().strftime("%I:%M %p")
    cursor.execute("INSERT INTO messages (username, text, timestamp) VALUES (%s, %s, %s)", 
                (st.session_state.username, new_message, timestamp))
    conn.commit()
    st.rerun()
