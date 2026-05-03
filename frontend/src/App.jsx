import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import InventoryReceipt from './pages/InventoryReceipt';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<InventoryReceipt />} />
        <Route path="/inventory-receipt" element={<InventoryReceipt />} />
      </Routes>
    </Router>
  );
}

export default App;