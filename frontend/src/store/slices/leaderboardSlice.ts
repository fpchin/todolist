/**
 * Redux slice for leaderboard management
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { tournamentsAPI, resultsAPI } from '../../api/endpoints';
import type { LeaderboardResponse, Result } from '../../types';

interface LeaderboardState {
  leaderboard: LeaderboardResponse | null;
  results: Result[];
  selectedDivision: string | null;
  sortBy: 'overall' | 'division';
  autoRefresh: boolean;
  refreshInterval: number; // seconds
  lastUpdated: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: LeaderboardState = {
  leaderboard: null,
  results: [],
  selectedDivision: null,
  sortBy: 'overall',
  autoRefresh: false,
  refreshInterval: 30, // 30 seconds default
  lastUpdated: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchLeaderboard = createAsyncThunk(
  'leaderboard/fetchLeaderboard',
  async (tournamentId: string, { rejectWithValue }) => {
    try {
      const response = await tournamentsAPI.getLeaderboard(tournamentId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch leaderboard');
    }
  }
);

export const fetchResults = createAsyncThunk(
  'leaderboard/fetchResults',
  async (params: { tournamentId: string; division?: string }, { rejectWithValue }) => {
    try {
      const response = await resultsAPI.list({
        tournament: params.tournamentId,
        division: params.division,
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch results');
    }
  }
);

export const calculateResults = createAsyncThunk(
  'leaderboard/calculateResults',
  async (tournamentId: string, { rejectWithValue }) => {
    try {
      const response = await resultsAPI.calculate(tournamentId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to calculate results');
    }
  }
);

const leaderboardSlice = createSlice({
  name: 'leaderboard',
  initialState,
  reducers: {
    setSelectedDivision: (state, action: PayloadAction<string | null>) => {
      state.selectedDivision = action.payload;
    },
    setSortBy: (state, action: PayloadAction<'overall' | 'division'>) => {
      state.sortBy = action.payload;
    },
    setAutoRefresh: (state, action: PayloadAction<boolean>) => {
      state.autoRefresh = action.payload;
    },
    setRefreshInterval: (state, action: PayloadAction<number>) => {
      state.refreshInterval = action.payload;
    },
    clearLeaderboard: (state) => {
      state.leaderboard = null;
      state.results = [];
      state.lastUpdated = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch leaderboard
      .addCase(fetchLeaderboard.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLeaderboard.fulfilled, (state, action: PayloadAction<LeaderboardResponse>) => {
        state.loading = false;
        state.leaderboard = action.payload;
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(fetchLeaderboard.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch results
      .addCase(fetchResults.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchResults.fulfilled, (state, action: PayloadAction<Result[]>) => {
        state.loading = false;
        state.results = action.payload;
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(fetchResults.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Calculate results
      .addCase(calculateResults.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(calculateResults.fulfilled, (state, action: PayloadAction<Result[]>) => {
        state.loading = false;
        state.results = action.payload;
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(calculateResults.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setSelectedDivision,
  setSortBy,
  setAutoRefresh,
  setRefreshInterval,
  clearLeaderboard,
  clearError,
} = leaderboardSlice.actions;
export default leaderboardSlice.reducer;
