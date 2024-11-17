import { useState, useEffect } from "react";
import { getLeaderboard } from "../api";

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState({
    user_leaderboard: [],
    pair_leaderboard: [],
  });

  // Fetch leaderboard data on component load
  useEffect(() => {
    fetchLeaderboard();
  }, []);

  // Function to fetch leaderboard data
  const fetchLeaderboard = async () => {
    try {
      const response = await getLeaderboard();
      setLeaderboard(response.data);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Leaderboard</h2>

      {/* User Leaderboard */}
      <h3 className="mt-4 font-semibold">User Leaderboard</h3>
      <ul>
        {leaderboard.user_leaderboard.map(([username, stats]) => (
          <li key={username} className="border p-2 mb-2">
            {username} - Wins: {stats.games_won}, Games Played: {stats.games_played}
          </li>
        ))}
      </ul>

      {/* Pair Leaderboard */}
      <h3 className="mt-4 font-semibold">Pair Leaderboard</h3>
      <ul>
        {leaderboard.pair_leaderboard.map(([pair, stats]) => (
          <li key={pair} className="border p-2 mb-2">
            {pair} - Wins: {stats.games_won}, Games Played: {stats.games_played}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;
