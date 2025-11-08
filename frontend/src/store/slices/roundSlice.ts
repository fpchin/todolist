/**
 * Redux slice for round management
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { roundsAPI } from '../../api/endpoints';
import type { Round } from '../../types';

interface RoundState {
  currentRound: Round | null;
  rounds: Round[];
  loading: boolean;
  error: string | null;
}

const initialState: RoundState = {
  currentRound: null,
  rounds: [],
  loading: false,
  error: null,
};

// Async thunks
export const fetchRound = createAsyncThunk(
  'round/fetchRound',
  async (roundId: string, { rejectWithValue }) => {
    try {
      const response = await roundsAPI.get(roundId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch round');
    }
  }
);

export const fetchRounds = createAsyncThunk(
  'round/fetchRounds',
  async (tournamentId: string, { rejectWithValue }) => {
    try {
      const response = await roundsAPI.list({ tournament: tournamentId });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch rounds');
    }
  }
);

const roundSlice = createSlice({
  name: 'round',
  initialState,
  reducers: {
    clearCurrentRound: (state) => {
      state.currentRound = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch single round
      .addCase(fetchRound.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRound.fulfilled, (state, action: PayloadAction<Round>) => {
        state.loading = false;
        state.currentRound = action.payload;
      })
      .addCase(fetchRound.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch rounds list
      .addCase(fetchRounds.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRounds.fulfilled, (state, action: PayloadAction<Round[]>) => {
        state.loading = false;
        state.rounds = action.payload;
      })
      .addCase(fetchRounds.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearCurrentRound, clearError } = roundSlice.actions;
export default roundSlice.reducer;
