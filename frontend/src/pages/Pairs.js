import { useState, useEffect } from "react";
import { getPairs, generatePairs, deletePair } from "../api";

const Pairs = () => {
  const [pairs, setPairs] = useState([]);

  // Fetch pairs on component load
  useEffect(() => {
    fetchPairs();
  }, []);

  // Function to fetch pairs from the backend
  const fetchPairs = async () => {
    try {
      const response = await getPairs();
      setPairs(response.data.pairs);
    } catch (error) {
      console.error("Error fetching pairs:", error);
    }
  };

  // Function to generate random pairs
  const handleGeneratePairs = async () => {
    try {
      await generatePairs();
      fetchPairs(); // Refresh the list
    } catch (error) {
      console.error("Error generating pairs:", error);
    }
  };

  // Function to delete a pair by index
  const handleDeletePair = async (index) => {
    try {
      await deletePair(index);
      fetchPairs(); // Refresh the list
    } catch (error) {
      console.error("Error deleting pair:", error);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Pairs</h2>
      <button
        className="bg-green-600 text-white px-4 py-2 mb-4"
        onClick={handleGeneratePairs}
      >
        Generate Random Pairs
      </button>
      <ul>
        {pairs.map((pair, index) => (
          <li key={index} className="flex justify-between items-center border p-2 mb-2">
            <span>
              {pair[0]} {pair[1] ? `& ${pair[1]}` : "(Waiting for partner)"}
            </span>
            <button
              className="bg-red-600 text-white px-4 py-2"
              onClick={() => handleDeletePair(index)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Pairs;
