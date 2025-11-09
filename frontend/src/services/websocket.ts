/**
 * WebSocket service for real-time leaderboard updates
 */
import io, { Socket } from 'socket.io-client';

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';

class WebSocketService {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(tournamentId: string): Socket {
    if (this.socket?.connected) {
      return this.socket;
    }

    this.socket = io(`${WS_BASE_URL}/leaderboard`, {
      transports: ['websocket'],
      query: {
        tournament_id: tournamentId,
      },
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
      if (reason === 'io server disconnect') {
        // Server initiated disconnect, attempt to reconnect
        this.attemptReconnect(tournamentId);
      }
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      this.attemptReconnect(tournamentId);
    });

    return this.socket;
  }

  private attemptReconnect(tournamentId: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

      setTimeout(() => {
        this.connect(tournamentId);
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  subscribeToLeaderboard(callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.on('leaderboard_update', callback);
    }
  }

  subscribeToScoreUpdate(callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.on('score_update', callback);
    }
  }

  unsubscribeFromLeaderboard(): void {
    if (this.socket) {
      this.socket.off('leaderboard_update');
    }
  }

  unsubscribeFromScoreUpdate(): void {
    if (this.socket) {
      this.socket.off('score_update');
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const websocketService = new WebSocketService();
