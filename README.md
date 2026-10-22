# 💰 AI Expense Tracker

An AI-powered expense tracking application that automatically extracts expense information from receipts and provides intelligent spending insights.

🚀 **Live Demo:** https://ai-expense-tracker-1-66xa.onrender.com
   **Demo login:** `demo@expensetracker.com` / `Demo1234!`

🔗 **Backend API:** https://ai-expense-tracker-ey3z.onrender.com

---

## 📌 Overview

AI Expense Tracker helps users manage their expenses by combining receipt analysis, secure authentication, database storage, and AI-powered spending analysis.

Users can:

- 🔐 Create an account and securely log in
- 📸 Upload a receipt image
- 🤖 Automatically extract expense information using AI
- 🏷️ Categorize expenses
- 💾 Store expenses in PostgreSQL
- 📊 View total and recent spending
- 🧠 Analyze spending patterns using LangChain and Groq
- 💡 Receive personalized spending insights and recommendations

--

## ✨ Features

### 🔐 User Authentication

- User registration and login
- JWT-based authentication
- Protected expense and AI endpoints
- User-specific expense data

### 📸 AI Receipt Analysis

Users upload a receipt image and the application extracts:

- Amount
- Category
- Description

The extracted expense is automatically saved to PostgreSQL.

### 📊 Expense Dashboard

The dashboard displays:

- Total spending
- Recent expenses
- Expense categories
- Transaction descriptions
- Expense count

### 🤖 AI Spending Analysis

The application analyzes the user's expenses and generates:

- Total spending
- Highest spending category
- Spending pattern insight
- Practical recommendation

### 🗄️ PostgreSQL Database

Expenses and users are stored in PostgreSQL.

Each expense is associated with the authenticated user.

---

# 🏗️ Architecture

```text
                 ┌──────────────────────┐
                 │    React Frontend    │
                 │                      │
                 │  Login               │
                 │  Dashboard           │
                 │  Receipt Upload      │
                 │  AI Analysis         │
                 └──────────┬───────────┘
                            │
                         REST API
                            │
                            ▼
                 ┌──────────────────────┐
                 │    FastAPI Backend   │
                 │                      │
                 │ Authentication       │
                 │ Expense Management   │
                 │ Receipt Processing   │
                 │ AI Analysis          │
                 └───────┬───────┬──────┘
                         │       │
                         ▼       ▼
              ┌──────────────┐  ┌─────────────────┐
              │ PostgreSQL   │  │    LangChain    │
              │              │  │        ↓        │
              │ Users        │  │      Groq       │
              │ Expenses     │  │        ↓        │
              └──────────────┘  │   AI Insights   │
                                └─────────────────┘
🧠 AI Architecture

The project uses LangChain to connect the application with the Groq LLM API.

Spending Analysis Flow
User Expenses
      ↓
FastAPI
      ↓
LangChain Prompt
      ↓
Groq LLM
      ↓
Structured JSON
      ↓
FastAPI
      ↓
React Dashboard

The application sends the user's expense information to the AI model with a structured prompt.

The model returns:

{
  "total_spending": 107.92,
  "top_category": "Shopping",
  "insight": "Most spending is concentrated in shopping.",
  "recommendation": "Set a weekly shopping budget."
}

The backend validates and returns this information to the React frontend.

🧾 Receipt Processing Flow
Receipt Image
      ↓
React Upload
      ↓
FastAPI
      ↓
Receipt AI Service
      ↓
Extract Amount / Category / Description
      ↓
PostgreSQL
      ↓
Dashboard Updated

This allows the user to upload a receipt instead of manually entering every expense.

🛠️ Tech Stack
Frontend
React
JavaScript
CSS
Vite
Backend
Python
FastAPI
SQLAlchemy
Uvicorn
Database
PostgreSQL
AI
LangChain
Groq API
Llama language model
Authentication
JWT
OAuth2 password flow
Deployment
Render
Development
Git
GitHub
Docker
Docker Compose

📁 Project Structure
AI-Expense-Tracker/
│
├── app/
│   ├── routers/
│   │   ├── users.py
│   │   ├── expenses.py
│   │   └── ai.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── receipt_service.py
│   │   └── langchain_service.py
│   │
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md

🔄 How the Application Works
1. User Login

The user logs in through the React frontend.

FastAPI validates the credentials and returns a JWT access token.

2. Dashboard

After authentication, the frontend uses the JWT token to access protected APIs.

3. Upload Receipt

The user uploads a receipt image.

The backend processes the image and extracts expense information using the AI receipt service.

4. Save Expense

The extracted information is stored in PostgreSQL and associated with the authenticated user.

5. Dashboard Update

The frontend reloads the user's expenses and displays the new transaction.

6. AI Spending Analysis

The user clicks Analyze My Spending.

The backend:

Retrieves the user's expenses
Converts them into structured text
Sends them through a LangChain prompt
Calls the Groq LLM
Parses the AI response
Returns structured spending insights
7. AI Recommendation

The AI provides a practical recommendation based on the user's spending pattern.

🔐 Environment Variables

Create a .env file locally:

DATABASE_URL=your_database_url
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key

For deployment, these values should be configured through the hosting platform's environment-variable settings.

⚠️ Never commit .env to GitHub.

The repository contains .env.example with placeholder values only.

💻 Local Development
Backend

Clone the repository:

git clone https://github.com/deebika-b/ai-expense-tracker.git
cd ai-expense-tracker

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure your .env file.

Start the backend:

uvicorn app.main:app --reload --port 8001

Backend will be available at:

http://127.0.0.1:8001

FastAPI documentation:

http://127.0.0.1:8001/docs

🎨 Frontend Development

Open another terminal:

cd frontend
npm install
npm run dev

Vite will provide the local frontend URL.

🐳 Docker

The project also includes Docker Compose configuration for running the application services during development.

docker compose up
☁️ Deployment

The application is deployed using Render.

Backend

FastAPI backend:

https://ai-expense-tracker-ey3z.onrender.com
Frontend

React frontend:

https://ai-expense-tracker-1-66xa.onrender.com

Environment variables are configured separately in the deployment environment.

🔒 Security

The application includes:

JWT authentication
Protected API endpoints
User-specific expense queries
Environment-based secret management
CORS configuration
Password hashing
.env excluded from Git

Sensitive credentials such as API keys, database passwords, and secret keys are not stored in the repository.

🎯 Future Improvements

Possible future improvements include:

📈 Spending charts and visualizations
📅 Monthly spending reports
🔔 Budget alerts
📱 Mobile-friendly enhancements
📄 PDF expense reports
🧠 More advanced spending predictions
💳 Multiple currency support
📊 Category-based analytics
🔍 Expense search and filtering

💼 What I Learned

This project helped me practice building a complete AI-powered full-stack application.

Key areas included:

Building REST APIs with FastAPI
React frontend development
JWT authentication
PostgreSQL database integration
SQLAlchemy ORM
Image/receipt processing
LangChain integration
LLM prompt engineering
Structured AI responses
API integration
CORS configuration
Docker
Git and GitHub
Cloud deployment
Environment-variable management
👩‍💻 Author

Deebika

Computer Science Engineer | Backend & AI Developer

Built with ❤️ using React, FastAPI, PostgreSQL, LangChain and Groq.

⭐ Project Highlights

AI-powered receipt extraction + expense management + personalized spending analysis in one full-stack application.


