import streamlit as st
import os
from detect import detect_weapon
from database import init_db, insert_log, get_logs
from datetime import datetime

# Set up folders
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Initialize DB
init_db()

# Page config
st.set_page_config(page_title="Weapon Detection", layout="centered")
st.title("🔫 Weapon Detection using YOLOv8")
st.write("Upload an image to detect handguns or knives using a custom-trained deep learning model.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Detect weapon
    result_path, detected_classes = detect_weapon(file_path)
    
    # Log to DB
    insert_log(uploaded_file.name, ", ".join(detected_classes), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Show result
    st.image(result_path, caption="Detection Result", use_column_width=True)
    st.success(f"Detected: {', '.join(detected_classes)}")

# Display history
st.header("🗂 Detection History")
logs = get_logs()
if logs:
    for row in logs[::-1]:
        st.markdown(f"- **Image**: `{row[0]}` | **Prediction**: `{row[1]}` | **Time**: `{row[2]}`")
else:
    st.info("No logs found yet.")
