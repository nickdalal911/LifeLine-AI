# 🔥 LifeLine AI – Burn Detection & Smart Medical Assistant

LifeLine AI is an AI-powered web application that detects burn severity from images and provides instant first-aid guidance using an intelligent chatbot.

🚀 **Live App:**
https://lifeline-ai-vedqqxqmsejirmza5x5rlzi.streamlit.app/

---

## 🧠 Features

* 🔍 **Burn Detection (AI Model)**
  Upload an image to detect burn type:

  * First Degree
  * Second Degree
  * Third Degree

* 🤖 **AI Chatbot Assistant**
  Get instant medical advice and first-aid guidance.

* 🚨 **Emergency Assistance Section**

  * Quick access to emergency guidance
  * Immediate steps for burn treatment
  * Helps users act fast in critical situations

* ⚡ **Real-Time Prediction**
  Fast and responsive results using deep learning.

* 📱 **Mobile-Friendly Interface**
  Works on both desktop and mobile browsers.

---

## 🚑 Emergency First-Aid Guide

If a burn occurs, follow these steps immediately:

1. 🧊 **Cool the burn**
   Hold under cool (not ice-cold) running water for 10–20 minutes

2. 🚫 **Avoid ice or toothpaste**
   These can worsen the injury

3. 🧴 **Cover the burn**
   Use a clean, non-stick cloth or sterile bandage

4. 💊 **Do not burst blisters**
   This increases risk of infection

5. 🏥 **Seek medical help if:**

   * Burn is severe (deep / large area)
   * On face, hands, or joints
   * Caused by chemicals or electricity

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Machine Learning:** TensorFlow / Keras
* **API:** OpenRouter (LLM for chatbot)
* **Model Hosting:** Google Drive (via gdown)

---

## 📂 Project Structure

```
LifeLine-AI/
│
├── app.py
├── chatbot.py
├── predict.py
├── requirements.txt
├── runtime.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/lifeline-ai.git
cd lifeline-ai
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add API Key

Create a `.streamlit/secrets.toml` file:

```
OPENROUTER_API_KEY = "your_api_key_here"
```

---

### 4. Run the app

```
streamlit run app.py
```

---

## 🧪 Model Details

* Model trained using deep learning for burn classification
* Stored externally (Google Drive) due to size limitations
* Automatically downloaded at runtime

---

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**.
It is **not a substitute for professional medical advice**.
Always consult a qualified healthcare provider for serious injuries.

---

## ⭐ Future Improvements

* 📍 Nearby hospital locator (Maps integration)
* 📊 Improved model accuracy & dataset expansion
* 💬 Advanced chatbot with medical knowledge base
* 📱 Native mobile app version

---

## 💡 Contribution

Feel free to fork the repo and improve the project!
Pull requests are welcome 🚀

---

