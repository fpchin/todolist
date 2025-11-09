/**
 * Player registration dialog
 */
import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Autocomplete,
  Grid,
  Stack,
  CircularProgress,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { playersAPI } from '../../api/endpoints';
import type { Player, TournamentPlayerRegistration } from '../../types';

const schema = yup.object({
  player_id: yup.string().required('Player is required'),
  handicap_index: yup
    .string()
    .required('Handicap index is required')
    .matches(/^\d+(\.\d)?$/, 'Must be a valid handicap (e.g., 12.5)'),
  division: yup.string().required('Division is required'),
}).required();

type RegistrationFormData = yup.InferType<typeof schema>;

interface PlayerRegistrationDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: TournamentPlayerRegistration) => void;
  loading?: boolean;
}

export const PlayerRegistrationDialog: React.FC<PlayerRegistrationDialogProps> = ({
  open,
  onClose,
  onSubmit,
  loading = false,
}) => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loadingPlayers, setLoadingPlayers] = useState(false);
  const [searchText, setSearchText] = useState('');

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<RegistrationFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      player_id: '',
      handicap_index: '',
      division: 'Championship',
    },
  });

  // Fetch players on search
  useEffect(() => {
    const fetchPlayers = async () => {
      setLoadingPlayers(true);
      try {
        const response = await playersAPI.list(searchText);
        setPlayers(response.data);
      } catch (error) {
        console.error('Failed to fetch players:', error);
      } finally {
        setLoadingPlayers(false);
      }
    };

    if (searchText.length >= 2 || searchText.length === 0) {
      fetchPlayers();
    }
  }, [searchText]);

  const handleFormSubmit = (data: RegistrationFormData) => {
    onSubmit(data);
    reset();
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  const divisions = [
    'Championship',
    'A Division',
    'B Division',
    'C Division',
    'Senior',
    'Ladies',
    'Junior',
  ];

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Register Player</DialogTitle>
      <form onSubmit={handleSubmit(handleFormSubmit)}>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <Controller
              name="player_id"
              control={control}
              render={({ field: { onChange, value } }) => (
                <Autocomplete
                  options={players}
                  getOptionLabel={(option) =>
                    `${option.first_name} ${option.last_name} (${option.email})`
                  }
                  loading={loadingPlayers}
                  onInputChange={(_, newValue) => setSearchText(newValue)}
                  onChange={(_, newValue) => onChange(newValue?.id || '')}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Select Player"
                      required
                      error={!!errors.player_id}
                      helperText={errors.player_id?.message}
                      InputProps={{
                        ...params.InputProps,
                        endAdornment: (
                          <>
                            {loadingPlayers ? <CircularProgress color="inherit" size={20} /> : null}
                            {params.InputProps.endAdornment}
                          </>
                        ),
                      }}
                    />
                  )}
                />
              )}
            />

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Controller
                  name="handicap_index"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Handicap Index"
                      fullWidth
                      required
                      placeholder="e.g., 12.5"
                      error={!!errors.handicap_index}
                      helperText={errors.handicap_index?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Controller
                  name="division"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Division"
                      select
                      fullWidth
                      required
                      error={!!errors.division}
                      helperText={errors.division?.message}
                      SelectProps={{
                        native: true,
                      }}
                    >
                      {divisions.map((division) => (
                        <option key={division} value={division}>
                          {division}
                        </option>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
            </Grid>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} disabled={loading}>
            Cancel
          </Button>
          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};
