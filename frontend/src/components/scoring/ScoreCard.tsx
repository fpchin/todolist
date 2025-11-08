/**
 * Score card summary component
 * Shows front 9, back 9, and total scores
 */
import React from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Box,
} from '@mui/material';

interface ScoreCardProps {
  scores: number[];
  pars: number[];
}

export const ScoreCard: React.FC<ScoreCardProps> = ({ scores, pars }) => {
  const calculateTotal = (start: number, end: number): { strokes: number; toPar: number } => {
    const strokes = scores.slice(start, end).reduce((sum, score) => sum + (score || 0), 0);
    const parTotal = pars.slice(start, end).reduce((sum, par) => sum + par, 0);
    const toPar = strokes > 0 ? strokes - parTotal : 0;
    return { strokes, toPar };
  };

  const front9 = calculateTotal(0, 9);
  const back9 = calculateTotal(9, 18);
  const total = {
    strokes: front9.strokes + back9.strokes,
    toPar: front9.toPar + back9.toPar,
  };

  const formatToPar = (toPar: number): string => {
    if (toPar === 0) return 'E';
    return toPar > 0 ? `+${toPar}` : `${toPar}`;
  };

  const getToParColor = (toPar: number): string => {
    if (toPar < 0) return 'success.main';
    if (toPar === 0) return 'text.primary';
    return 'error.main';
  };

  return (
    <Paper elevation={2} sx={{ mb: 2 }}>
      <Box p={2}>
        <Typography variant="h6" gutterBottom>
          Score Summary
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Holes</TableCell>
                <TableCell align="right">Strokes</TableCell>
                <TableCell align="right">To Par</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Front 9</TableCell>
                <TableCell align="right">{front9.strokes > 0 ? front9.strokes : '-'}</TableCell>
                <TableCell align="right" sx={{ color: getToParColor(front9.toPar) }}>
                  {front9.strokes > 0 ? formatToPar(front9.toPar) : '-'}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Back 9</TableCell>
                <TableCell align="right">{back9.strokes > 0 ? back9.strokes : '-'}</TableCell>
                <TableCell align="right" sx={{ color: getToParColor(back9.toPar) }}>
                  {back9.strokes > 0 ? formatToPar(back9.toPar) : '-'}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <strong>Total</strong>
                </TableCell>
                <TableCell align="right">
                  <strong>{total.strokes > 0 ? total.strokes : '-'}</strong>
                </TableCell>
                <TableCell align="right" sx={{ color: getToParColor(total.toPar) }}>
                  <strong>{total.strokes > 0 ? formatToPar(total.toPar) : '-'}</strong>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Paper>
  );
};
