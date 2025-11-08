/**
 * Individual hole score input component
 * Touch-friendly interface with large buttons
 */
import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Stack,
  Chip,
} from '@mui/material';
import { ScoreButton } from '../common/ScoreButton';

interface HoleScoreInputProps {
  holeNumber: number;
  par: number;
  strokeIndex: number;
  currentScore: number;
  onScoreChange: (score: number) => void;
  disabled?: boolean;
}

export const HoleScoreInput: React.FC<HoleScoreInputProps> = ({
  holeNumber,
  par,
  strokeIndex,
  currentScore,
  onScoreChange,
  disabled = false,
}) => {
  // Generate score options from par-2 to par+6 (reasonable range)
  const minScore = Math.max(1, par - 2);
  const maxScore = par + 6;
  const scoreOptions = Array.from({ length: maxScore - minScore + 1 }, (_, i) => minScore + i);

  // Calculate score relative to par
  const getScoreName = (score: number): string => {
    const diff = score - par;
    if (diff <= -2) return 'Eagle or better';
    if (diff === -1) return 'Birdie';
    if (diff === 0) return 'Par';
    if (diff === 1) return 'Bogey';
    if (diff === 2) return 'Double Bogey';
    return `+${diff}`;
  };

  const getScoreColor = (score: number): 'success' | 'default' | 'warning' | 'error' => {
    const diff = score - par;
    if (diff <= -1) return 'success';
    if (diff === 0) return 'default';
    if (diff === 1) return 'warning';
    return 'error';
  };

  return (
    <Paper
      elevation={2}
      sx={{
        p: 2,
        mb: 2,
        bgcolor: disabled ? 'action.disabledBackground' : 'background.paper',
      }}
    >
      <Stack spacing={2}>
        {/* Hole header */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h5" fontWeight="bold">
            Hole {holeNumber}
          </Typography>
          <Stack direction="row" spacing={1}>
            <Chip label={`Par ${par}`} size="small" color="primary" />
            <Chip label={`SI ${strokeIndex}`} size="small" variant="outlined" />
          </Stack>
        </Box>

        {/* Current score display */}
        {currentScore > 0 && (
          <Box textAlign="center">
            <Typography variant="h3" color="primary" fontWeight="bold">
              {currentScore}
            </Typography>
            <Chip
              label={getScoreName(currentScore)}
              color={getScoreColor(currentScore)}
              size="small"
            />
          </Box>
        )}

        {/* Score buttons */}
        <Grid container spacing={1}>
          {scoreOptions.map((score) => (
            <Grid item xs={3} key={score}>
              <ScoreButton
                fullWidth
                score={score}
                isSelected={currentScore === score}
                onClick={() => onScoreChange(score)}
                disabled={disabled}
              />
            </Grid>
          ))}
        </Grid>

        {/* Clear button */}
        {currentScore > 0 && (
          <ScoreButton
            fullWidth
            variant="outlined"
            color="secondary"
            onClick={() => onScoreChange(0)}
            disabled={disabled}
          >
            Clear
          </ScoreButton>
        )}
      </Stack>
    </Paper>
  );
};
