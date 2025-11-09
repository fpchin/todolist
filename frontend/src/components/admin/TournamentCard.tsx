/**
 * Tournament card component for admin dashboard
 */
import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Button,
  Stack,
  Box,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  People as PeopleIcon,
  EmojiEvents as TrophyIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';
import type { Tournament } from '../../types';

interface TournamentCardProps {
  tournament: Tournament;
  onEdit?: (tournament: Tournament) => void;
  onDelete?: (tournament: Tournament) => void;
  onViewLeaderboard?: (tournament: Tournament) => void;
  onManagePlayers?: (tournament: Tournament) => void;
}

export const TournamentCard: React.FC<TournamentCardProps> = ({
  tournament,
  onEdit,
  onDelete,
  onViewLeaderboard,
  onManagePlayers,
}) => {
  const getStatusColor = (
    status: string
  ): 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' => {
    switch (status) {
      case 'DRAFT':
        return 'default';
      case 'OPEN':
        return 'info';
      case 'IN_PROGRESS':
        return 'warning';
      case 'COMPLETED':
        return 'success';
      case 'CANCELLED':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return dateString;
    }
  };

  return (
    <Card>
      <CardContent>
        <Stack spacing={2}>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start">
            <Typography variant="h6" component="h2" gutterBottom>
              {tournament.name}
            </Typography>
            <Chip
              label={tournament.status.replace('_', ' ')}
              color={getStatusColor(tournament.status)}
              size="small"
            />
          </Box>

          <Stack direction="row" spacing={1} flexWrap="wrap">
            <Chip
              icon={<TrophyIcon />}
              label={tournament.format_type}
              size="small"
              variant="outlined"
            />
          </Stack>

          <Typography variant="body2" color="text.secondary">
            <strong>Location:</strong> {tournament.location}
          </Typography>

          <Typography variant="body2" color="text.secondary">
            <strong>Dates:</strong> {formatDate(tournament.start_date)} -{' '}
            {formatDate(tournament.end_date)}
          </Typography>

          <Typography variant="body2" color="text.secondary">
            <strong>Max Players:</strong> {tournament.max_players}
          </Typography>
        </Stack>
      </CardContent>

      <CardActions>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          {onViewLeaderboard && (
            <Button
              size="small"
              startIcon={<ViewIcon />}
              onClick={() => onViewLeaderboard(tournament)}
            >
              Leaderboard
            </Button>
          )}
          {onManagePlayers && (
            <Button
              size="small"
              startIcon={<PeopleIcon />}
              onClick={() => onManagePlayers(tournament)}
            >
              Players
            </Button>
          )}
          {onEdit && (
            <Button size="small" startIcon={<EditIcon />} onClick={() => onEdit(tournament)}>
              Edit
            </Button>
          )}
          {onDelete && (
            <Button
              size="small"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={() => onDelete(tournament)}
            >
              Delete
            </Button>
          )}
        </Stack>
      </CardActions>
    </Card>
  );
};
