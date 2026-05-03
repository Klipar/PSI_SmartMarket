import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import InventoryReceipt from './pages/InventoryReceipt';
import ReorderPage from './pages/ReorderPage';
import './App.css';
import RevaluationPage from './pages/RevaluationPage';


function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <main className="app-content">
          <Routes>
            {/* Головна сторінка — за замовчуванням може бути InventoryReceipt або Home */}
            <Route path="/" element={<InventoryReceipt />} />
            
            {/* Маршрут для UC01: Прийом товару */}
            <Route path="/inventory-receipt" element={<InventoryReceipt />} />
            
            <Route path="/revaluation" element={<RevaluationPage />} />
            
            {/* Маршрут для UC02: Розумне замовлення */}
            <Route path="/reorder" element={<ReorderPage />} />
            
            {/* Fallback для неіснуючих сторінок */}
            <Route path="*" element={<div>404 - Сторінку не знайдено</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;