import cv2
import numpy as np
import requests
import time
import streamlit as st
from io import BytesIO
from threading import Thread

# Function to capture and send video
def capture_and_send_video():
    # Open the video capture (default camera)
    cap = cv2.VideoCapture(0)

    # Set the video codec and output file format
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    frame_count = 0
    start_time = time.time()
    video_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Show live video feed
        out.write(frame)
        video_data.append(frame)
        frame_count += 1

        # Display video feed on Streamlit
        st.image(frame, channels="BGR", use_column_width=True)

        # After 33 seconds, stop and send the recorded video
        if time.time() - start_time > 33:
            st.write("Sending 33 seconds video to backend...")

            # Convert frames to video format (e.g., AVI or MP4)
            video_bytes = encode_video(video_data)
            
            # Send video data to backend
            response = send_to_backend(video_bytes)

            # Handle backend response
            if response.status_code == 200:
                results = response.json()
                st.write("Results received:", results)
            else:
                st.write("Failed to get results.")

            # Continue recording
            video_data = []  # Reset data for next batch

    cap.release()
    out.release()

# Function to encode video to bytes
def encode_video(frames):
    # Use cv2 to encode the frames to a video byte stream
    video_bytes = BytesIO()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_bytes, fourcc, 20.0, (640, 480))

    for frame in frames:
        out.write(frame)
    
    out.release()
    video_bytes.seek(0)  # Go to the beginning of the byte stream
    return video_bytes

# Function to send video to the backend
def send_to_backend(video_bytes):
    url = "http://your_backend_url.com/upload_video"  # Replace with your backend URL
    files = {"file": ("video.avi", video_bytes, "video/avi")}
    response = requests.post(url, files=files)
    return response

# Streamlit interface
def main():
    st.title("Live Video Recording and Sending to Backend")

    if st.button("Start Recording"):
        st.write("Recording started... Please show your face to the camera.")
        capture_and_send_video()

if __name__ == "__main__":
    main()
