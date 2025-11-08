import { configureStore } from '@reduxjs/toolkit';

// Reducers will be added here as features are implemented
export const store = configureStore({
  reducer: {
    // Add reducers here
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
