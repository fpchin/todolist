import { configureStore } from '@reduxjs/toolkit';
import roundReducer from './slices/roundSlice';
import scoreReducer from './slices/scoreSlice';
import tournamentReducer from './slices/tournamentSlice';
import leaderboardReducer from './slices/leaderboardSlice';

export const store = configureStore({
  reducer: {
    round: roundReducer,
    score: scoreReducer,
    tournament: tournamentReducer,
    leaderboard: leaderboardReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
