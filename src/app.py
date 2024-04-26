import os
from pathlib import Path
import streamlit as st
from main import YouTubeDownloader
from pytube.exceptions import RegexMatchError
from stqdm import stqdm
from time import sleep

st.image('../images/banner.png')
st.title(":zap: YouTube Downloader")


st.markdown("""
Please enter the URL of the YouTube video you want to download, 
select the desired file format and resolution, 
and specify the path where you want the video to be saved. 
Ensure that you have write permission to the path you specify.
""")


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
    
    output_path = st.text_input("Enter the output path for the videos", 
                                placeholder="E.g., /Users/YourName/Videos",
                                help="Enter the full path to the folder where you want to save the downloaded video.")


    if st.button('Click here to Download the video'):
        if output_path:
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            downloader = YouTubeDownloader(url=user_input, 
                                           file_extension=file_ext, 
                                           output_path=output_path, 
                                           quality=file_res)
            downloader.Download()
            st.success(f"Video downloaded successfully to {output_path}")
        else:
            st.error("Please enter a valid output path.")






