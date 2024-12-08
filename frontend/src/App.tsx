import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Auth from "./pages/Auth";
import Generate from "./pages/Generate";
import "./assets/styles.css";


const App: React.FC = () => (
  <Router>
    <Routes>
      <Route
        path="/login"
        element={<Auth />}
      />
      <Route
        path="/generate"
        element={<Generate />}
      />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  </Router>
);

export default App;
