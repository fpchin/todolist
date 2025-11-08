import { configureStore } from '@reduxjs/toolkit';
import roundReducer from './slices/roundSlice';
import scoreReducer from './slices/scoreSlice';

export const store = configureStore({
  reducer: {
    round: roundReducer,
    score: scoreReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
