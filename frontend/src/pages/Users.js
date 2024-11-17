import { useState, useEffect } from 'react';
import { getUsers, registerUser } from '../api';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState('');

  useEffect(() => {
    getUsers().then((response) => setUsers(response.data.users));
  }, []);

  const handleRegister = () => {
    registerUser(username).then(() => {
      setUsers((prev) => [...prev, username]);
      setUsername('');
    });
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user}>{user}</li>
        ))}
      </ul>
      <div className="mt-4">
        <input
          className="border p-2 mr-2"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
        />
        <button className="bg-blue-600 text-white px-4 py-2" onClick={handleRegister}>
          Register User
        </button>
      </div>
    </div>
  );
};

export default Users;
