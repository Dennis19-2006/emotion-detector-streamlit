import streamlit as st
import librosa
import numpy as np
import pickle
import soundfile as sf
import os

# Load the pre-trained emotion detection model
MODEL_PATH = "emotion_model.pkl"  # Make sure you have a trained model
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    model = None

# Function to extract MFCC features
def extract_features(file_path, n_mfcc=40):
    audio, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfccs.T, axis=0)  # Take mean to reduce dimensions

# Streamlit UI
st.title("🎤 AI Emotion Detector from Voice")
st.write("Upload an audio file to analyze your emotions.")

uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    file_path = f"temp_audio.wav"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    if model:
        # Extract features and predict
        features = extract_features(file_path).reshape(1, -1)
        prediction = model.predict(features)[0]
        emotions = {0: "Neutral", 1: "Happy", 2: "Sad", 3: "Angry", 4: "Fearful"}
        st.subheader(f"Detected Emotion: {emotions.get(prediction, 'Unknown')}")
    else:
        st.error("Model not found. Please train and upload the model.")
    
    # Clean up
    os.remove(file_path)

st.markdown("---")
st.write("Developed with ❤️ using Streamlit and Librosa")
