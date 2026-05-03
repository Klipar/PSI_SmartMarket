import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ReorderPage from './pages/ReorderPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <main className="app-content">
          <Routes>
            <Route path="/reorder" element={<ReorderPage />} />
            {/* Додай інші маршрути тут */}
            <Route path="/" element={<div>Home Page</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;