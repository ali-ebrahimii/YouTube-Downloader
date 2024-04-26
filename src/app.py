import streamlit as st
from main import YouTubeDownloader
from pytube.exceptions import RegexMatchError
from stqdm import stqdm
from time import sleep

#Title of the application
st.image('../images/banner.png')
st.title(":zap: YouTube Downloader")


user_input = str(st.text_input("Copy url of video here"))

if user_input:
    yt = YouTubeDownloader(user_input)
    ext, res = yt.ExtRes()

    file_ext = st.selectbox('File Extensions',ext)
    if file_ext != 'Please select an option':
        st.write(f'you choose {file_ext} for File Extensions')
    else:
        st.write('Please make a selection from the dropdown.')
    
    file_res = st.selectbox('File Resolution',res)
    if file_res != 'Please select an option':
        st.write(f'you choose {file_res} for File Resolution')
    else:
        st.write('Please make a selection from the dropdown.')
    
    output_path = st.selectbox('Output Path',['Please select an option', 'Desktop', 'Other'])
    if output_path != 'Please select an option':
        st.write(f'you choose {output_path} for Output Path')
    else:
        st.write('Please make a selection from the dropdown.')
    
    if st.button('Click here to Download the video'):
        if output_path == 'Desktop':
            downloader = YouTubeDownloader(url=user_input, 
                                           file_extension=file_ext, 
                                           output_path='../../../../../Desktop', 
                                           quality=file_res,
                                           )
            downloader.Download()
        
        if output_path == 'Other':
            pass






