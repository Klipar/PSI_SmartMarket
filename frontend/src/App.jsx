import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import InventoryReceipt from './pages/InventoryReceipt';
import ReorderPage from './pages/ReorderPage';
import InventoryAudit from './pages/InventoryAudit';
import RevaluationPage from './pages/RevaluationPage';
import './App.css';

const DARK_PAGES = ['/inventory-receipt', '/', '/inventory-audit'];

function Layout() {
  const location = useLocation();
  const isDarkPage = DARK_PAGES.includes(location.pathname);
  const showSidebar = !DARK_PAGES.includes(location.pathname);

  // Створюємо об'єкт стилів для перекриття фону
  const mainStyle = isDarkPage ? {
    backgroundColor: '#0B1426', // Твій темний колір
    minHeight: '100vh',
    width: '100%',
    transition: 'background-color 0.2s ease'
  } : {};

  return (
    <div className="app-container">
      {showSidebar && <Sidebar />}
      
      {/* Накидаємо style прямо на тег main */}
      <main className="app-main" style={mainStyle}>
        <Routes>
          <Route path="/" element={<InventoryReceipt />} />
          <Route path="/inventory-receipt" element={<InventoryReceipt />} />
          <Route path="/reorder" element={<ReorderPage />} />
          <Route path="/revaluation" element={<RevaluationPage />} />
          <Route path="/inventory-audit" element={<InventoryAudit />} />
          <Route path="*" element={<div style={{ color: 'white', padding: '20px' }}>404 - Сторінку не знайдено</div>} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}

export default App;