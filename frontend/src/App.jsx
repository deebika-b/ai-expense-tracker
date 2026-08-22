import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8001";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(
    localStorage.getItem("token") || ""
  );

  const [expenses, setExpenses] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (token) {
      loadExpenses(token);
    }
  }, [token]);

  async function login() {
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch(`${API}/users/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadExpenses(currentToken) {
    try {
      const response = await fetch(`${API}/expenses/`, {
        headers: {
          Authorization: `Bearer ${currentToken}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not load expenses"
        );
      }

      setExpenses(data);
    } catch (error) {
      setError(error.message);
    }
  }

  async function uploadReceipt() {
    if (!selectedFile) {
      setError("Please select a receipt image first.");
      return;
    }

    setError("");
    setSuccess("");
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API}/ai/receipt`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Receipt analysis failed"
        );
      }

      setSuccess(
        `Receipt added successfully: €${Number(
          data.expense.amount
        ).toFixed(2)}`
      );

      setSelectedFile(null);

      await loadExpenses(token);
    } catch (error) {
      setError(error.message);
    } finally {
      setUploading(false);
    }
  }

  async function analyzeSpending() {
    setError("");
    setSuccess("");
    setAnalyzing(true);

    try {
      const response = await fetch(`${API}/ai/analyze`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "AI analysis failed"
        );
      }

      setAnalysis(data.analysis);
    } catch (error) {
      setError(error.message);
    } finally {
      setAnalyzing(false);
    }
  }

  function logout() {
    localStorage.removeItem("token");

    setToken("");
    setExpenses([]);
    setAnalysis(null);
    setSelectedFile(null);
    setError("");
    setSuccess("");
  }

  const totalSpending = expenses.reduce(
    (total, expense) =>
      total + Number(expense.amount || 0),
    0
  );

  if (!token) {
    return (
      <div className="login-page">
        <div className="login-card">
          <div className="logo">💰</div>

          <h1>AI Expense Tracker</h1>

          <p className="subtitle">
            Smart expense tracking powered by AI
          </p>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              placeholder="Enter your password"
            />
          </div>

          <button
            className="primary-button full-width"
            onClick={login}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>💰 AI Expense Tracker</h1>
          <p>Smart spending, powered by AI</p>
        </div>

        <button
          className="logout-button"
          onClick={logout}
        >
          Logout
        </button>
      </header>

      <main className="dashboard">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            {success}
          </div>
        )}

        {/* TOTAL */}
        <section className="total-card">
          <div>
            <span>Total Spending</span>
            <h2>€{totalSpending.toFixed(2)}</h2>
          </div>

          <div className="total-icon">💳</div>
        </section>

        {/* RECEIPT */}
        <section className="card">
          <div className="card-header">
            <div>
              <h2>📸 Upload Receipt</h2>
              <p>
                Upload a receipt and let AI extract
                the expense automatically.
              </p>
            </div>
          </div>

          <div className="upload-area">
            <div className="upload-icon">📄</div>

            <input
              id="receipt"
              type="file"
              accept="image/*"
              onChange={(e) => {
                setSelectedFile(
                  e.target.files[0] || null
                );
                setError("");
                setSuccess("");
              }}
            />

            {selectedFile && (
              <p className="selected-file">
                📎 {selectedFile.name}
              </p>
            )}

            <button
              className="primary-button"
              onClick={uploadReceipt}
              disabled={uploading || !selectedFile}
            >
              {uploading
                ? "Analyzing Receipt..."
                : "Upload & Analyze Receipt"}
            </button>
          </div>
        </section>

        {/* EXPENSES */}
        <section className="card">
          <div className="card-header">
            <div>
              <h2>📊 Recent Expenses</h2>
              <p>Your latest transactions</p>
            </div>

            <span className="count-badge">
              {expenses.length}
            </span>
          </div>

          {expenses.length === 0 ? (
            <div className="empty-state">
              <span>🧾</span>
              <p>No expenses yet.</p>
              <small>
                Upload your first receipt to get started.
              </small>
            </div>
          ) : (
            <div className="expense-list">
              {expenses.map((expense) => (
                <div
                  className="expense-item"
                  key={expense.id}
                >
                  <div className="expense-info">
                    <div className="category-icon">
                      {expense.category === "Food"
                        ? "🍔"
                        : expense.category ===
                          "Shopping"
                        ? "🛍️"
                        : "💰"}
                    </div>

                    <div>
                      <strong>
                        {expense.category}
                      </strong>
                      <p>{expense.description}</p>
                    </div>
                  </div>

                  <strong className="expense-amount">
                    €{Number(expense.amount).toFixed(2)}
                  </strong>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* AI ANALYSIS */}
        <section className="card ai-card">
          <div className="card-header">
            <div>
              <h2>🤖 AI Spending Analysis</h2>
              <p>
                Get intelligent insights about your
                spending.
              </p>
            </div>
          </div>

          <button
            className="ai-button"
            onClick={analyzeSpending}
            disabled={analyzing}
          >
            {analyzing
              ? "🤖 Analyzing..."
              : "✨ Analyze My Spending"}
          </button>

          {analysis && (
            <div className="analysis-result">
              <div className="analysis-grid">
                <div className="analysis-box">
                  <span>Total Spending</span>
                  <strong>
                    €
                    {Number(
                      analysis.total_spending
                    ).toFixed(2)}
                  </strong>
                </div>

                <div className="analysis-box">
                  <span>Highest Spending Category</span>
                  <strong>
                    {analysis.top_category}
                  </strong>
                </div>
              </div>

              <div className="insight-box">
                <h3>💡 Insight</h3>
                <p>{analysis.insight}</p>
              </div>

              <div className="recommendation-box">
                <h3>🎯 Recommendation</h3>
                <p>{analysis.recommendation}</p>
              </div>
            </div>
          )}
        </section>
      </main>

      <footer>
        <p>
          AI Expense Tracker • React • FastAPI •
          PostgreSQL • LangChain
        </p>
      </footer>
    </div>
  );
}

export default App;