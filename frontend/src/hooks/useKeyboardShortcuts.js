import { useEffect } from 'react';
import { api } from '../services/api';

function isTypingTarget(target) {
  const tag = target?.tagName?.toLowerCase();
  return tag === 'input' || tag === 'select' || tag === 'textarea' || target?.isContentEditable;
}

export function useKeyboardShortcuts({ toggleTheme, onShortcut }) {
  useEffect(() => {
    async function handleKeydown(event) {
      if (isTypingTarget(event.target) || event.metaKey || event.ctrlKey || event.altKey) return;

      const key = event.key.toLowerCase();
      if (key === 't') {
        toggleTheme();
        onShortcut?.('Theme toggled');
        return;
      }

      if (key === 'r') {
        try {
          await api.resetSimulation();
          onShortcut?.('Simulation reset');
        } catch {
          onShortcut?.('Reset failed');
        }
        return;
      }

      if (event.code === 'Space') {
        event.preventDefault();
        window.dispatchEvent(new CustomEvent('cascadeos:demo-trigger'));
        try {
          await api.triggerSimulation({
            node_id: 'water_34th',
            failure_type: 'main_break',
          });
          onShortcut?.('34th St demo cascade triggered');
        } catch {
          onShortcut?.('Demo trigger failed');
        }
      }
    }

    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  }, [toggleTheme, onShortcut]);
}
