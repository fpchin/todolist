/**
 * Live Leaderboard Page
 * Real-time tournament leaderboard with OCB tiebreakers
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  AppBar,
  Toolbar,
  IconButton,
  Box,
  ToggleButtonGroup,
  ToggleButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Chip,
  Switch,
  FormControlLabel,
  Button,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import {
  fetchLeaderboard,
  setSelectedDivision,
  setSortBy,
  setAutoRefresh,
  clearLeaderboard,
  clearError,
} from '../store/slices/leaderboardSlice';
import { fetchTournament } from '../store/slices/tournamentSlice';
import { LeaderboardTable } from '../components/leaderboard/LeaderboardTable';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { websocketService } from '../services/websocket';

export const LeaderboardPage: React.FC = () => {
  const { tournamentId } = useParams<{ tournamentId: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const { currentTournament } = useAppSelector((state) => state.tournament);
  const {
    leaderboard,
    selectedDivision,
    sortBy,
    autoRefresh,
    refreshInterval,
    lastUpdated,
    loading,
    error,
  } = useAppSelector((state) => state.leaderboard);

  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    if (tournamentId) {
      dispatch(fetchTournament(tournamentId));
      dispatch(fetchLeaderboard(tournamentId));

      // Setup WebSocket for real-time updates
      const socket = websocketService.connect(tournamentId);
      setWsConnected(true);

      websocketService.subscribeToLeaderboard((data) => {
        console.log('Leaderboard updated:', data);
        dispatch(fetchLeaderboard(tournamentId));
      });

      websocketService.subscribeToScoreUpdate((data) => {
        console.log('Score updated:', data);
        dispatch(fetchLeaderboard(tournamentId));
      });

      return () => {
        websocketService.unsubscribeFromLeaderboard();
        websocketService.unsubscribeFromScoreUpdate();
        websocketService.disconnect();
        setWsConnected(false);
        dispatch(clearLeaderboard());
      };
    }
  }, [tournamentId, dispatch]);

  // Auto-refresh interval
  useEffect(() => {
    if (autoRefresh && tournamentId) {
      const interval = setInterval(() => {
        dispatch(fetchLeaderboard(tournamentId));
      }, refreshInterval * 1000);

      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval, tournamentId, dispatch]);

  const handleRefresh = () => {
    if (tournamentId) {
      dispatch(fetchLeaderboard(tournamentId));
    }
  };

  const handleBack = () => {
    navigate(-1);
  };

  const handleDivisionChange = (event: any) => {
    const value = event.target.value;
    dispatch(setSelectedDivision(value === 'all' ? null : value));
  };

  const handleSortByChange = (_event: React.MouseEvent<HTMLElement>, newValue: 'overall' | 'division') => {
    if (newValue !== null) {
      dispatch(setSortBy(newValue));
    }
  };

  const handleAutoRefreshToggle = (event: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setAutoRefresh(event.target.checked));
  };

  const handleExport = () => {
    // TODO: Implement CSV export
    console.log('Export leaderboard');
  };

  if (loading && !leaderboard) {
    return <LoadingSpinner message="Loading leaderboard..." />;
  }

  if (!currentTournament || !leaderboard) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <ErrorAlert error="Tournament or leaderboard not found" />
        <Button onClick={handleBack} startIcon={<ArrowBackIcon />}>
          Go Back
        </Button>
      </Container>
    );
  }

  // Get unique divisions
  const divisions = Array.from(new Set(leaderboard.entries.map((e) => e.division)));

  return (
    <Box>
      <AppBar position="sticky">
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={handleBack}>
            <ArrowBackIcon />
          </IconButton>
          <Box flexGrow={1}>
            <Typography variant="h6" noWrap>
              {currentTournament.name} - Leaderboard
            </Typography>
            <Typography variant="caption">
              {lastUpdated && `Updated: ${format(new Date(lastUpdated), 'HH:mm:ss')}`}
              {wsConnected && (
                <Chip
                  label="LIVE"
                  color="success"
                  size="small"
                  sx={{ ml: 1, height: 20 }}
                />
              )}
            </Typography>
          </Box>
          <Stack direction="row" spacing={1}>
            <IconButton color="inherit" onClick={handleRefresh} disabled={loading}>
              <RefreshIcon />
            </IconButton>
            <IconButton color="inherit" onClick={handleExport}>
              <DownloadIcon />
            </IconButton>
          </Stack>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 3, mb: 4 }}>
        {error && <ErrorAlert error={error} onClose={() => dispatch(clearError())} />}

        {/* Filters */}
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} mb={3} alignItems="center">
          <ToggleButtonGroup
            value={sortBy}
            exclusive
            onChange={handleSortByChange}
            aria-label="sort by"
            size="small"
          >
            <ToggleButton value="overall" aria-label="overall rank">
              Overall Rank
            </ToggleButton>
            <ToggleButton value="division" aria-label="division rank">
              Division Rank
            </ToggleButton>
          </ToggleButtonGroup>

          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Division</InputLabel>
            <Select
              value={selectedDivision || 'all'}
              label="Division"
              onChange={handleDivisionChange}
            >
              <MenuItem value="all">All Divisions</MenuItem>
              {divisions.map((division) => (
                <MenuItem key={division} value={division}>
                  {division}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box flexGrow={1} />

          <FormControlLabel
            control={
              <Switch
                checked={autoRefresh}
                onChange={handleAutoRefreshToggle}
                color="primary"
              />
            }
            label="Auto-refresh"
          />
        </Stack>

        {/* Leaderboard Table */}
        <LeaderboardTable
          entries={leaderboard.entries}
          showDivisionRank={sortBy === 'division'}
          selectedDivision={selectedDivision}
        />

        {/* Statistics */}
        <Box mt={3} p={2} bgcolor="background.paper" borderRadius={2}>
          <Typography variant="subtitle2" color="text.secondary">
            Total Players: {leaderboard.entries.length}
          </Typography>
          <Typography variant="subtitle2" color="text.secondary">
            Divisions: {divisions.join(', ')}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};
