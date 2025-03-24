import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const MyPosts = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingPost, setEditingPost] = useState(null);
  const [updatedTitle, setUpdatedTitle] = useState("");
  const [updatedContent, setUpdatedContent] = useState("");

  useEffect(() => {
    fetchMyPosts();
  }, []);

  const fetchMyPosts = async () => {
    try {
      const response = await axiosInstance.get("my_posts");
      setPosts(response.data.data);
    } catch (error) {
      setError("Failed to load your posts");
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = (post) => {
    setEditingPost(post.id); // ✅ Ensure correct post_id is stored
    setUpdatedTitle(post.title);
    setUpdatedContent(post.content);
  };

  const handleUpdatePost = async () => {
    if (!editingPost) return;
    try {
      await axiosInstance.put("post_edit", {
        post_id: editingPost,  // ✅ Ensure post_id is passed
        title: updatedTitle,
        content: updatedContent,
      });
      setEditingPost(null);
      fetchMyPosts(); // Refresh after update
    } catch (error) {
      setError("Failed to update post");
    }
  };

  const handleDeletePost = async (postId) => {
    if (!window.confirm("Are you sure you want to delete this post?")) return;
    try {
      await axiosInstance.delete(`post_delete?post_id=${postId}`);
      fetchMyPosts(); // Refresh after deletion
    } catch (error) {
      setError("Failed to delete post");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">My Posts</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <ul className="space-y-4">
          {posts.map((post) => (
            <li key={post.id} className="border p-4 rounded-lg shadow bg-white">
              {editingPost === post.id ? (
                <div>
                  <input
                    type="text"
                    className="border p-2 w-full mb-2"
                    value={updatedTitle}
                    onChange={(e) => setUpdatedTitle(e.target.value)}
                  />
                  <textarea
                    className="border p-2 w-full mb-2"
                    value={updatedContent}
                    onChange={(e) => setUpdatedContent(e.target.value)}
                  />
                  <button
                    onClick={handleUpdatePost}
                    className="bg-blue-500 text-white px-4 py-2 rounded"
                  >
                    Update
                  </button>
                  <button
                    onClick={() => setEditingPost(null)}
                    className="ml-2 bg-gray-500 text-white px-4 py-2 rounded"
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <>
                  <h2 className="text-xl font-semibold text-blue-600">{post.title}</h2>
                  <p className="text-gray-700">{post.content}</p>
                  <button
                    onClick={() => handleEditClick(post)}
                    className="bg-yellow-500 text-white px-3 py-1 rounded mr-2"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeletePost(post.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded"
                  >
                    Delete
                  </button>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MyPosts;
