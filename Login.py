import streamlit as st
import pandas as pd
import subprocess

import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



def main():
    """Simple Login App"""

    

    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        
        st.write("# Welcome to Zen! 👋")
        
        
        st.markdown('''
                       

**ZEN - Your Path to Student Wellness**

Hello Zenites, a dedicated mental health and well-being platform designed specifically for students. We understand the unique challenges you face during your academic journey, and we're here to provide you with the support, resources, and community you need to thrive, both in and out of the classroom.

**Why Choose ZEN?**

🧠 **Tailored for Students:** We've created a safe and inclusive space where you can connect with peers who understand your experiences. Our platform is built with students in mind, making it easy for you to find the support you need.

📚 **Academic Success:** Your mental health plays a crucial role in your academic performance. We offer tools and strategies to help you manage stress, anxiety, and the pressures of student life while maintaining a strong focus on your studies.

🤝 **Community and Support:** Join a community of like-minded students who are on a similar journey. Share your experiences, provide and receive support, and know that you're never alone in your challenges.

🔒 **Privacy and Confidentiality:** Your well-being is your priority, and it's ours too. We ensure the utmost privacy and confidentiality in all interactions and discussions on our platform.

**What ZEN Offers:**

🧘 **Mental Health Resources:** Access a wealth of mental health resources, articles, and self-help tools to enhance your emotional well-being.

🤖 **Chat with Our Chatbot:** Connect with our friendly chatbot for immediate support, information, and coping strategies, available 24/7.

📆 **Therapist Matching:** Find a therapist or counselor specializing in student-related issues through our trusted network of mental health professionals.

📣 **Peer Support:** Engage with fellow students through group discussions, forums, and peer-to-peer support.

📊 **Progress Tracking:** Monitor your mental health journey and see your progress with our easy-to-use tracking tools.

🎉 **Rewards and Achievements:** Stay motivated and earn rewards as you take steps towards better mental health.

**Join Us Today**

Your mental health is a vital aspect of your academic and personal success. ZEN is your one-stop destination for well-being and support. Take the first step towards a healthier, happier you by joining our community today.

Ready to embrace a brighter future? Sign up now and discover the difference ZEN can make in your student life.


*Your well-being is worth it. Join ZEN and let's embark on this journey to mental wellness together.*
''')

    elif choice == "Login":
        st.subheader("Enter the ZEN world!")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))
                subprocess.Popen(["streamlit","run","1_Chatbot.py"])
            else:
                st.warning("Incorrect Username/Password")





    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
    main()