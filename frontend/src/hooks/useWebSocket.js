import { useEffect, useRef, useState, useCallback } from 'react';

const BASE_DELAY = 1000;
const MAX_DELAY = 30000;

export function useWebSocket(onMessage) {
  const wsUrl = `${import.meta.env.VITE_WS_URL}/main`;
  const wsRef = useRef(null);
  const retryRef = useRef(null);
  const delayRef = useRef(BASE_DELAY);
  const mountedRef = useRef(true);

  const [status, setStatus] = useState('connecting');

  const connect = useCallback(() => {
    if (!mountedRef.current) return;

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      if (!mountedRef.current) return;
      setStatus('connected');
      delayRef.current = BASE_DELAY;
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      } catch {
        // ignore malformed frames
      }
    };

    ws.onclose = () => {
      if (!mountedRef.current) return;
      setStatus('reconnecting');
      retryRef.current = setTimeout(() => {
        delayRef.current = Math.min(delayRef.current * 2, MAX_DELAY);
        connect();
      }, delayRef.current);
    };

    ws.onerror = () => {
      ws.close();
    };
  }, [wsUrl, onMessage]);

  useEffect(() => {
    mountedRef.current = true;
    connect();

    return () => {
      mountedRef.current = false;
      clearTimeout(retryRef.current);
      wsRef.current?.close();
    };
  }, [connect]);

  return status;
}
