import { createRoot } from 'react-dom/client';
import './theme/theme.css';
import './styles/global.css';
import './styles/responsive.css';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(<App />);
