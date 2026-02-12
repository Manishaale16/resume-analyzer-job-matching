# 🚀 SmartResume AI - Advanced Resume Analyzer & Job Matcher

SmartResume AI is a professional, high-fidelity platform designed to give job seekers an unfair advantage in the hiring process. It uses a combination of **Local NLP (Natural Language Processing)** and **Machine Learning** to help you beat ATS systems and optimize your professional profile.


![image alt](https://github.com/Manishaale16/resume-analyzer-job-matching/blob/51fb75c7c13dec4f5d7f0a1ede46145e34b74201/Screenshot%202026-02-12%20094003.png)

---

## 📸 Screenshots


| Upload & Analysis | Professional Dashboard |
|:---:|:---:|
| ![Upload](screenshots/upload.png) | ![Dashboard](screenshots/dashboard.png) |

---

## 🔗 Live Demo
[Coming Soon - Stay Tuned!]

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

## 🏗️ System Architecture

```text
       +-------------------+          +-----------------------+
       |   Next.js Client  | <------> |   FastAPI Backend     |
       |  (Framer Motion)  |   JWT    |  (Python/Async/CORS)  |
       +---------+---------+          +-----------+-----------+
                 ^                               |
                 |                               v
       +---------+---------+          +-----------------------+
       | MongoDB Atlas DB  | <------> |  AI/NLP Engine        |
       | (Analysis History)|          | (spaCy & Scikit-learn)|
       +-------------------+          +-----------------------+
```

---

## � Project Folder Structure

```text
Resume_analyzer/
├── frontend/                 # Next.js Application
│   ├── public/               # Static Assets
│   └── src/
│       ├── app/              # App Router Pages
│       ├── components/       # Reusable UI Components
│       ├── context/          # Auth State Management
│       └── styles/           # Tailwind Config
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # API Route Controllers
│   │   ├── core/             # JWT/Config/Security
│   │   ├── models/           # Pydantic Schemas
│   │   └── services/         # NLP & DB Logic
│   ├── uploads/              # Temp File Storage
│   └── requirements.txt      # Python Dependencies
├── .gitignore                # Global Ignore Config
└── README.md                 # Documentation
```

---

## �🛠️ Tech Stack

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

## � Core API Endpoints

| Method | Endpoint | Description | Auth Required |
|:---|:---|:---|:---|
| `POST` | `/api/auth/register` | User account registration | No |
| `POST` | `/api/auth/login` | JWT token acquisition | No |
| `POST` | `/api/resumes/analyze` | Upload and analyze resume against JD | (Optional) |
| `GET` | `/api/resumes/history` | Retrieve user analysis history | Yes |
| `POST` | `/api/jobs/match` | Match resume against mock job database | No |
| `GET` | `/api/users/me` | Fetch current profile info | Yes |

---

## �🚀 Getting Started

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
# OPENAI_API_KEY=optional (System will use local NLP if left empty)
```

---

## 🧠 How it Works

The system implements a **multi-stage analysis pipeline**:
1. **Text Extraction**: Cleanly extracts text from complex document layouts.
2. **Contextual Tokenization**: Uses `spaCy` to understand professional terminology and years of experience.
3. **Similarity Vectors**: Employs **TF-IDF Vectorization** and **Cosine Similarity** to quantify how well your resume matches the job description's context.
4. **Scoring Logic**: A weighted algorithm that balances skills (45%), experience (30%), and structural similarity (25%).

---

## 🛡️ Security & Privacy

Privacy is a core tenet of SmartResume AI:
- **Data Protection**: Resumes are processed in volatile memory. If saved to history, they are stored in an encrypted database instance.
- **Local Analysis**: Leveraging local NLP means your resume content isn't unnecessarily sent to third-party AI companies unless you opt-in for LLM features.
- **Secure Sessions**: Authentication is handled via stateless JWT tokens with periodic expiry.

---

## 🔮 Future Enhancements

- [ ] **AI Interview Prep**: Generate custom interview questions based on detected skill gaps.
- [ ] **Resume Rewriter**: Direct integration with LLMs to suggest bullet point rewrites.
- [ ] **Multi-user Teams**: Dashboard for recruiters to rank batches of resumes.
- [ ] **Cloud Storage**: Integration with Google Drive and Dropbox for easy uploads.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.



## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.



<<<<<<< HEAD
[def]: image.png
=======
[def]: image.png
>>>>>>> 47099f4ab2d2e9e89b333ca3849cab578207a875
