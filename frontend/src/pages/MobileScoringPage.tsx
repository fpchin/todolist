/**
 * Mobile Scoring Page
 * Touch-friendly interface for entering scores for 18 holes
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  AppBar,
  Toolbar,
  IconButton,
  Button,
  Tabs,
  Tab,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Check as CheckIcon,
} from '@mui/icons-material';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import {
  fetchRound,
  clearCurrentRound,
} from '../store/slices/roundSlice';
import {
  fetchHoleScores,
  saveBulkHoleScores,
  setHoleScore,
  resetCurrentScores,
  clearError,
} from '../store/slices/scoreSlice';
import { HoleScoreInput } from '../components/scoring/HoleScoreInput';
import { ScoreCard } from '../components/scoring/ScoreCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';

export const MobileScoringPage: React.FC = () => {
  const { roundId } = useParams<{ roundId: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const { currentRound, loading: roundLoading, error: roundError } = useAppSelector(
    (state) => state.round
  );
  const { currentScores, saving, error: scoreError, lastSaved } = useAppSelector(
    (state) => state.score
  );

  const [tabValue, setTabValue] = useState(0); // 0 = Front 9, 1 = Back 9
  const [currentHole, setCurrentHole] = useState(0); // 0-17
  const [showSaveSuccess, setShowSaveSuccess] = useState(false);

  // TODO: Get these from user context/session
  const playerId = 'PLAYER_ID_PLACEHOLDER';

  useEffect(() => {
    if (roundId) {
      dispatch(fetchRound(roundId));
      dispatch(fetchHoleScores({ roundId, playerId }));
    }

    return () => {
      dispatch(clearCurrentRound());
      dispatch(resetCurrentScores());
    };
  }, [roundId, dispatch]);

  useEffect(() => {
    if (lastSaved) {
      setShowSaveSuccess(true);
    }
  }, [lastSaved]);

  const handleScoreChange = (holeIndex: number, strokes: number) => {
    dispatch(setHoleScore({ holeIndex, strokes }));
  };

  const handleSave = async () => {
    if (!roundId) return;

    // Validate all 18 holes have scores
    const hasAllScores = currentScores.every((score) => score > 0);
    if (!hasAllScores) {
      alert('Please enter scores for all 18 holes before saving.');
      return;
    }

    try {
      await dispatch(
        saveBulkHoleScores({
          round_id: roundId,
          player_id: playerId,
          hole_scores: currentScores,
        })
      ).unwrap();
    } catch (err) {
      console.error('Failed to save scores:', err);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setCurrentHole(newValue === 0 ? 0 : 9);
  };

  const handleBack = () => {
    navigate(-1);
  };

  if (roundLoading) {
    return <LoadingSpinner message="Loading round..." />;
  }

  if (roundError) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <ErrorAlert error={roundError} />
        <Button onClick={handleBack} startIcon={<ArrowBackIcon />}>
          Go Back
        </Button>
      </Container>
    );
  }

  if (!currentRound) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <ErrorAlert error="Round not found" />
        <Button onClick={handleBack} startIcon={<ArrowBackIcon />}>
          Go Back
        </Button>
      </Container>
    );
  }

  const holes = currentRound.course.holes || [];
  const pars = holes.map((h) => h.par);
  const strokeIndices = holes.map((h) => h.handicap_stroke_index);

  // Determine which holes to display based on current tab
  const displayHoles = tabValue === 0
    ? Array.from({ length: 9 }, (_, i) => i)
    : Array.from({ length: 9 }, (_, i) => i + 9);

  // Calculate completion percentage
  const completedHoles = currentScores.filter((score) => score > 0).length;
  const completionPercentage = Math.round((completedHoles / 18) * 100);

  return (
    <Box sx={{ pb: 8 }}>
      {/* App Bar */}
      <AppBar position="sticky">
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={handleBack}>
            <ArrowBackIcon />
          </IconButton>
          <Box flexGrow={1}>
            <Typography variant="h6" noWrap>
              {currentRound.course.course_name}
            </Typography>
            <Typography variant="caption">
              Round {currentRound.round_number} • {completedHoles}/18 holes
            </Typography>
          </Box>
          <Button
            variant="contained"
            color="secondary"
            startIcon={saving ? <CheckIcon /> : <SaveIcon />}
            onClick={handleSave}
            disabled={saving || completedHoles < 18}
          >
            {saving ? 'Saving...' : 'Save'}
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="sm" sx={{ mt: 2 }}>
        {/* Error display */}
        {scoreError && (
          <ErrorAlert
            error={scoreError}
            onClose={() => dispatch(clearError())}
          />
        )}

        {/* Completion progress */}
        <Alert severity={completedHoles === 18 ? 'success' : 'info'} sx={{ mb: 2 }}>
          {completedHoles === 18
            ? 'All holes completed! Ready to save.'
            : `${completionPercentage}% complete (${completedHoles}/18 holes)`}
        </Alert>

        {/* Score card summary */}
        <ScoreCard scores={currentScores} pars={pars} />

        {/* Front 9 / Back 9 Tabs */}
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{ mb: 2, borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Front 9" />
          <Tab label="Back 9" />
        </Tabs>

        {/* Hole score inputs */}
        {displayHoles.map((holeIndex) => (
          <HoleScoreInput
            key={holeIndex}
            holeNumber={holeIndex + 1}
            par={pars[holeIndex] || 4}
            strokeIndex={strokeIndices[holeIndex] || holeIndex + 1}
            currentScore={currentScores[holeIndex]}
            onScoreChange={(strokes) => handleScoreChange(holeIndex, strokes)}
            disabled={saving}
          />
        ))}
      </Container>

      {/* Success notification */}
      <Snackbar
        open={showSaveSuccess}
        autoHideDuration={3000}
        onClose={() => setShowSaveSuccess(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity="success" onClose={() => setShowSaveSuccess(false)}>
          Scores saved successfully!
        </Alert>
      </Snackbar>
    </Box>
  );
};
