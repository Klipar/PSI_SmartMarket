import React, { useState } from 'react';
import axios from 'axios';
import backArrow from '../assets/back-arrow.svg';
import doneIcon from '../assets/done-icon.svg';
import plusIcon from '../assets/Plus-icon.svg';
import trashIcon from '../assets/Trash.svg';
import { Scan, Camera, Zap, Image as ImageIcon, Calendar, Loader2 } from 'lucide-react';

const InventoryReceipt = () => {
  const [items, setItems] = useState([
    { id: 1, name: 'Industrial Bearing Pro', sku: 'BRG-992-XL', ean: '858000000001', qty: 10, plan: 12, expDate: '2025-10-31', price: 15.50 },
    { id: 2, name: 'Industrial Bearing Pro', sku: 'BRG-992-XL', ean: '858000000002', qty: 5, plan: 8, expDate: '2025-12-20', price: 12.00 },
  ]);
  const [loading, setLoading] = useState(false);
  const [deliveryNote, setDeliveryNote] = useState("BXK-GH-901");

  const updateQty = (id, delta) => {
    setItems(prev => prev.map(item => item.id === id ? { ...item, qty: Math.max(0, item.qty + delta) } : item));
  };

  const removeItem = (id) => setItems(prev => prev.filter(item => item.id !== id));

  const handleConfirmReceipt = async () => {
    if (items.length === 0) return alert("Список порожній!");
    setLoading(true);
    try {
      const requests = items.map(item => axios.post('http://127.0.0.1:8000/api/stock/receive/', {
        ean: item.ean,
        batch_id: `${deliveryNote}-${item.id}`,
        quantity: item.qty,
        expiration_date: item.expDate,
        price: item.price
      }));
      await Promise.all(requests);
      alert("Успішно прийнято!");
      setItems([]);
    } catch (error) {
      alert("Помилка API: " + (error.response?.data?.error || error.message));
    } finally { setLoading(false); }
  };

  return (
    <div className="receipt-container">
      {/* Header */}
      <div className="receipt-header">
        <button className="icon-btn"><img src={backArrow} alt="Back" /></button>
        <h1>Inventory Receipt</h1>
        <div className="spacer"></div>
      </div>

      {/* Delivery ID */}
      <div className="input-card">
        <label>Delivery note ID</label>
        <div className="input-row">
          <input type="text" value={deliveryNote} onChange={(e) => setDeliveryNote(e.target.value)} />
          <Scan size={20} color="#64748b" />
        </div>
      </div>

      {/* Scanner Area */}
      <div className="scanner-preview">
        <img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=1000" alt="Warehouse" className="bg-img" />
        <div className="scan-frame">
          <div className="corner tl"></div><div className="corner tr"></div>
          <div className="corner bl"></div><div className="corner br"></div>
          <div className="scan-line"></div>
        </div>
        <div className="scanner-tools">
          <button className="tool-btn"><Zap size={20} /></button>
          <button className="main-cam-btn"><Camera size={28} /></button>
          <button className="tool-btn"><ImageIcon size={20} /></button>
        </div>
      </div>

      {/* List Header */}
      <div className="list-title-row">
        <h2>Scanned Items ({items.length}/12)</h2>
        <span className="badge">In Progress</span>
      </div>

      {/* Items List */}
      <div className="items-list">
        {items.map(item => (
          <div key={item.id} className="item-card">
            <div className="item-main-info">
              <div>
                <h3>{item.name}</h3>
                <p className="sku">SKU: {item.sku} | EAN: {item.ean}</p>
              </div>
              <button onClick={() => removeItem(item.id)} className="delete-btn">
                <img src={trashIcon} alt="Delete" />
              </button>
            </div>
            <div className="item-controls">
              <div className="control-group">
                <label>Quantity (Plan: {item.plan})</label>
                <div className="qty-selector">
                  <button onClick={() => updateQty(item.id, -1)}>-</button>
                  <span>{item.qty}</span>
                  <button onClick={() => updateQty(item.id, 1)} className="plus">+</button>
                </div>
              </div>
              <div className="control-group">
                <label>Expiration</label>
                <div className="date-display">
                  <span>{item.expDate}</span>
                  <Calendar size={16} color="#64748b" />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <button className="add-manual-btn">
        <img src={plusIcon} alt="" /> Add Item Manually
      </button>

      {/* Footer */}
      <div className="footer-actions">
        <button className="btn-secondary">Save Draft</button>
        <button className="btn-primary" onClick={handleConfirmReceipt} disabled={loading}>
          {loading ? <Loader2 className="spin" /> : <>Confirm Receipt <img src={doneIcon} alt="" /></>}
        </button>
      </div>
    </div>
  );
};

export default InventoryReceipt;