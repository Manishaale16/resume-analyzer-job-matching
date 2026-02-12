# 🚀 SmartResume AI - Advanced Resume Analyzer & Job Matcher

SmartResume AI is a professional, high-fidelity platform designed to give job seekers an unfair advantage in the hiring process. It uses a combination of **Local NLP (Natural Language Processing)** and **Machine Learning** to help you beat ATS systems and optimize your professional profile.

---

## ✨ Key Features

- **🛡️ ATS Optimization Engine**: Analyzes your resume against actual ATS protocols to ensure your document gets through the noise.
- **📉 Zero-Cost Local Analysis**: Built-in intelligent analysis using `spaCy` and `Scikit-learn`. Works perfectly without an internet connection or paid API keys.
- **🎯 Skill & Keyword Gap Analysis**: Detects exactly which technical and soft skills you are missing based on specific job descriptions.
- **📊 Professional Dashboard**: Track your optimization progress with match trend charts and skill radar maps.
- **📄 Dual Format Parsing**: Native support for high-precision text extraction from both `.pdf` and `.docx` files.
- **⚡ Interactive Platform Demo**: Experience the power of the AI with a simulated real-time scanning walkthrough.
- **💼 Job Matching Engine**: Instantly match your resume against a database of roles to see where you stand.
- **🔒 Secure & Private**: JWT-authenticated sessions and local file processing ensure your data remains yours.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Styling**: Tailwind CSS (Premium Glassmorphism Design)
- **Animations**: Framer Motion
- **Icons**: React Icons (Hi2, Fa)
- **Charts**: Recharts

### Backend
- **Core**: FastAPI (Python 3.9+)
- **Analysis**: spaCy (NLP), Scikit-learn (ML Similarity)
- **Database**: MongoDB (via Motor Async Driver)
- **Auth**: JWT (Python-Jose) & Passlib (Bcrypt)

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- MongoDB Atlas (or local MongoDB)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Configuration
Create a `.env` file in the `backend` folder:
```env
SECRET_KEY=yoursecretkeyhere
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=resume_analyzer
ALLOWED_ORIGINS=["http://localhost:3000"]
# OPENAI_API_KEY=optional_key_here (System will use local NLP if left empty)
```

---

## 🧠 How it Works

The system implements a **multi-stage analysis pipeline**:
1. **Text Extraction**: Cleanly extracts text from complex document layouts.
2. **Contextual Tokenization**: Uses `spaCy` to understand professional terminology and years of experience.
3. **Similarity Vectors**: Employs **TF-IDF Vectorization** and **Cosine Similarity** to quantify how well your resume matches the job description's context.
4. **Scoring Logic**: A weighted algorithm that balances skills (45%), experience (30%), and structural similarity (25%).

---

## 🤝 Support

For support, email [support@smartresume.ai](mailto:support@smartresume.ai) or visit our [Contact Page](http://localhost:3000/contact).

---

© 2026 SmartResume AI. Built for the modern job seeker.
