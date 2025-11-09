/**
 * Tests for score Redux slice
 */
import { describe, it, expect } from 'vitest';
import scoreReducer, { setHoleScore, resetCurrentScores } from '../scoreSlice';

describe('scoreSlice', () => {
  const initialState = {
    holeScores: [],
    currentScores: Array(18).fill(0),
    loading: false,
    saving: false,
    error: null,
    lastSaved: null,
  };

  it('should return the initial state', () => {
    expect(scoreReducer(undefined, { type: 'unknown' })).toEqual(initialState);
  });

  it('should handle setHoleScore', () => {
    const actual = scoreReducer(initialState, setHoleScore({ holeIndex: 0, strokes: 4 }));
    expect(actual.currentScores[0]).toEqual(4);
  });

  it('should handle setHoleScore for different holes', () => {
    let state = initialState;
    state = scoreReducer(state, setHoleScore({ holeIndex: 0, strokes: 4 }));
    state = scoreReducer(state, setHoleScore({ holeIndex: 1, strokes: 5 }));
    state = scoreReducer(state, setHoleScore({ holeIndex: 17, strokes: 3 }));

    expect(state.currentScores[0]).toEqual(4);
    expect(state.currentScores[1]).toEqual(5);
    expect(state.currentScores[17]).toEqual(3);
  });

  it('should handle resetCurrentScores', () => {
    const stateWithScores = {
      ...initialState,
      currentScores: [4, 5, 4, 3, 5, 6, 4, 3, 5, 4, 4, 3, 6, 5, 4, 4, 3, 4],
    };

    const actual = scoreReducer(stateWithScores, resetCurrentScores());
    expect(actual.currentScores).toEqual(Array(18).fill(0));
  });

  it('should not set score for invalid hole index', () => {
    const actual = scoreReducer(initialState, setHoleScore({ holeIndex: 18, strokes: 4 }));
    expect(actual.currentScores).toEqual(initialState.currentScores);
  });

  it('should not set score for negative hole index', () => {
    const actual = scoreReducer(initialState, setHoleScore({ holeIndex: -1, strokes: 4 }));
    expect(actual.currentScores).toEqual(initialState.currentScores);
  });
});
