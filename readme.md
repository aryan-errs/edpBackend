# Remote Health Service Kiosk

## Overview
The Remote Health Service Kiosk is designed to provide preliminary medical assessments in underserved areas. Utilizing advanced technologies, these kiosks connect users with healthcare professionals, enabling virtual consultations and preliminary diagnoses. The kiosks feature user-friendly interfaces and sophisticated data collection tools, ensuring accessibility and privacy for users in remote regions.

## Objective
The goal is to extend healthcare services to areas with limited access to medical facilities. These kiosks serve as decentralized hubs, offering timely diagnostic services through technology. Users can input vital health data, engage in video consultations, and receive data-driven assessments, empowering them to manage their health proactively and equitably.

## Tech Stack
- **Programming Language**: Python
- **Machine Learning Framework**: TensorFlow
- **Computer Vision Library**: OpenCV
- **Microcontroller Platform**: Raspberry Pi
- **Operating System**: Raspbian OS
- **Version Control**: Git
- **Pre-trained Model**: TensorFlow Object Detection Model

## Project Completion Status
1. Integrated language, speech, and computer vision models for technical pre-diagnosis.
2. Integrated heart rate and temperature sensors with Raspberry Pi.
3. Collected user symptom data and processed it through respective models.
4. Sent pre-diagnosis analysis to the frontend.
5. Provided diagnosis containing precautions, recommended medicines, and suggested doctors.

## LLM Model
Leveraging pre-trained models on medical literature, the system analyzes user-inputted symptoms through text or speech, inferring potential diseases and providing health-related inferences.

## CV Model
1. Image input from attached camera.
2. Trained on dataset from [dermaamin.com](https://www.dermaamin.com/site/).
3. Preprocessing includes normalization and data augmentation.
4. Utilizes ResNet50 for feature detection.
5. Achieved 94.37% accuracy in detecting 114 disease classes.

## Feedback Ensemble
A proposed RandomForest model works with the LLM to improve accuracy based on supervised feedback data, achieving 95% accuracy and 95.22% F1-score.
