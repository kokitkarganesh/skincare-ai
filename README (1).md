# 🌿 SkinCare AI

An intelligent skincare platform built as a Final Year BE Project. Upload a skin image to detect diseases, get a personalized skincare routine based on your skin type, or chat with our AI assistant for expert skincare guidance.

---

---

## ✨ What It Does

| Feature | Description |
|---|---|
| 🔬 Disease Detection | Detects 10 skin conditions with 85% accuracy using an ensemble deep learning model |
| 💆 Skincare Analysis | Classifies skin type (Dry / Normal / Oily) and generates morning, evening & weekly routines |
| 💬 AI Assistant | RAG-powered chatbot using Google Gemini with 175+ expert Q&A pairs |
| 🌿 Remedy Options | Every recommendation includes commercial, natural, and home remedy alternatives |

---

## 🛠️ Tech Stack

**Backend**
- Python / Flask
- PyTorch 2.1
- EfficientNet-B3 + ResNet18 (Ensemble) — Disease Detection
- EfficientNet-B0 — Skin Type Classification
- FAISS + Google Gemini — RAG Chatbot

**Frontend**
- React 18 + Vite
- Axios
- Lucide React
- Custom CSS

---

## 📂 Project Structure

```
skincare-ai/
├── Skin-care_Backend/
│   ├── models/                  # AI model weights (via Git LFS)
│   │   ├── final_ensemble_model_v2.pth
│   │   └── skin_type_model.pth
│   ├── routes/
│   │   ├── disease.py
│   │   ├── skincare.py
│   │   └── chatbot_route.py
│   ├── utils/
│   ├── data/
│   │   └── skincare_knowledge.json
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
│
└── skincaref/
    └── skincare-app/
        ├── src/
        │   ├── components/
        │   ├── services/
        │   └── App.jsx
        ├── package.json
        └── vite.config.js
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.12
- Node.js 18+
- Git LFS — required to download model files

### 1. Install Git LFS
```bash
git lfs install
```

### 2. Clone the Repository
```bash
git clone https://github.com/kokitkarganesh/skincare-ai.git
cd skincare-ai
```
> Model files (~111 MB) will download automatically via Git LFS.

### 3. Backend Setup
```bash
cd Skin-care_Backend
python -m venv venv

# Activate virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 4. Frontend Setup
```bash
cd ../skincaref/skincare-app
npm install
```

---

## ▶️ Running the App

Open **two terminals**:

**Terminal 1 — Backend**
```bash
cd Skin-care_Backend
venv\Scripts\activate        # Windows
python app.py
```

**Terminal 2 — Frontend**
```bash
cd skincaref/skincare-app
npm run dev
```

---

## 🔧 Troubleshooting

**Models not found after cloning?**
```bash
git lfs pull
```

**"Module not found" error?**
Make sure your virtual environment is activated — you should see `(venv)` at the start of your terminal line.

**Port already in use?**
```bash
# Windows
taskkill /F /PID <PID>
```

---

## 📊 Model Performance

| Model | Accuracy | Classes |
|---|---|---|
| Disease Detection (EfficientNet-B3 + ResNet18) | 85% | 10 skin conditions |
| Skin Type Classification (EfficientNet-B0) | 89% | Dry, Normal, Oily |

---

## 👨‍💻 Team

Final Year BE Project — Computer Engineering, Mumbai University

---


