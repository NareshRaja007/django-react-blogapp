import { useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Login = () => {
  const [formData, setFormData] = useState({
    user_id: "",
    password: "",
  });

  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
    setMessage(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.user_id || !formData.password) {
      setError("User ID and Password are required!");
      return;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}blog_app/login`, formData);
      setMessage("Login successful! Redirecting...");
      setError(null);

      // Store token (for later API calls)
      localStorage.setItem("token", response.data.data.token);
      
      // Redirect (if needed)
      setTimeout(() => {
        window.location.href = "/";
      }, 1500);
      
    } catch (err) {
      setError(err.response?.data?.message || "Invalid credentials! Try again.");
      setMessage(null);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-md border rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Login</h2>

      {message && <p className="text-green-500">{message}</p>}
      {error && <p className="text-red-500">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold">User ID <span className="text-red-500">*</span></label>
          <input
            type="text"
            name="user_id"
            value={formData.user_id}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block font-semibold">Password <span className="text-red-500">*</span></label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>

        <button type="submit" className="w-full p-2 bg-green-500 text-white rounded">Login</button>
      </form>
    </div>
  );
};

export default Login;
