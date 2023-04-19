!pip install easyocr

!pip install -q streamlit

import re
import easyocr
import PIL
from PIL import ImageDraw
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
print(conn)

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import pandas as pd
# import streamlit as st
# from io import BytesIO
# import numpy as np 
# import easyocr as ocr
# import PIL
# from PIL import ImageDraw
# from PIL import Image
# import sqlite3
# 
# def ocr_model(): 
#     reader = ocr.Reader(['en'],model_storage_directory='.', gpu = False) 
#     return reader 
# 
# #@st.cache_data(show_spinner= "Extracting Text")
# def draw_boxes(image,bounds,color='red',width=2):
#   draw=ImageDraw.Draw(image)
#   for bound in bounds:
#     p0,p1,p2,p3=bound[0]
#     draw.line([*p0,*p1,*p2,*p3,*p0],fill=color,width=width)
#   return image
# 
# @st.cache_data
# def insertBLOB(filename,im_data,extracted_text):
#     try:
#         sqliteConnection = sqlite3.connect("bizcardx_db.db")
#         cursor = sqliteConnection.cursor()
# 
#         create_table=f"""CREATE TABLE IF NOT EXISTS {filename} (
#                     "filename"	TEXT NOT NULL,
#                     "image"	BLOB NOT NULL,
#                     "extracted_text"	TEXT NOT NULL,
#                     PRIMARY KEY("filename"))"""
#         cursor.execute(create_table)
# 
#         insert_query = f""" INSERT INTO {filename} (filename, image, extracted_text) VALUES (?, ?, ?)"""  
#         data_tuple = (filename,im_data,extracted_text)
#         cursor.execute(insert_query,data_tuple)
# 
#         sqliteConnection.commit()
#         cursor.close()
# 
#     except sqlite3.Error as error:
#         st.error("Failed to insert blob data into sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
# 
# def readBlobData(saved_name):
#   try:
#       sqliteConnection = sqlite3.connect("bizcardx_db.db")
#       cursor = sqliteConnection.cursor()
#       st.write("Connected to SQLite")
# 
#       view_query = f"SELECT * from {saved_name}"
#       cursor.execute(view_query)
#       record = cursor.fetchall()
# 
#       for row in record:
#           name = row[0]
#           photo = row[1]
#           text = row[2]
#           
#       cursor.close()
#       return name, photo, text
# 
#   except :
#       st.error("Details Not found")
#   finally:
#       if sqliteConnection:
#           sqliteConnection.close()
# 
# def del_details(file_name):
#     try:
#         sqliteConnection = sqlite3.connect("bizcardx_db.db")
#         cursor = sqliteConnection.cursor()
#         #st.write("Connected to SQLite")
#         
#         drop_query = f"DROP TABLE {file_name} "
#         cursor.execute(drop_query)
#         
#         sqliteConnection.commit()
#         cursor.close()
#     except:
#         st.write("Failed to delete data from sqlite table")
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
# #extract_info(text)
# 
# st.set_page_config(page_title='💳BizCardX: Extracting Business Card Data with OCR',
#                   # page_icon=,
#                    layout='wide')
# st.sidebar.image("biz.gif", width=400)
# selected =st.sidebar.selectbox('📒Welcome to BizCardX',('HOMEPAGE', 'SEND YOUR CARD', 'View Details', 'Delete Details'))
# #def play_video(video_path):
#  #   video_file = open(video_path, 'rb')
#   #  video_bytes = video_file.read()
#    # st.video(video_bytes)
# if selected == 'HOMEPAGE':
#     st.header('💳BizCardX: Extracting Business Card Data with OCR')
# 
#     st.subheader('PURPOSE : Business Card Data Extraction')
#     #st.image("BusinessCardSDK_Banner.png")
#     st.write('''A business card scanner makes uploading data from paper business cards, in volume, 
#              easier than typing that data. A business card scanning app can extract, classify and translate multilingual data
#               from paper business cards via the device’s internal camera. Once the business card scanner has extracted the data,
#               users can import the data into their contact manager or a CRM system.''')
#     st.subheader("OUR KEY-POINTS")
#     st.write('''1. OCR technology: Extract business card data with ease using our state-of-the-art OCR technology.''')
#     st.write('''2. Editable data: Easily update and edit your contact information as needed.''')
#     st.write('''3. Data upload and secure storage: Upload your business card data securely to our database for safekeeping.''')
#     st.write('''4. Download in JSON format: Download your business card data in JSON format for easy integration with other software applications.''')
#     st.subheader("[github](https://github.com/ajaywanekar)")
#     st.subheader("[linkedin](https://www.linkedin.com/in/ajay-wanekar-245a50230/)")
# 
# elif selected == 'SEND YOUR CARD':
#     st.subheader('Lets Upload Your card')
#     file = st.file_uploader("Choose Your Image",
#                      accept_multiple_files=False,
#                      type=['png', 'jpg', 'jpeg'],
#                      label_visibility="visible")
#     #image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])
#     reader = ocr_model()
#     if file is not None:
#       if st.button("extract info"):
#         bytes_data = file.getvalue()
#         col1, col2 = st.columns(2)
# 
#         with col1:       
#         
#           input_image=PIL.Image.open(file)
# 
#           with st.spinner("Extracting text..."):
#             
#             #reading text from image
#             result=reader.readtext(np.array(input_image),detail=1,paragraph=True)
#             
#             #making list of the extracted texts
#             result_text=[]
#  
#             for text in result:
#                 result_text.append(text[1])
# 
# 
#             #drawing boxes in image over the detected texts
#             st.write(' Detected texts')
#             st.image(draw_boxes(input_image,result))
#         
#         with col2:
#           with st.form("my_form"):           
#             st.write('Edit the extracted text before saving')
#             edited_list = st.experimental_data_editor(result_text,num_rows="dynamic")
#             filename=st.text_input('Save file as')
#             st.caption('-->Save filename with Contact no.as it creates unique value')
#             submitted = st.form_submit_button("Save to DB")
# 
#         if submitted and filename:
#             extracted_text=''
#             for text in edited_list:
#                 extracted_text+=' '+text
# 
#             insertBLOB(filename,bytes_data,extracted_text)
#             st.snow()
# 
# elif selected == "View Details":
#     filename=st.text_input('Enter the filename')
#     submitted = st.button("View Details")
# 
#     if filename and submitted:
#       try:
#         name, photo, text= readBlobData(filename)
#         col1, col2 = st.columns(2)
# 
#         with col1:
#         #st.write(name)
#           st.subheader("Business Card")
#           image_data = BytesIO(photo)
#           img = Image.open(image_data)
#           st.image(img)
# 
#         with col2:
#           st.subheader("Details")
#           st.write(text)
#       except:
#         st.info("Please Upload the Business Card")
# 
# if selected == "Delete Details":
# 
#     file_name=st.text_input('Enter the file name', key='verification_1')
# 
#     submitted_button_1 = st.button("Delete Details", key = 'key1')
#     st.error('Data cannot be recovered once deleted')
# 
#     if file_name and submitted_button_1: 
#           try:
#               sqliteConnection = sqlite3.connect("bizcardx_db.db")
#               cursor = sqliteConnection.cursor()
#               #st.write("Connected to SQLite")
#               
#               drop_query = f"DROP TABLE {file_name}"
#               cursor.execute(drop_query)
#               st.success("Details Deleted successfully")
#               
#               sqliteConnection.commit()
#               cursor.close()
#           except:
#               st.error("File not found")
#           finally:
#               if sqliteConnection:
#                   sqliteConnection.close()   
#           
#     elif submitted_button_1:
#       st.info("Please check the file name")
#

!npm install localtunnel

!streamlit run /content/app.py &>/content/logs.txt &

!npx localtunnel --port 8501