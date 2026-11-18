# 🌱 AgriCare AI – Smart Potato Farming Assistant

**An AI-powered platform designed to help potato farmers monitor crop health, detect diseases, and manage farming activities.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-brightgreen?style=for-the-badge)](https://agricare-ai.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=flat-square&logo=streamlit)](https://streamlit.io/)

## 🚀 Live Application

**Try AgriCare AI:** https://agricare-ai.streamlit.app/

## 📌 About the Project

AgriCare AI is a smart farming application focused on potato cultivation. It combines machine learning, AI assistance, and farm-management tools in one platform.

The application helps farmers identify common potato leaf diseases through image-based detection and organize important farming information.

## ✨ Key Features

### 1. AI-Based Potato Disease Detection
- Detects three potato leaf conditions:
  - Early Blight
  - Late Blight
  - Healthy
- Uses a trained CNN model.
- Displays prediction confidence and class probabilities.

### 2. Farmer Dashboard & Authentication
- Farmer registration and login.
- Secure password hashing.
- Personalized farmer dashboard.

### 3. Farm Management
- Add and manage farm details.
- Store crop information.
- Track potato varieties and crop stages.

### 4. Farming Records
- Disease scan history.
- Farm activity scheduling.
- Expense management.
- Harvest record management.

### 5. Smart Farming Assistance
- Weather information.
- Agricultural knowledge resources.
- AI-powered farming assistant.
- Notifications and farmer profile management.

## 🧠 Machine Learning Model

The disease detection module uses a Convolutional Neural Network (CNN) trained to classify potato leaf images into three categories.

| Class | Description |
|---|---|
| Early Blight | Detects early blight symptoms |
| Late Blight | Detects late blight symptoms |
| Healthy | Identifies healthy potato leaves |

**Model files:**
- `best_potato_model.keras`
- `potato_disease_model.keras`
- `class_names.json`

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend & Application | Streamlit |
| Machine Learning | TensorFlow / Keras |
| Image Processing | Pillow |
| Data Management | Pandas |
| Database | SQLite |
| AI Assistant | Google Gemini |
| Weather Data | Open-Meteo |
| Visualization | Plotly |
| Deployment | Streamlit Community Cloud |
| Version Control | Git & GitHub |

## 📂 Project Structure

```text
AgriCare-AI/
│
├── app.py
├── requirements.txt
│
├── agricare/
│   ├── components/
│   ├── database/
│   │   └── db.py
│   ├── pages/
│   ├── services/
│   └── utils/
│
├── models/
│   ├── best_potato_model.keras
│   ├── potato_disease_model.keras
│   └── class_names.json
│
└── Potato_Disease_Detection.ipynb
```

## ⚙️ Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Siddharths16code/AgriCare-AI.git
cd AgriCare-AI
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure Gemini API Key**

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

**5. Run the application**

```bash
streamlit run app.py
```

## 🔐 Security & Data

- Passwords are stored using PBKDF2-based hashing.
- API credentials are managed through Streamlit secrets.
- SQLite is used for application data storage.

Never commit API keys or private credentials to GitHub.

## 🌍 Deployment

AgriCare AI is deployed using Streamlit Community Cloud.

**Live URL:** https://agricare-ai.streamlit.app/

## 🎯 Project Objective

To make AI-powered agricultural assistance more accessible by combining crop disease detection, farm management, and intelligent farming support in a single platform.

## 👨‍💻 Developer

**Siddharth**

GitHub: [@Siddharths16code](https://github.com/Siddharths16code)

---

⭐ If you find this project useful, consider giving the repository a star!
