import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import { MobileScoringPage } from './pages/MobileScoringPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { LeaderboardPage } from './pages/LeaderboardPage';

// Placeholder pages - will be implemented in future phases
const HomePage = () => <div>Home Page - Coming Soon</div>;
const LoginPage = () => <div>Login Page - Coming Soon</div>;

function App() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<AdminDashboardPage />} />
        <Route path="/leaderboard/:tournamentId" element={<LeaderboardPage />} />
        <Route path="/scoring/:roundId" element={<MobileScoringPage />} />
      </Routes>
    </Box>
  );
}

export default App;
