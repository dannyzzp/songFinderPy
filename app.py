# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:14:10 2025

@author: danny
"""

import streamlit as st
import subprocess
import os
import pygame
import sys
# subprocess.run([sys.executable, "-m", "pip", "install", "librosa"])
import librosa
st.write(1515)

st.write(1717)
x,sr = librosa.load('Dave-Ft-Central-Cee-Trojan-Horse-(TrendyBeatz.com).mp3', sr = None) 
st.write(x)
# Set the working directory
#os.chdir('C:\\Users\\danny\\onedrive\\desktop\\songfinder')
st.write(os.getcwd())
# Initialize pygame mixer
#pygame.mixer.init()

# Function to run songFinder.py and get the output
def run_song_finder():
    #st.write(os.path.isfile('/mount/src/songfinderpy/songFinder.py'))
    st.write(os.listdir(os.getcwd())[16])
    st.write(os.path.isfile(os.listdir(os.getcwd())[16]))
    st.write(os.listdir(os.getcwd()))
    result = subprocess.run(
        [f"{sys.executable}", "songFinder.py"],
        #["python", os.listdir(os.getcwd())[16]],
        capture_output=False,
        text=False
    )
    if result.returncode != 0:
        st.error("Error processing the file.")
        return None
    # exec(open("/mount/src/songfinderpy/songFinder.py").read())
    # Parse the output to get the song names
    songs = []
    with open("songRecs.txt", "r") as file:
        for line in file:
            songs.append(line.strip() + '.mp3')  # .strip() to remove newline characters
    return songs

# Function to play an audio file
def play_audio(file_path):
    if pygame.mixer.music.get_busy():  # Stop any currently playing music
        pygame.mixer.music.stop()
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Function to pause audio
def pause_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

# Function to resume audio
def resume_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()

# Function to stop audio
def stop_audio():
    pygame.mixer.music.stop()

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
            
            # Add a play button for each song
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"Play", key=f"play_{i}"):
                    if os.path.exists(song):
                        play_audio(song)
                    else:
                        st.error(f"File {song} not found.")
            with col2:
                if st.button(f"Pause", key=f"pause_{i}"):
                    pause_audio()
            with col3:
                if st.button(f"Resume", key=f"resume_{i}"):
                    resume_audio()
            with col4:
                if st.button(f"Stop", key=f"stop_{i}"):
                    stop_audio()
    
    # Clean up the temporary file
    os.remove("uploadedSong.mp3")