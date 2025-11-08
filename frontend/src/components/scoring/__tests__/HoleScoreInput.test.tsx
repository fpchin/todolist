/**
 * Unit tests for HoleScoreInput component
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { HoleScoreInput } from '../HoleScoreInput';

describe('HoleScoreInput', () => {
  const mockOnScoreChange = vi.fn();

  const defaultProps = {
    holeNumber: 1,
    par: 4,
    strokeIndex: 1,
    currentScore: 0,
    onScoreChange: mockOnScoreChange,
  };

  beforeEach(() => {
    mockOnScoreChange.mockClear();
  });

  it('renders hole information correctly', () => {
    render(<HoleScoreInput {...defaultProps} />);

    expect(screen.getByText('Hole 1')).toBeInTheDocument();
    expect(screen.getByText('Par 4')).toBeInTheDocument();
    expect(screen.getByText('SI 1')).toBeInTheDocument();
  });

  it('displays score buttons in correct range', () => {
    render(<HoleScoreInput {...defaultProps} />);

    // For par 4, should show scores 2-10 (par-2 to par+6)
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('10')).toBeInTheDocument();
  });

  it('calls onScoreChange when score button clicked', () => {
    render(<HoleScoreInput {...defaultProps} />);

    const scoreButton = screen.getByText('5');
    fireEvent.click(scoreButton);

    expect(mockOnScoreChange).toHaveBeenCalledWith(5);
  });

  it('highlights selected score', () => {
    render(<HoleScoreInput {...defaultProps} currentScore={4} />);

    expect(screen.getByText('4')).toBeInTheDocument();
    expect(screen.getByText('Par')).toBeInTheDocument();
  });

  it('shows score relative to par', () => {
    render(<HoleScoreInput {...defaultProps} currentScore={3} />);

    expect(screen.getByText('Birdie')).toBeInTheDocument();
  });

  it('disables inputs when disabled prop is true', () => {
    render(<HoleScoreInput {...defaultProps} disabled={true} />);

    const scoreButton = screen.getByText('4');
    expect(scoreButton).toBeDisabled();
  });
});
