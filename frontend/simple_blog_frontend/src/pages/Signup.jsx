import { useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Signup = () => {
  const [formData, setFormData] = useState({
    user_id: "",
    name: "",
    contact_number: "",
    password: "",
  });

  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  // Validation function
  const validateForm = () => {
    const { user_id, name, contact_number, password } = formData;

    if (!user_id || !name || !contact_number || !password) {
      setError("All fields are required!");
      return false;
    }

    if (!/^\d{10}$/.test(contact_number)) {
      setError("Mobile number must be exactly 10 digits!");
      return false;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long!");
      return false;
    }

    return true;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
    setMessage(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    try {
      const response = await axios.post(`${API_BASE_URL}blog_app/register`, formData);
      setMessage("Signup successful! You can now log in.");
      setError(null);
      setFormData({ user_id: "", name: "", contact_number: "", password: "" }); // Reset form
    } catch (err) {
      setError(err.response?.data?.message || "Signup failed! Try again.");
      setMessage(null);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-md border rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Signup</h2>

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
          <label className="block font-semibold">Name <span className="text-red-500">*</span></label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block font-semibold">Mobile Number <span className="text-red-500">*</span></label>
          <input
            type="text"
            name="contact_number"
            value={formData.contact_number}
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

        <button type="submit" className="w-full p-2 bg-blue-500 text-white rounded">Signup</button>
      </form>
    </div>
  );
};

export default Signup;
