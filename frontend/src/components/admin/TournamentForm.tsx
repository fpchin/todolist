/**
 * Tournament form for creating/editing tournaments
 */
import React, { useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  MenuItem,
  Stack,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import type { Tournament } from '../../types';

const schema = yup.object({
  name: yup.string().required('Tournament name is required').max(255),
  location: yup.string().required('Location is required').max(255),
  start_date: yup.string().required('Start date is required'),
  end_date: yup.string().required('End date is required'),
  format_type: yup.string().required('Format type is required'),
  status: yup.string().required('Status is required'),
  max_players: yup.number().required('Max players is required').min(1).max(1000),
}).required();

type TournamentFormData = yup.InferType<typeof schema>;

interface TournamentFormProps {
  open: boolean;
  tournament?: Tournament | null;
  onClose: () => void;
  onSubmit: (data: Partial<Tournament>) => void;
  loading?: boolean;
}

export const TournamentForm: React.FC<TournamentFormProps> = ({
  open,
  tournament,
  onClose,
  onSubmit,
  loading = false,
}) => {
  const isEditMode = Boolean(tournament);

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TournamentFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      name: '',
      location: '',
      start_date: '',
      end_date: '',
      format_type: 'STROKEPLAY',
      status: 'DRAFT',
      max_players: 200,
    },
  });

  useEffect(() => {
    if (tournament) {
      reset({
        name: tournament.name,
        location: tournament.location,
        start_date: tournament.start_date,
        end_date: tournament.end_date,
        format_type: tournament.format_type,
        status: tournament.status,
        max_players: tournament.max_players,
      });
    } else {
      reset({
        name: '',
        location: '',
        start_date: '',
        end_date: '',
        format_type: 'STROKEPLAY',
        status: 'DRAFT',
        max_players: 200,
      });
    }
  }, [tournament, reset]);

  const handleFormSubmit = (data: TournamentFormData) => {
    onSubmit(data);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>{isEditMode ? 'Edit Tournament' : 'Create Tournament'}</DialogTitle>
      <form onSubmit={handleSubmit(handleFormSubmit)}>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <Controller
              name="name"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Tournament Name"
                  fullWidth
                  required
                  error={!!errors.name}
                  helperText={errors.name?.message}
                />
              )}
            />

            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Controller
                  name="start_date"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Start Date"
                      type="date"
                      fullWidth
                      required
                      InputLabelProps={{ shrink: true }}
                      error={!!errors.start_date}
                      helperText={errors.start_date?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="end_date"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="End Date"
                      type="date"
                      fullWidth
                      required
                      InputLabelProps={{ shrink: true }}
                      error={!!errors.end_date}
                      helperText={errors.end_date?.message}
                    />
                  )}
                />
              </Grid>
            </Grid>

            <Controller
              name="location"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Location"
                  fullWidth
                  required
                  error={!!errors.location}
                  helperText={errors.location?.message}
                />
              )}
            />

            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Controller
                  name="format_type"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Format"
                      select
                      fullWidth
                      required
                      error={!!errors.format_type}
                      helperText={errors.format_type?.message}
                    >
                      <MenuItem value="STROKEPLAY">Stroke Play</MenuItem>
                      <MenuItem value="STABLEFORD">Stableford</MenuItem>
                      <MenuItem value="MATCHPLAY">Match Play</MenuItem>
                      <MenuItem value="SCRAMBLE">Scramble</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Controller
                  name="status"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Status"
                      select
                      fullWidth
                      required
                      error={!!errors.status}
                      helperText={errors.status?.message}
                    >
                      <MenuItem value="DRAFT">Draft</MenuItem>
                      <MenuItem value="OPEN">Open</MenuItem>
                      <MenuItem value="IN_PROGRESS">In Progress</MenuItem>
                      <MenuItem value="COMPLETED">Completed</MenuItem>
                      <MenuItem value="CANCELLED">Cancelled</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>
            </Grid>

            <Controller
              name="max_players"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Maximum Players"
                  type="number"
                  fullWidth
                  required
                  error={!!errors.max_players}
                  helperText={errors.max_players?.message}
                />
              )}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? 'Saving...' : isEditMode ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};
