import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Users from "./pages/Users";
import Pairs from "./pages/Pairs";
import Leaderboard from "./pages/Leaderboard";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<h1>Welcome to Llaut Mus Tournament!</h1>} />
        <Route path="/users" element={<Users />} />
        <Route path="/pairs" element={<Pairs />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </Router>
  );
}

export default App;
