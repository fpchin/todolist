/**
 * Leaderboard table component with OCB tiebreaker display
 */
import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Typography,
  Box,
  Collapse,
  IconButton,
  Stack,
} from '@mui/material';
import { KeyboardArrowDown, KeyboardArrowUp } from '@mui/icons-material';
import type { LeaderboardEntry } from '../../types';

interface LeaderboardTableProps {
  entries: LeaderboardEntry[];
  showDivisionRank?: boolean;
  selectedDivision?: string | null;
}

const LeaderboardRow: React.FC<{
  entry: LeaderboardEntry;
  showDivisionRank: boolean;
}> = ({ entry, showDivisionRank }) => {
  const [open, setOpen] = React.useState(false);

  const formatToPar = (toPar: number): string => {
    if (toPar === 0) return 'E';
    return toPar > 0 ? `+${toPar}` : `${toPar}`;
  };

  const getToParColor = (toPar: number): string => {
    if (toPar < 0) return 'success.main';
    if (toPar === 0) return 'text.primary';
    return 'error.main';
  };

  // Calculate to par
  const toPar = entry.total_net - 72; // Assuming par 72, should come from course data

  return (
    <>
      <TableRow hover sx={{ '& > *': { borderBottom: 'unset' } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
          </IconButton>
        </TableCell>
        <TableCell align="center">
          <Typography variant="h6" fontWeight="bold">
            {showDivisionRank ? entry.rank_division : entry.rank_overall}
          </Typography>
        </TableCell>
        <TableCell>
          <Stack>
            <Typography variant="body1" fontWeight="medium">
              {entry.player.first_name} {entry.player.last_name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {entry.division}
            </Typography>
          </Stack>
        </TableCell>
        <TableCell align="center">
          <Typography variant="h6">{entry.total_gross}</Typography>
        </TableCell>
        <TableCell align="center">
          <Typography variant="h6" fontWeight="bold">
            {entry.total_net}
          </Typography>
        </TableCell>
        <TableCell align="center">
          <Chip
            label={formatToPar(toPar)}
            color={toPar < 0 ? 'success' : toPar === 0 ? 'default' : 'error'}
            size="small"
          />
        </TableCell>
      </TableRow>

      {/* OCB Details */}
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 2 }}>
              <Typography variant="subtitle2" gutterBottom component="div">
                OCB Tiebreaker Details
              </Typography>
              <Table size="small" aria-label="ocb-details">
                <TableHead>
                  <TableRow>
                    <TableCell>Metric</TableCell>
                    <TableCell align="right">Total</TableCell>
                    <TableCell align="right">Last 9</TableCell>
                    <TableCell align="right">Last 6</TableCell>
                    <TableCell align="right">Last 3</TableCell>
                    <TableCell align="right">Last Hole</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell component="th" scope="row">
                      Net Score
                    </TableCell>
                    <TableCell align="right">{entry.ocb_net.total}</TableCell>
                    <TableCell align="right">{entry.ocb_net.last_9}</TableCell>
                    <TableCell align="right">{entry.ocb_net.last_6}</TableCell>
                    <TableCell align="right">{entry.ocb_net.last_3}</TableCell>
                    <TableCell align="right">{entry.ocb_net.last_hole}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

export const LeaderboardTable: React.FC<LeaderboardTableProps> = ({
  entries,
  showDivisionRank = false,
  selectedDivision = null,
}) => {
  const filteredEntries = selectedDivision
    ? entries.filter((entry) => entry.division === selectedDivision)
    : entries;

  if (filteredEntries.length === 0) {
    return (
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="body1" color="text.secondary">
          No results available yet
        </Typography>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell align="center">
              <strong>Rank</strong>
            </TableCell>
            <TableCell>
              <strong>Player</strong>
            </TableCell>
            <TableCell align="center">
              <strong>Gross</strong>
            </TableCell>
            <TableCell align="center">
              <strong>Net</strong>
            </TableCell>
            <TableCell align="center">
              <strong>To Par</strong>
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filteredEntries.map((entry) => (
            <LeaderboardRow
              key={entry.player.id}
              entry={entry}
              showDivisionRank={showDivisionRank}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
