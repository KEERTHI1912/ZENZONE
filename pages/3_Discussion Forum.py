import streamlit as st
import sqlite3

# Create a SQLite database and tables for users, topics, posts, and replies
conn = sqlite3.connect('form.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY, title TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, author_id INTEGER, topic_id INTEGER, content TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY, author_id INTEGER, post_id INTEGER, content TEXT)')
conn.commit()

# Streamlit UI
st.title('Discussion Forum')

# User registration
st.subheader('Register')
username = st.text_input('Enter your username:')
if st.button('Register'):
    cur.execute('INSERT INTO users (username) VALUES (?)', (username,))
    conn.commit()
    st.success(f'Welcome, {username}!')

# Create a topic
st.subheader('Create a New Topic')
title = st.text_input('Topic title:')
if st.button('Create Topic'):
    cur.execute('INSERT INTO topics (title) VALUES (?)', (title,))
    conn.commit()
    st.success(f'Topic created: {title}')

# Forum topics
st.subheader('Forum Topics')
topics = cur.execute('SELECT id, title FROM topics').fetchall()
selected_topic = st.selectbox('Select a topic:', topics)

if selected_topic is not None:
    st.write(f'Selected Topic: {selected_topic[1]}')

    # Create a new post
    st.subheader('Create a New Post')
    post_content = st.text_area('Post content:')
    if st.button('Create Post'):
        if post_content:
            author_id = cur.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
            cur.execute('INSERT INTO posts (author_id, topic_id, content) VALUES (?, ?, ?)', (author_id, selected_topic[0], post_content))
            conn.commit()
            st.success('Post created successfully!')
        else:
            st.warning('Please enter post content.')

    # Display posts
    st.subheader('Posts in this Topic')
    posts = cur.execute('SELECT p.id, u.username, p.content FROM posts p JOIN users u ON p.author_id = u.id WHERE p.topic_id = ?', (selected_topic[0],)).fetchall()
    for post in posts:
        st.write(f'Author: {post[1]}')
        st.write(f'Content: {post[2]}')
        reply_button = st.button('Reply', key=f'reply_{post[0]}')
        if reply_button:
            post_id = post[0]
            reply_content = st.text_area(f'Reply to {post[1]}:', key=f'reply_content_{post_id}')
            if st.button('Post Reply', key=f'post_reply_{post_id}'):
                if reply_content:
                    cur.execute('INSERT INTO replies (author_id, post_id, content) VALUES (?, ?, ?)', (author_id, post_id, reply_content))
                    conn.commit()
                    st.success('Reply posted successfully!')
                else:
                    st.warning('Please enter reply content.')

# Close the database connection
conn.close()