import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import InventoryReceipt from './pages/InventoryReceipt';
import ReorderPage from './pages/ReorderPage';
import InventoryAudit from './pages/InventoryAudit';
import './App.css';

const ROUTES_WITHOUT_SIDEBAR = ['/inventory-receipt', '/', '/inventory-audit'];

function Layout() {
  const location = useLocation();
  const showSidebar = !ROUTES_WITHOUT_SIDEBAR.includes(location.pathname);

  return (
    <div className="app-container">
      {showSidebar && <Sidebar />}
      <main className="app-main">
        <Routes>
          <Route path="/" element={<InventoryReceipt />} />
          <Route path="/inventory-receipt" element={<InventoryReceipt />} />
          <Route path="/reorder" element={<ReorderPage />} />
          <Route path="*" element={<div style={{ color: 'white', padding: '20px' }}>404 - Сторінку не знайдено</div>} />
          <Route path="/inventory-audit" element={<InventoryAudit />} />
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