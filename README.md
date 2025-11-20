# **Voice-Integrated Gesture Recognition System**

A multimodal interaction system that combines voice commands and hand gestures to control computer actions. The project integrates real-time gesture recognition with a voice assistant to enable hands-free and seamless human–computer interaction.

---

##  Motivation & Overview

Traditional systems depend on physical input devices like a mouse and keyboard. This project introduces a more natural, accessible, and modern way of interacting with a computer.

By combining:
- Hand gesture–based cursor control  
- Voice-based system commands  

…the system enables quick, efficient, and hands-free navigation—especially useful for accessibility, productivity, and HCI research.

The goal is to build an intuitive system that naturally responds to human movement and speech.

---

##  Features

- Real-time hand gesture detection  
- Voice command recognition  
- Cursor control using hand gestures  
- Basic system actions via voice assistant  
- Combined gesture + voice multimodal control  
- Smooth and responsive interaction for most gestures  

---

##  Technologies Used

- **Python**
- **OpenCV** – Camera input & gesture processing  
- **MediaPipe** – Hand landmark detection  
- **SpeechRecognition** – Voice-to-text conversion  
- **PyAutoGUI** – Mouse & keyboard automation  

---

##  Project Structure

Voice-Integrated-Gesture-Recognition-System/
├── src/
│   ├── gesture_control.py      # Hand gesture detection + cursor control
│   ├── voice_assistant.py      # Voice command processing
│   └── main.py                 # Combined multimodal interaction pipeline
├── models/                     # ML models
├── data/                       # Training data
└── README.md



---

## ▶️ How to Run

### 1. Install dependencies

pip install opencv-python mediapipe SpeechRecognition pyautogui


### 2. Run the main application

python main.py


### 3. Use the system
- Show hand gestures to the webcam for cursor control  
- Speak commands like **"open browser"**, **"scroll down"**, **"close window"**, etc.  
- The system responds to both gesture and voice inputs  

---
