/**
 * API endpoint service functions
 */
import { apiClient } from './client';
import type {
  Tournament,
  TournamentPlayer,
  TournamentPlayerRegistration,
  Player,
  Round,
  HoleScore,
  BulkHoleScoresRequest,
  Result,
  LeaderboardResponse,
  CourseConfiguration,
} from '../types';

// Tournaments
export const tournamentsAPI = {
  list: () => apiClient.get<Tournament[]>('/tournaments/'),

  get: (id: string) => apiClient.get<Tournament>(`/tournaments/${id}/`),

  create: (data: Partial<Tournament>) => apiClient.post<Tournament>('/tournaments/', data),

  update: (id: string, data: Partial<Tournament>) =>
    apiClient.patch<Tournament>(`/tournaments/${id}/`, data),

  delete: (id: string) => apiClient.delete(`/tournaments/${id}/`),

  registerPlayer: (tournamentId: string, data: TournamentPlayerRegistration) =>
    apiClient.post<TournamentPlayer>(`/tournaments/${tournamentId}/register_player/`, data),

  getPlayers: (tournamentId: string) =>
    apiClient.get<TournamentPlayer[]>(`/tournaments/${tournamentId}/players/`),

  getLeaderboard: (tournamentId: string) =>
    apiClient.get<LeaderboardResponse>(`/tournaments/${tournamentId}/leaderboard/`),
};

// Tournament Players
export const tournamentPlayersAPI = {
  list: (params?: { tournament?: string; player?: string; division?: string }) =>
    apiClient.get<TournamentPlayer[]>('/tournament-players/', { params }),

  get: (id: string) => apiClient.get<TournamentPlayer>(`/tournament-players/${id}/`),

  update: (id: string, data: Partial<TournamentPlayer>) =>
    apiClient.patch<TournamentPlayer>(`/tournament-players/${id}/`, data),

  delete: (id: string) => apiClient.delete(`/tournament-players/${id}/`),
};

// Players
export const playersAPI = {
  list: (search?: string) =>
    apiClient.get<Player[]>('/players/', { params: { search } }),

  get: (id: string) => apiClient.get<Player>(`/players/${id}/`),

  create: (data: Partial<Player>) => apiClient.post<Player>('/players/', data),

  update: (id: string, data: Partial<Player>) =>
    apiClient.patch<Player>(`/players/${id}/`, data),

  delete: (id: string) => apiClient.delete(`/players/${id}/`),
};

// Rounds
export const roundsAPI = {
  list: (params?: { tournament?: string; status?: string }) =>
    apiClient.get<Round[]>('/rounds/', { params }),

  get: (id: string) => apiClient.get<Round>(`/rounds/${id}/`),

  create: (data: Partial<Round>) => apiClient.post<Round>('/rounds/', data),

  update: (id: string, data: Partial<Round>) =>
    apiClient.patch<Round>(`/rounds/${id}/`, data),

  delete: (id: string) => apiClient.delete(`/rounds/${id}/`),
};

// Hole Scores
export const holeScoresAPI = {
  list: (params?: { round?: string; player?: string; hole_number?: number }) =>
    apiClient.get<HoleScore[]>('/hole-scores/', { params }),

  get: (id: string) => apiClient.get<HoleScore>(`/hole-scores/${id}/`),

  create: (data: Partial<HoleScore>) => apiClient.post<HoleScore>('/hole-scores/', data),

  bulkCreate: (data: BulkHoleScoresRequest) =>
    apiClient.post<HoleScore[]>('/hole-scores/bulk_create/', data),

  update: (id: string, data: Partial<HoleScore>) =>
    apiClient.patch<HoleScore>(`/hole-scores/${id}/`, data),

  delete: (id: string) => apiClient.delete(`/hole-scores/${id}/`),
};

// Results
export const resultsAPI = {
  list: (params?: { tournament?: string; division?: string }) =>
    apiClient.get<Result[]>('/results/', { params }),

  get: (id: string) => apiClient.get<Result>(`/results/${id}/`),

  calculate: (tournamentId: string) =>
    apiClient.post<Result[]>(`/results/calculate/`, { tournament_id: tournamentId }),
};

// Courses
export const coursesAPI = {
  list: () => apiClient.get<CourseConfiguration[]>('/courses/'),

  get: (id: string) => apiClient.get<CourseConfiguration>(`/courses/${id}/`),

  create: (data: Partial<CourseConfiguration>) =>
    apiClient.post<CourseConfiguration>('/courses/', data),

  update: (id: string, data: Partial<CourseConfiguration>) =>
    apiClient.patch<CourseConfiguration>(`/courses/${id}/`, data),

  delete: (id: string) => apiClient.delete(`/courses/${id}/`),
};

// Health check
export const healthAPI = {
  check: () => apiClient.get('/health/'),
};
