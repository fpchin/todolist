/**
 * Unit tests for ScoreCard component
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ScoreCard } from '../ScoreCard';

describe('ScoreCard', () => {
  const pars = [4, 4, 4, 3, 4, 5, 4, 3, 5, 4, 4, 3, 5, 4, 4, 4, 3, 4];

  it('renders score summary table', () => {
    const scores = [4, 5, 4, 3, 5, 6, 4, 3, 5, 4, 4, 3, 6, 5, 4, 4, 3, 4];

    render(<ScoreCard scores={scores} pars={pars} />);

    expect(screen.getByText('Score Summary')).toBeInTheDocument();
    expect(screen.getByText('Front 9')).toBeInTheDocument();
    expect(screen.getByText('Back 9')).toBeInTheDocument();
    expect(screen.getByText('Total')).toBeInTheDocument();
  });

  it('calculates front 9 correctly', () => {
    const scores = [4, 5, 4, 3, 5, 6, 4, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    render(<ScoreCard scores={scores} pars={pars} />);

    // Front 9 = 39 (4+5+4+3+5+6+4+3+5), Par 36, +3
    expect(screen.getByText('39')).toBeInTheDocument();
    expect(screen.getByText('+3')).toBeInTheDocument();
  });

  it('calculates back 9 correctly', () => {
    const scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3, 6, 5, 4, 4, 3, 4];

    render(<ScoreCard scores={scores} pars={pars} />);

    // Back 9 = 37, Par 36, +1
    expect(screen.getByText('37')).toBeInTheDocument();
    expect(screen.getByText('+1')).toBeInTheDocument();
  });

  it('displays even par as E', () => {
    const scores = pars; // Exactly par

    render(<ScoreCard scores={scores} pars={pars} />);

    const eChips = screen.getAllByText('E');
    expect(eChips.length).toBeGreaterThan(0);
  });

  it('handles incomplete rounds gracefully', () => {
    const scores = [4, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    render(<ScoreCard scores={scores} pars={pars} />);

    // Should show partial scores
    expect(screen.getByText('13')).toBeInTheDocument();
  });

  it('displays under par with negative number', () => {
    const scores = [3, 3, 3, 2, 3, 4, 3, 2, 4, 3, 3, 2, 4, 3, 3, 3, 2, 3];

    render(<ScoreCard scores={scores} pars={pars} />);

    // Total should be under par
    const toParElements = screen.getAllByText(/-\d+/);
    expect(toParElements.length).toBeGreaterThan(0);
  });
});
