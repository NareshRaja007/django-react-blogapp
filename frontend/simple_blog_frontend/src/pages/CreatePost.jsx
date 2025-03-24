import { useState } from "react";
import axiosInstance from "../axiosInstance";

const CreatePost = () => {
  const [formData, setFormData] = useState({ title: "", content: "" });
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
    setMessage(null);
  };

  const handleSubmit = async () => {
    try {
      const response = await axiosInstance.post("post_create", formData);
      setMessage("Post created successfully!");
      setFormData({ title: "", content: "" });
    } catch (error) {
      setError(error.response?.data?.message || "Failed to create post");
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold">Create Post</h2>
      {message && <p className="text-green-500">{message}</p>}
      {error && <p className="text-red-500">{error}</p>}

      <input type="text" name="title" placeholder="Title" onChange={handleInputChange} className="border p-2 w-full mb-2" />
      <textarea name="content" placeholder="Content" onChange={handleInputChange} className="border p-2 w-full mb-2"></textarea>

      <button onClick={handleSubmit} className="bg-blue-500 text-white p-2 w-full">Create</button>
    </div>
  );
};

export default CreatePost;
