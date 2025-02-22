import psycopg2
import streamlit as st
import random
from datetime import datetime
import pytz  

# connection_str = st.secrets["postgres"]["connection_str"]
connection_str = "postgresql://neondb_owner:npg_Ilg2G7Vdsntr@ep-dry-breeze-a85tfkd4-pooler.eastus2.azure.neon.tech/erlanger_half_chat?sslmode=require"

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

# Function to insert and clear input
def insert_message():
    if st.session_state.chat_input:
        # Set timezone to Eastern Time
        eastern_time_zone = pytz.timezone('US/Eastern')
        # Get current time in Eastern Time
        timestamp = datetime.now(eastern_time_zone).strftime("%I:%M %p")
        
        # Insert the new message into the database
        cursor.execute("INSERT INTO messages (username, text, timestamp) VALUES (%s, %s, %s)", 
                    (st.session_state.username, st.session_state.chat_input, timestamp))
        conn.commit()
        
        # Clear the input box
        st.session_state.chat_input = ""

        # Use rerun to update the UI and show the cleared input field
        st.rerun()

# Sidebar
st.title("💬 Race Chats")
st.write("Chat with others in real time!")
st.info("[Click here to watch the app tutorial :tv:](https://youtu.be/VOCMwRqKgCg?si=dBO3vYMZo4BfDnd7)")

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
st.text_input("Type your message:", key="chat_input", on_change=insert_message)

# Handle sending and resetting chat input
if st.button("Send"):
    insert_message()
