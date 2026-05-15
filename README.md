# 🧴 SkinCare AI

AI-powered skin analysis platform with disease detection, personalized skincare routines, and AI chatbot assistance.

## ✨ Features

- 🔬 **Disease Detection** - 85% accurate detection of 10 skin diseases
- 💆 **Skincare Analysis** - Personalized routines based on skin type (Dry/Normal/Oily)
- 💬 **AI Chatbot** - skincare advice with natural remedies
- 🌿 **Natural + Commercial Options** - Home remedies alongside product recommendations

## 🚀 Quick Setup

### Prerequisites

- **Python 3.12** - https://www.python.org/downloads/
- **Node.js 18+** - https://nodejs.org/
- **Git LFS** - https://git-lfs.github.com/ (for downloading models)

### Installation
```bash
# 1. Install Git LFS (one-time setup)
git lfs install

# 2. Clone repository (models will download automatically via Git LFS)
git clone https://github.com/yourusername/skincare-ai.git
cd skincare-ai

# Git LFS will automatically download model files (~2-3GB)
# This may take 5-10 minutes depending on your internet speed

# 3. Setup Backend
cd skincare-backend
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows
pip install -r requirements.txt

# 4. Setup Frontend
cd ../skincaref/skincare-app
npm install
```

### Running the Application

**Terminal 1 (Backend):**
```bash
cd skincare-backend
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd skincaref/skincare-app
npm run dev
```

**Access:**
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend API: http://localhost:5000
- ✅ Health Check: http://localhost:5000/health

## 📂 Project Structure
```
skincare-ai/
├── skincare-backend/           # Flask API
│   ├── models/                 # AI models (via Git LFS)
│   │   ├── final_ensemble_model_v2.pth/
│   │   └── skin_type_model.pth
│   ├── routes/                 # API endpoints
│   │   ├── disease.py
│   │   ├── skincare.py
│   │   └── chatbot_route.py
│   ├── utils/                  # Helper functions
│   ├── data/
│   │   └── skincare_knowledge.json
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
│
└── skincaref/
    └── skincare-app/           # React Frontend
        ├── src/
        │   ├── components/
        │   ├── services/
        │   └── App.jsx
        ├── package.json
        └── vite.config.js
```

## 🔧 Troubleshooting

### **Models not downloading?**

If models didn't download automatically:
```bash
# Pull LFS files manually
git lfs pull

# Verify models downloaded
ls -lh skincare-backend/models/
```

### **Git LFS not installed?**

Install Git LFS first:
- **Windows:** Download from https://git-lfs.github.com/
- **Mac:** `brew install git-lfs`
- **Linux:** `sudo apt-get install git-lfs`

Then run:
```bash
git lfs install
git lfs pull
```

### **"Module not found" error**

Make sure virtual environment is activated:
```bash
# You should see (venv) in your terminal
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### **Port already in use**
```bash
# Kill process on port 5000 or 5173
# Windows: taskkill /F /PID <PID>
# Mac/Linux: kill -9 <PID>
```

## 📊 Tech Stack

**Backend:**
- Flask (REST API)
- PyTorch 2.1 (Skin Type Classification - EfficientNetB3)
- RAG + Gemini Chatbot

**Frontend:**
- React 18
- Vite (Build tool)
- Axios (API client)
- Lucide React (Icons)
- Modern CSS (Custom styling)

**Models:**
- Disease Detection: 85% accuracy, 10 classes 
- Skin Type: 89% accuracy, 3 classes (Dry, Normal, Oily)
- Knowledge Base: 175+ Q&A pairs with natural remedies

## 🎯 Features in Detail

### Disease Detection
- Ensemble Model: EfficientNet-B3 + ResNet18
- Detects 10 skin conditions

### Skincare Analysis  
- AI-powered skin type detection
- Personalized routines (morning/evening/weekly)
- Natural, commercial, and home remedy options
- Lifestyle tips based on questionnaire

### AI Chatbot
- RAG + Gemini

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.


**Made with 💙**