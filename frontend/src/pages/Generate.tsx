import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generateText, logout, GenerateResponse } from "../utils/api";

const Generate: React.FC = () => {
  const [text, setText] = useState<string>("");
  const [output, setOutput] = useState<GenerateResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const navigate = useNavigate();

  const handleGenerate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await generateText(text);
      setOutput(response);
    } catch (err: any) {
      setError(err.message || "Failed to generate");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/login");
    } catch (err: any) {
      setError(err.message || "Failed to logout");
    }
  };

  return (
    <div className="generate-container">
      <div className="header">
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
        <h1>Generate Text</h1>
      </div>
      <form onSubmit={handleGenerate}>
        <textarea
          placeholder="Enter your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {output && (
        <div className="output">
          <h2>Output</h2>
          <p><strong>ID:</strong> {output.id}</p>
          <p>
            <strong>Link:</strong>{" "}
            <a href={output.link} target="_blank" rel="noopener noreferrer">
              {output.link}
            </a>
          </p>
          <p><strong>Text:</strong> {output.text}</p>
          <p><strong>Status:</strong> {output.status}</p>
        </div>
      )}
    </div>
  );
};

export default Generate;