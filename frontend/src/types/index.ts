/**
 * TypeScript type definitions for GTMS API models
 */

export interface Player {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  club_affiliation?: string;
  created_at: string;
  updated_at: string;
}

export interface Tournament {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  location: string;
  format_type: 'STROKEPLAY' | 'STABLEFORD' | 'MATCHPLAY' | 'SCRAMBLE';
  status: 'DRAFT' | 'OPEN' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
  max_players: number;
  created_at: string;
  updated_at: string;
}

export interface TournamentPlayer {
  id: string;
  tournament: string;
  player: Player;
  handicap_index: string;
  playing_handicap: number;
  division: string;
  status: 'REGISTERED' | 'CONFIRMED' | 'WITHDRAWN' | 'DISQUALIFIED';
  created_at: string;
  updated_at: string;
}

export interface CourseConfiguration {
  id: string;
  course_name: string;
  tee_color: string;
  rating: string;
  slope: number;
  par: number;
  holes: HoleConfiguration[];
  created_at: string;
  updated_at: string;
}

export interface HoleConfiguration {
  id: string;
  course: string;
  hole_number: number;
  par: number;
  handicap_stroke_index: number;
  distance: number;
  created_at: string;
  updated_at: string;
}

export interface Round {
  id: string;
  tournament: string;
  round_number: number;
  round_date: string;
  course: CourseConfiguration;
  status: 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
  created_at: string;
  updated_at: string;
}

export interface HoleScore {
  id: string;
  round: string;
  player: string;
  hole_number: number;
  strokes: number;
  putts?: number;
  fairway_hit?: boolean;
  green_in_regulation?: boolean;
  verified: boolean;
  scorer?: string;
  created_at: string;
  updated_at: string;
}

export interface Result {
  id: string;
  tournament: string;
  player: Player;
  division: string;
  total_gross: number;
  total_net: number;
  gross_last_9: number;
  gross_last_6: number;
  gross_last_3: number;
  gross_last_hole: number;
  net_last_9: number;
  net_last_6: number;
  net_last_3: number;
  net_last_hole: number;
  rank_overall: number;
  rank_division: number;
  verified: boolean;
  calculated_at: string;
  created_at: string;
  updated_at: string;
}

// Request DTOs
export interface BulkHoleScoresRequest {
  round_id: string;
  player_id: string;
  hole_scores: number[];
  scorer_id?: string;
}

export interface TournamentPlayerRegistration {
  player_id: string;
  handicap_index: string;
  division: string;
}

// Response DTOs
export interface LeaderboardEntry {
  player: Player;
  division: string;
  total_gross: number;
  total_net: number;
  rank_overall: number;
  rank_division: number;
  ocb_net: {
    total: number;
    last_9: number;
    last_6: number;
    last_3: number;
    last_hole: number;
  };
}

export interface LeaderboardResponse {
  tournament: Tournament;
  entries: LeaderboardEntry[];
  last_updated: string;
}

// Error response
export interface APIError {
  detail?: string;
  [key: string]: any;
}
