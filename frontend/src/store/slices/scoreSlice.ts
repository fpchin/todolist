/**
 * Redux slice for score management
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { holeScoresAPI } from '../../api/endpoints';
import type { HoleScore, BulkHoleScoresRequest } from '../../types';

interface ScoreState {
  holeScores: HoleScore[];
  currentScores: number[]; // 18 hole scores being entered
  loading: boolean;
  saving: boolean;
  error: string | null;
  lastSaved: string | null;
}

const initialState: ScoreState = {
  holeScores: [],
  currentScores: Array(18).fill(0),
  loading: false,
  saving: false,
  error: null,
  lastSaved: null,
};

// Async thunks
export const fetchHoleScores = createAsyncThunk(
  'score/fetchHoleScores',
  async ({ roundId, playerId }: { roundId: string; playerId: string }, { rejectWithValue }) => {
    try {
      const response = await holeScoresAPI.list({ round: roundId, player: playerId });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch scores');
    }
  }
);

export const saveBulkHoleScores = createAsyncThunk(
  'score/saveBulkHoleScores',
  async (data: BulkHoleScoresRequest, { rejectWithValue }) => {
    try {
      const response = await holeScoresAPI.bulkCreate(data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to save scores');
    }
  }
);

export const updateHoleScore = createAsyncThunk(
  'score/updateHoleScore',
  async ({ id, data }: { id: string; data: Partial<HoleScore> }, { rejectWithValue }) => {
    try {
      const response = await holeScoresAPI.update(id, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update score');
    }
  }
);

const scoreSlice = createSlice({
  name: 'score',
  initialState,
  reducers: {
    setHoleScore: (state, action: PayloadAction<{ holeIndex: number; strokes: number }>) => {
      const { holeIndex, strokes } = action.payload;
      if (holeIndex >= 0 && holeIndex < 18) {
        state.currentScores[holeIndex] = strokes;
      }
    },
    resetCurrentScores: (state) => {
      state.currentScores = Array(18).fill(0);
    },
    loadScoresFromAPI: (state, action: PayloadAction<HoleScore[]>) => {
      const scores = action.payload;
      const scoresArray = Array(18).fill(0);
      scores.forEach((score) => {
        if (score.hole_number >= 1 && score.hole_number <= 18) {
          scoresArray[score.hole_number - 1] = score.strokes;
        }
      });
      state.currentScores = scoresArray;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch hole scores
      .addCase(fetchHoleScores.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchHoleScores.fulfilled, (state, action: PayloadAction<HoleScore[]>) => {
        state.loading = false;
        state.holeScores = action.payload;
        // Auto-populate currentScores
        const scoresArray = Array(18).fill(0);
        action.payload.forEach((score) => {
          if (score.hole_number >= 1 && score.hole_number <= 18) {
            scoresArray[score.hole_number - 1] = score.strokes;
          }
        });
        state.currentScores = scoresArray;
      })
      .addCase(fetchHoleScores.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Save bulk hole scores
      .addCase(saveBulkHoleScores.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(saveBulkHoleScores.fulfilled, (state, action: PayloadAction<HoleScore[]>) => {
        state.saving = false;
        state.holeScores = action.payload;
        state.lastSaved = new Date().toISOString();
      })
      .addCase(saveBulkHoleScores.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      })
      // Update single hole score
      .addCase(updateHoleScore.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(updateHoleScore.fulfilled, (state, action: PayloadAction<HoleScore>) => {
        state.saving = false;
        const index = state.holeScores.findIndex((s) => s.id === action.payload.id);
        if (index !== -1) {
          state.holeScores[index] = action.payload;
        }
      })
      .addCase(updateHoleScore.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload as string;
      });
  },
});

export const { setHoleScore, resetCurrentScores, loadScoresFromAPI, clearError } = scoreSlice.actions;
export default scoreSlice.reducer;
