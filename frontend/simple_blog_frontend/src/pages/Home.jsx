"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import AllUsers from "./Allusers";
import CreatePost from "./CreatePost";
import MyPosts from "./Myposts";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Home = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState("posts"); // Default: Show all posts
  const [formData, setFormData] = useState({ user_id: "", password: "", name: "", contact_number: "" });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMessage, setAuthMessage] = useState(null);
  const [authError, setAuthError] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    checkAuth();
    fetchPosts();
  }, []);

  const checkAuth = () => {
    const token = localStorage.getItem("access");
    if (token) {
      setIsAuthenticated(true);
      setUser(JSON.parse(localStorage.getItem("user")));
    }
  };

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}all_posts`);
      setPosts(response.data.data.data);
    } catch (error) {
      console.error("Error fetching blog posts:", error);
      setError("Failed to load blog posts");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setAuthError(null);
    setAuthMessage(null);
  };

  const validateForm = (isSignup = false) => {
    const { user_id, password, name, contact_number } = formData;

    if (!user_id || !password) {
      setAuthError("User ID and Password are required!");
      return false;
    }

    if (isSignup) {
      if (!name || !contact_number) {
        setAuthError("All fields are required for signup!");
        return false;
      }
      if (!/^\d{10}$/.test(contact_number)) {
        setAuthError("Mobile number must be exactly 10 digits!");
        return false;
      }
      if (password.length < 6) {
        setAuthError("Password must be at least 6 characters!");
        return false;
      }
    }

    return true;
  };

  const handleAuth = async (endpoint) => {
    if (!validateForm(endpoint === "register")) return;

    try {
      const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData);
      setAuthMessage(endpoint === "login" ? "Login successful!" : "Signup successful! You can now log in.");
      setAuthError(null);

      if (endpoint === "login") {
        localStorage.setItem("access", response.data.data.access);
        localStorage.setItem("refresh", response.data.data.refresh);
        localStorage.setItem("user", JSON.stringify(response.data.data.user));
        setIsAuthenticated(true);
        setUser(response.data.data.user);
        setView("posts");
        fetchPosts();
      } else {
        setView("login");
      }
    } catch (error) {
      setAuthError(error.response?.data?.message || `Failed to ${endpoint}, please try again.`);
      setAuthMessage(null);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    setIsAuthenticated(false);
    setUser(null);
    setView("posts");
  };

  return (
    <div className="container mx-auto p-4">
      {/* Navigation Bar */}
      <nav className="flex justify-between items-center mb-4 p-4 bg-gray-100 rounded-lg shadow">
        <h1 className="text-2xl font-bold">Blog Posts</h1>
        <div>
          {isAuthenticated ? (
            <>
              <button onClick={() => setView("createPost")} className="mr-4 text-blue-500 font-semibold">Create Post</button>
              <button onClick={() => setView("myPosts")} className="mr-4 text-purple-500 font-semibold">My Posts</button>
              <button onClick={() => setView("users")} className="mr-4 text-green-500 font-semibold">All Users</button>
              <button onClick={handleLogout} className="text-red-500 font-semibold">Logout</button>
            </>
          ) : (
            <>
              <button onClick={() => setView("signup")} className="mr-4 text-blue-500 font-semibold">Signup</button>
              <button onClick={() => setView("login")} className="text-green-500 font-semibold">Login</button>
            </>
          )}
        </div>
      </nav>

      {/* Authentication Forms */}
      {view === "signup" && (
        <div className="p-4 mb-4 bg-white shadow rounded">
          <h2 className="text-xl font-semibold mb-2">Signup</h2>
          {authMessage && <p className="text-green-500">{authMessage}</p>}
          {authError && <p className="text-red-500">{authError}</p>}

          <input type="text" name="user_id" placeholder="User ID" onChange={handleInputChange} className="border p-2 w-full mb-2" />
          <input type="text" name="name" placeholder="Name" onChange={handleInputChange} className="border p-2 w-full mb-2" />
          <input type="text" name="contact_number" placeholder="Contact Number" onChange={handleInputChange} className="border p-2 w-full mb-2" />
          <input type="password" name="password" placeholder="Password" onChange={handleInputChange} className="border p-2 w-full mb-2" />
          
          <button onClick={() => handleAuth("register")} className="bg-blue-500 text-white p-2 w-full">Signup</button>
        </div>
      )}

      {view === "login" && (
        <div className="p-4 mb-4 bg-white shadow rounded">
          <h2 className="text-xl font-semibold mb-2">Login</h2>
          {authMessage && <p className="text-green-500">{authMessage}</p>}
          {authError && <p className="text-red-500">{authError}</p>}

          <input type="text" name="user_id" placeholder="User ID" onChange={handleInputChange} className="border p-2 w-full mb-2" />
          <input type="password" name="password" placeholder="Password" onChange={handleInputChange} className="border p-2 w-full mb-2" />
          
          <button onClick={() => handleAuth("login")} className="bg-green-500 text-white p-2 w-full">Login</button>
        </div>
      )}

      {/* Blog Posts Section */}
      {view === "posts" && (
        <>
          {loading ? <p className="text-center text-gray-500">Loading...</p> : posts.length === 0 ? <p className="text-center text-gray-500">No blog posts found.</p> :
            <ul className="space-y-4">{posts.map((post) => (
              <li key={post.id} className="border p-4 rounded-lg shadow bg-white">
                <h2 className="text-xl font-semibold text-blue-600">{post.title}</h2>
                <p className="text-gray-700">{post.content}</p>
              </li>
            ))}</ul>}
        </>
      )}

      {view === "users" && <AllUsers />}
      {view === "createPost" && <CreatePost />}
      {view === "myPosts" && <MyPosts />}
    </div>
  );
};

export default Home;
