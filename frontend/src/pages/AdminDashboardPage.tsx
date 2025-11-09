/**
 * Admin Dashboard Page
 * Tournament management interface
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Grid,
  AppBar,
  Toolbar,
  Box,
  Snackbar,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import {
  fetchTournaments,
  createTournament,
  updateTournament,
  deleteTournament,
  clearError,
  clearSuccessMessage,
} from '../store/slices/tournamentSlice';
import { TournamentCard } from '../components/admin/TournamentCard';
import { TournamentForm } from '../components/admin/TournamentForm';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import type { Tournament } from '../types';

export const AdminDashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const { tournaments, loading, saving, error, successMessage } = useAppSelector(
    (state) => state.tournament
  );

  const [formOpen, setFormOpen] = useState(false);
  const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [tournamentToDelete, setTournamentToDelete] = useState<Tournament | null>(null);

  useEffect(() => {
    dispatch(fetchTournaments());
  }, [dispatch]);

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => {
        dispatch(clearSuccessMessage());
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage, dispatch]);

  const handleCreateClick = () => {
    setSelectedTournament(null);
    setFormOpen(true);
  };

  const handleEditClick = (tournament: Tournament) => {
    setSelectedTournament(tournament);
    setFormOpen(true);
  };

  const handleDeleteClick = (tournament: Tournament) => {
    setTournamentToDelete(tournament);
    setDeleteDialogOpen(true);
  };

  const handleFormClose = () => {
    setFormOpen(false);
    setSelectedTournament(null);
  };

  const handleFormSubmit = async (data: Partial<Tournament>) => {
    try {
      if (selectedTournament) {
        await dispatch(updateTournament({ id: selectedTournament.id, data })).unwrap();
      } else {
        await dispatch(createTournament(data)).unwrap();
      }
      handleFormClose();
    } catch (err) {
      console.error('Failed to save tournament:', err);
    }
  };

  const handleDeleteConfirm = async () => {
    if (tournamentToDelete) {
      try {
        await dispatch(deleteTournament(tournamentToDelete.id)).unwrap();
        setDeleteDialogOpen(false);
        setTournamentToDelete(null);
      } catch (err) {
        console.error('Failed to delete tournament:', err);
      }
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setTournamentToDelete(null);
  };

  const handleViewLeaderboard = (tournament: Tournament) => {
    navigate(`/leaderboard/${tournament.id}`);
  };

  const handleManagePlayers = (tournament: Tournament) => {
    navigate(`/admin/tournaments/${tournament.id}/players`);
  };

  if (loading && tournaments.length === 0) {
    return <LoadingSpinner message="Loading tournaments..." />;
  }

  return (
    <Box>
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Tournament Management
          </Typography>
          <Button color="inherit" startIcon={<AddIcon />} onClick={handleCreateClick}>
            Create Tournament
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {error && <ErrorAlert error={error} onClose={() => dispatch(clearError())} />}

        {tournaments.length === 0 ? (
          <Box textAlign="center" py={8}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No tournaments found
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Get started by creating your first tournament
            </Typography>
            <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreateClick}>
              Create Tournament
            </Button>
          </Box>
        ) : (
          <Grid container spacing={3}>
            {tournaments.map((tournament) => (
              <Grid item xs={12} sm={6} md={4} key={tournament.id}>
                <TournamentCard
                  tournament={tournament}
                  onEdit={handleEditClick}
                  onDelete={handleDeleteClick}
                  onViewLeaderboard={handleViewLeaderboard}
                  onManagePlayers={handleManagePlayers}
                />
              </Grid>
            ))}
          </Grid>
        )}
      </Container>

      {/* Tournament Form Dialog */}
      <TournamentForm
        open={formOpen}
        tournament={selectedTournament}
        onClose={handleFormClose}
        onSubmit={handleFormSubmit}
        loading={saving}
      />

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={handleDeleteCancel}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete "{tournamentToDelete?.name}"? This action cannot be
            undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} disabled={saving}>
            Cancel
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" disabled={saving}>
            {saving ? 'Deleting...' : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Success Snackbar */}
      <Snackbar
        open={!!successMessage}
        autoHideDuration={3000}
        onClose={() => dispatch(clearSuccessMessage())}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity="success" onClose={() => dispatch(clearSuccessMessage())}>
          {successMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};
