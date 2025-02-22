# jiayou

CHeer me on in person or virutally asynchronously. 


🚀 Setting Up NeonDB for Streamlit Chat

## **Overview**
This guide will help you set up a **free cloud PostgreSQL database** using [NeonDB](https://neon.tech/) for storing chat messages in your Streamlit app.

## **1️⃣ Create a Free NeonDB Account**
1. Go to [Neon.tech](https://neon.tech/).
2. Sign up for a **free account**.
3. Click **Create a New Project**.
4. Choose **PostgreSQL** and name your database.
5. Copy the **Database Connection URL**, which will look like this:
   ```
   postgresql://your-username:your-password@your-db-host.com/dbname
   ```

## **2️⃣ Install Required Python Packages**
Make sure you have **psycopg2** installed to connect your Streamlit app to NeonDB:
```bash
pip install psycopg2
```

## **3️⃣ Update Your Streamlit App Code**
Replace your SQLite setup with the following **PostgreSQL-based chat app**:

```python
import psycopg2
import streamlit as st
import random
from datetime import datetime

# Connect to NeonDB PostgreSQL
conn = psycopg2.connect("postgresql://your-username:your-password@your-db-host.com/dbname")
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

# Assign a random username per session
if "username" not in st.session_state:
    st.session_state.username = f"User{random.randint(1000, 9999)}"

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
```

## **4️⃣ Deploy & Test**
1. Run your Streamlit app:
   ```bash
   streamlit run your_script.py
   ```
2. Send messages and confirm they are stored in **NeonDB**.
3. Check your database by logging into **NeonDB** and running:
   ```sql
   SELECT * FROM messages;
   ```

🎉 **You're now using a cloud database for your chat app!** 🚀

