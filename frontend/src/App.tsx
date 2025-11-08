import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import { MobileScoringPage } from './pages/MobileScoringPage';

// Placeholder pages - will be implemented in Phase 2.5
const HomePage = () => <div>Home Page - Coming Soon</div>;
const LoginPage = () => <div>Login Page - Coming Soon</div>;
const DashboardPage = () => <div>Admin Dashboard - Coming Soon</div>;
const LeaderboardPage = () => <div>Live Leaderboard - Coming Soon</div>;

function App() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/leaderboard/:tournamentId" element={<LeaderboardPage />} />
        <Route path="/scoring/:roundId" element={<MobileScoringPage />} />
      </Routes>
    </Box>
  );
}

export default App;
