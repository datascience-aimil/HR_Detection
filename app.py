import time
import requests
import streamlit as st
from io import BytesIO

# Function to capture and send video
def capture_and_send_video():
    # Initialize the list to store captured frames
    video_data = []
    start_time = time.time()

    # Create a unique key counter
    key_counter = 0

    # Streamlit camera input (with a unique key for each instance)
    while time.time() - start_time < 1:  # Record for 33 seconds
        # Increment the key counter for each new camera input
        key_counter += 1

        # Capture image from camera input with a unique key
        img = st.camera_input("Take a photo", key=f"camera_{key_counter}")

        if img is not None:
            # Display the captured image
            st.image(img, caption="Captured Image", use_column_width=True)
            video_data.append(img.getvalue())  # Append image bytes

        # Display a message indicating video capture duration
        st.write(f"Recording... {int(time.time() - start_time)} seconds elapsed.")

    st.write("Sending 33 seconds of images to backend...")

    # Send the captured frames to the backend
    response = send_to_backend(video_data)

    # Handle backend response
    if response.status_code == 200:
        results = response.json()
        st.write("Results received:", results)
    else:
        st.write("Failed to get results.")

# Function to send video data (image frames) to the backend
def send_to_backend(video_data):
    url = "http://your_backend_url.com/upload_video"  # Replace with your backend URL
    files = []
    
    # Package each image as a file in the request
    for idx, frame in enumerate(video_data):
        files.append(("file", (f"frame_{idx}.jpg", frame, "image/jpeg")))

   # response = requests.post(url, files=files)
    return {"HR":72}

# Streamlit interface
def main():
    st.title("Live Video Recording and Sending to Backend")

    if st.button("Start Recording"):
        st.write("Recording started... Please show your face to the camera.")
        capture_and_send_video()

if __name__ == "__main__":
    main()
