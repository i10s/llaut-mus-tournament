import axios from 'axios';

const API_BASE = "https://llaut-mus-backend.fly.dev";

export const getUsers = () => axios.get(`${API_BASE}/users/`);
export const registerUser = (username) => axios.post(`${API_BASE}/users/register/`, { username });

export const getPairs = () => axios.get(`${API_BASE}/pairs/`);
export const generatePairs = () => axios.post(`${API_BASE}/pairs/generate-random/`);
export const deletePair = (index) => axios.delete(`${API_BASE}/pairs/${index}/`);

export const getTournament = () => axios.get(`${API_BASE}/tournament/bracket/`);
export const createBracket = () => axios.post(`${API_BASE}/tournament/create-bracket/`);

export const getLeaderboard = () => axios.get(`${API_BASE}/stats/leaderboard/`);
