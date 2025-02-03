# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:14:10 2025

@author: danny
"""

import streamlit as st
import subprocess
import os
import sys

# Set the working directory
# os.chdir('C:\\Users\\danny\\onedrive\\desktop\\songfinder')
st.write(os.getcwd())

# Function to run songFinder.py and get the output
def run_song_finder():
    st.write(os.listdir(os.getcwd()))
    result = subprocess.run(
        [f"{sys.executable}", "songFinder.py"],
        capture_output=False,
        text=False
    )
    if result.returncode != 0:
        st.error("Error processing the file.")
        return None
    # Parse the output to get the song names
    songs = []
    with open("songRecs.txt", "r") as file:
        for line in file:
            songs.append(line.strip() + '.mp3')  # .strip() to remove newline characters
    return songs

# Streamlit app
st.title("🎵 Song Finder App (recommend music based on audio similarities)")
st.write("Upload an MP3 file to find similar songs (song durations between 2 mins and 6 mins preferred)")

# File uploader with a unique key
uploaded_file = st.file_uploader("Choose an MP3 file", type=["mp3"], key="file_uploader_unique_key")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("uploadedSong.mp3", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Run songFinder.py
    st.write("Processing your file...")
    songs = run_song_finder()
    
    if songs:
        st.success("Here are your recommended songs:")
        for i, song in enumerate(songs):
            st.write(f"{i+1}. {song}")
            
            # Display the audio player for each song
            if os.path.exists(song):
                st.audio(song, format="audio/mp3")
            else:
                st.error(f"File {song} not found.")
    
    # Clean up the temporary file
    os.remove("uploadedSong.mp3")