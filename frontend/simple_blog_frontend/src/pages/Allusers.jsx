import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const AllUsers = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axiosInstance.get("users");
      setUsers(response.data.data);
    } catch (error) {
      setError(error.response?.data?.message || "Failed to load users");
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold">All Users</h2>
      {error ? <p className="text-red-500">{error}</p> :
        <ul className="space-y-2">
          {users.map((user) => (
            <li key={user.id} className="border p-2 rounded">{user.name} ({user.contact_number})</li>
          ))}
        </ul>}
    </div>
  );
};

export default AllUsers;
