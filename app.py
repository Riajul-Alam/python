import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml
from db_connection import get_database_connection

st.set_page_config(
    page_title="Admission Form",
    page_icon=":sunny:",
    # layout="wide",
    initial_sidebar_state="expanded",
)
# database localhost connection
# @st.cache()

# def get_database_connection():
#     db = mysql.connect(host = "localhost",
#                       user = "root",
#                       passwd = "root",
#                       database = "mydatabase",
#                       auth_plugin='mysql_native_password')
#     cursor = db.cursor()
#     return cursor, db
 
cursor, db = get_database_connection()
 
# cursor.execute('''CREATE TABLE studentinfo (id varchar(20) PRIMARY KEY,
#                                       student_name varchar(255),
#                                       fathers_name varchar(255),
#                                       mothers_name varchar(255),
#                                       present_address varchar(500),
#                                       permanent_address varchar(500),
#                                       contact_no varchar(11),
#                                       email varchar(255),
#                                       gpa varchar(10),
#                                       religion varchar(255),
#                                       nationality varchar(15),
#                                       reg_date date,
#                                       date_of_birth date,
#                                       gender varchar(8))''')

def admin():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username=="admin" and password=='admin':
            st.sidebar.success('Login Success')

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from studentinfo where reg_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                st.write(i[1])
                st.write(i[2])
                Accept=st.button('Accept',key=i[0])
                if Accept:
                    st.write('Accepted')
                    cursor.execute(f"Update studentinfo set status='Accepted' where id='{i[0]}'")
                    db.commit()
                Reject=st.button('Reject',key=i[0])
                if Reject:
                    st.write('Rejected')
                    cursor.execute(f"Update studentinfo set status='Rejected' where id='{i[0]}'")
                    db.commit()

        else:
            st.sidebar.warning('Wrong Credintials')


def form():
    uid=uuid4()
    uid=str(uid)[:10]
    with st.form(key='member form'):
        student_name = st.text_input("Name")
        fathers_name = st.text_input("Father's Name")
        mothers_name = st.text_input("Mother's Name")
        present_address = st.text_area("Present Address")
        permanent_address = st.text_area("Permanent Address")
        email = st.text_input("E-mail")
        mobile = st.text_input('Mobile')
        gpa = st.text_input("GPA")
        religion = st.selectbox("Religion",('--Select Religion--','Islam','Hindu','Cristian'))
        nationality = st.text_input("Nationality")
        reg_date = st.date_input("Registration Date")
        date_of_birth = st.date_input("Bith Date")
        gender = st.radio('Gender', ('Male', 'Female'))
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO studentinfo (id ,student_name,fathers_name,mothers_name,present_address,permanent_address,contact_no,email,gpa, 
                                            religion,nationality,reg_date,date_of_birth,gender) 
                                    VALUES ( '{uid}', '{student_name}', '{fathers_name}', '{mothers_name}', '{present_address}', '{permanent_address}','{mobile}', '{email}', '{gpa}', '{religion}', '{nationality}' ,'{reg_date}' ,'{date_of_birth}', '{gender}')'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{student_name}*! You have successfully Registered')
            st.code(uid)
            st.warning("Please Store this code!!!")
        
def info():
    id=st.text_input('Your Code')
    Submit=st.button(label='Search')
    if Submit:
    	cursor.execute(f"select * from studentinfo where id='{id}'")
    	tables = cursor.fetchall()
    	st.write(tables)

def stat():
    id=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from studentinfo where id='{id}'")
        table=cursor.fetchall()
        st.write(table)

def main():
    st.title('Diploma in Data Science Admission')
    selected=st.sidebar.selectbox('Select',
                        ('-----------',
                        'Admin',
                        'Registration',
                        'Information',
                        'Status'
                        ))
    if selected=='Admin':
        admin()
    elif selected=='Registration':
        form()
    elif selected=='Information':
        info()
    elif selected=='Status':
        stat()
if __name__=='__main__':
    main()
