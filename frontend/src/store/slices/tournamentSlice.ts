/**
 * Redux slice for tournament management
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { tournamentsAPI, tournamentPlayersAPI } from '../../api/endpoints';
import type { Tournament, TournamentPlayer, TournamentPlayerRegistration } from '../../types';

interface TournamentState {
  tournaments: Tournament[];
  currentTournament: Tournament | null;
  tournamentPlayers: TournamentPlayer[];
  loading: boolean;
  saving: boolean;
  error: string | null;
  successMessage: string | null;
}

const initialState: TournamentState = {
  tournaments: [],
  currentTournament: null,
  tournamentPlayers: [],
  loading: false,
  saving: false,
  error: null,
  successMessage: null,
};

// Async thunks
export const fetchTournaments = createAsyncThunk(
  'tournament/fetchTournaments',
  async (_, { rejectWithValue }) => {
    try {
      const response = await tournamentsAPI.list();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch tournaments');
    }
  }
);

export const fetchTournament = createAsyncThunk(
  'tournament/fetchTournament',
  async (tournamentId: string, { rejectWithValue }) => {
    try {
      const response = await tournamentsAPI.get(tournamentId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch tournament');
    }
  }
);

export const createTournament = createAsyncThunk(
  'tournament/createTournament',
  async (data: Partial<Tournament>, { rejectWithValue }) => {
    try {
      const response = await tournamentsAPI.create(data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create tournament');
    }
  }
);

export const updateTournament = createAsyncThunk(
  'tournament/updateTournament',
  async ({ id, data }: { id: string; data: Partial<Tournament> }, { rejectWithValue }) => {
    try {
      const response = await tournamentsAPI.update(id, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update tournament');
    }
  }
);

export const deleteTournament = createAsyncThunk(
  'tournament/deleteTournament',
  async (tournamentId: string, { rejectWithValue }) => {
    try {
      await tournamentsAPI.delete(tournamentId);
      return tournamentId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to delete tournament');
    }
  }
);

export const fetchTournamentPlayers = createAsyncThunk(
  'tournament/fetchTournamentPlayers',
  async (tournamentId: string, { rejectWithValue }) => {
    try {
      const response = await tournamentsAPI.getPlayers(tournamentId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch tournament players');
    }
  }
);

export const registerPlayer = createAsyncThunk(
  'tournament/registerPlayer',
  async (
    { tournamentId, data }: { tournamentId: string; data: TournamentPlayerRegistration },
    { rejectWithValue }
  ) => {
    try {
      const response = await tournamentsAPI.registerPlayer(tournamentId, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to register player');
    }
  }
);

export const updateTournamentPlayer = createAsyncThunk(
  'tournament/updateTournamentPlayer',
  async (
    { id, data }: { id: string; data: Partial<TournamentPlayer> },
    { rejectWithValue }
  ) => {
    try {
      const response = await tournamentPlayersAPI.update(id, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update player');
    }
  }
);

export const withdrawPlayer = createAsyncThunk(
  'tournament/withdrawPlayer',
  async (playerId: string, { rejectWithValue }) => {
    try {
      await tournamentPlayersAPI.delete(playerId);
      return playerId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to withdraw player');
    }
  }
);

const tournamentSlice = createSlice({
  name: 'tournament',
  initialState,
  reducers: {
    clearCurrentTournament: (state) => {
      state.currentTournament = null;
      state.tournamentPlayers = [];
    },
    clearError: (state) => {
      state.error = null;
    },
    clearSuccessMessage: (state) => {
      state.successMessage = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch tournaments list
      .addCase(fetchTournaments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTournaments.fulfilled, (state, action: PayloadAction<Tournament[]>) => {
        state.loading = false;
        state.tournaments = action.payload;
      })
      .addCase(fetchTournaments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch single tournament
      .addCase(fetchTournament.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTournament.fulfilled, (state, action: PayloadAction<Tournament>) => {
        state.loading = false;
        state.currentTournament = action.payload;
      })
      .addCase(fetchTournament.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create tournament
      .addCase(createTournament.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(createTournament.fulfilled, (state, action: PayloadAction<Tournament>) => {
        state.saving = false;
        state.tournaments.unshift(action.payload);
        state.currentTournament = action.payload;
        state.successMessage = 'Tournament created successfully';
      })
      .addCase(createTournament.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      })
      // Update tournament
      .addCase(updateTournament.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(updateTournament.fulfilled, (state, action: PayloadAction<Tournament>) => {
        state.saving = false;
        const index = state.tournaments.findIndex((t) => t.id === action.payload.id);
        if (index !== -1) {
          state.tournaments[index] = action.payload;
        }
        state.currentTournament = action.payload;
        state.successMessage = 'Tournament updated successfully';
      })
      .addCase(updateTournament.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      })
      // Delete tournament
      .addCase(deleteTournament.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(deleteTournament.fulfilled, (state, action: PayloadAction<string>) => {
        state.saving = false;
        state.tournaments = state.tournaments.filter((t) => t.id !== action.payload);
        if (state.currentTournament?.id === action.payload) {
          state.currentTournament = null;
        }
        state.successMessage = 'Tournament deleted successfully';
      })
      .addCase(deleteTournament.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      })
      // Fetch tournament players
      .addCase(fetchTournamentPlayers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTournamentPlayers.fulfilled, (state, action: PayloadAction<TournamentPlayer[]>) => {
        state.loading = false;
        state.tournamentPlayers = action.payload;
      })
      .addCase(fetchTournamentPlayers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Register player
      .addCase(registerPlayer.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(registerPlayer.fulfilled, (state, action: PayloadAction<TournamentPlayer>) => {
        state.saving = false;
        state.tournamentPlayers.push(action.payload);
        state.successMessage = 'Player registered successfully';
      })
      .addCase(registerPlayer.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      })
      // Update tournament player
      .addCase(updateTournamentPlayer.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(updateTournamentPlayer.fulfilled, (state, action: PayloadAction<TournamentPlayer>) => {
        state.saving = false;
        const index = state.tournamentPlayers.findIndex((p) => p.id === action.payload.id);
        if (index !== -1) {
          state.tournamentPlayers[index] = action.payload;
        }
        state.successMessage = 'Player updated successfully';
      })
      .addCase(updateTournamentPlayer.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      })
      // Withdraw player
      .addCase(withdrawPlayer.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(withdrawPlayer.fulfilled, (state, action: PayloadAction<string>) => {
        state.saving = false;
        state.tournamentPlayers = state.tournamentPlayers.filter((p) => p.id !== action.payload);
        state.successMessage = 'Player withdrawn successfully';
      })
      .addCase(withdrawPlayer.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearCurrentTournament, clearError, clearSuccessMessage } = tournamentSlice.actions;
export default tournamentSlice.reducer;
