import { Routes, Route } from 'react-router-dom';
import { Container } from '@mui/material';

// Placeholder pages - will be implemented in Phase 2.4 and 2.5
const HomePage = () => <div>Home Page - Coming Soon</div>;
const LoginPage = () => <div>Login Page - Coming Soon</div>;
const DashboardPage = () => <div>Admin Dashboard - Coming Soon</div>;
const LeaderboardPage = () => <div>Live Leaderboard - Coming Soon</div>;
const ScoringPage = () => <div>Mobile Scoring UI - Coming Soon</div>;

function App() {
  return (
    <Container maxWidth="xl">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/leaderboard/:tournamentId" element={<LeaderboardPage />} />
        <Route path="/scoring/:roundId" element={<ScoringPage />} />
      </Routes>
    </Container>
  );
}

export default App;
