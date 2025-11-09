/**
 * Tests for API endpoints
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { tournamentsAPI, playersAPI, holeScoresAPI } from '../endpoints';
import axios from 'axios';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as any;

describe('API Endpoints', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('tournamentsAPI', () => {
    it('list() calls correct endpoint', async () => {
      const mockResponse = { data: [] };
      mockedAxios.get = vi.fn().resolves(mockResponse);

      const result = await tournamentsAPI.list();

      expect(mockedAxios.get).toHaveBeenCalledWith('/tournaments/');
      expect(result).toEqual(mockResponse);
    });

    it('get() calls correct endpoint with ID', async () => {
      const tournamentId = '123';
      const mockResponse = { data: { id: tournamentId } };
      mockedAxios.get = vi.fn().resolves(mockResponse);

      const result = await tournamentsAPI.get(tournamentId);

      expect(mockedAxios.get).toHaveBeenCalledWith(`/tournaments/${tournamentId}/`);
      expect(result).toEqual(mockResponse);
    });

    it('create() posts data', async () => {
      const tournamentData = { name: 'Test Tournament' };
      const mockResponse = { data: { id: '123', ...tournamentData } };
      mockedAxios.post = vi.fn().resolves(mockResponse);

      const result = await tournamentsAPI.create(tournamentData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/tournaments/', tournamentData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('playersAPI', () => {
    it('list() with search parameter', async () => {
      const mockResponse = { data: [] };
      mockedAxios.get = vi.fn().resolves(mockResponse);

      await playersAPI.list('John');

      expect(mockedAxios.get).toHaveBeenCalledWith('/players/', { params: { search: 'John' } });
    });
  });

  describe('holeScoresAPI', () => {
    it('bulkCreate() posts all 18 scores', async () => {
      const bulkData = {
        round_id: '123',
        player_id: '456',
        hole_scores: Array(18).fill(4),
      };
      const mockResponse = { data: [] };
      mockedAxios.post = vi.fn().resolves(mockResponse);

      const result = await holeScoresAPI.bulkCreate(bulkData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/hole-scores/bulk_create/', bulkData);
      expect(result).toEqual(mockResponse);
    });
  });
});
