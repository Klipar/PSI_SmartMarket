import React, { useState, useRef } from 'react';
import { Scan, Camera, Zap, Image as ImageIcon, Calendar, Loader2, Trash2, Plus, Check, Pencil, X } from 'lucide-react';
import backArrow from '../assets/back-arrow.svg';
import './InventoryReceipt.css';

const BASE_URL = 'http://127.0.0.1:8000/api';

const InventoryReceipt = () => {
  const [items, setItems] = useState([
    { id: 1, name: 'Industrial Bearing Pro', sku: 'BRG-992-XL', ean: '858000000001', qty: 10, plan: 12, expDate: '2025-10-31', price: 15.50 },
    { id: 2, name: 'Industrial Bearing Pro', sku: 'BRG-992-XL', ean: '858000000002', qty: 5, plan: 8, expDate: '2025-12-20', price: 12.00 },
  ]);
  const [loading, setLoading] = useState(false);
  const [deliveryNote, setDeliveryNote] = useState('BXK-GH-901');
  const [toast, setToast] = useState(null);
  const [removingIds, setRemovingIds] = useState([]);
  const [editingEan, setEditingEan] = useState(null); // id товару що редагується
  const [eanDraft, setEanDraft] = useState('');
  const nextId = useRef(3);
  const toastTimer = useRef(null);
  const eanInputRef = useRef(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(null), 2500);
  };

  const updateQty = (id, delta) => {
    setItems(prev =>
      prev.map(item => item.id === id ? { ...item, qty: Math.max(0, item.qty + delta) } : item)
    );
  };

  const updateField = (id, field, value) => {
    setItems(prev =>
      prev.map(item => item.id === id ? { ...item, [field]: value } : item)
    );
  };

  const startEditEan = (item) => {
    setEditingEan(item.id);
    setEanDraft(item.ean);
    setTimeout(() => eanInputRef.current?.focus(), 50);
  };

  const confirmEan = (id) => {
    const trimmed = eanDraft.trim();
    if (!trimmed) { showToast('EAN cannot be empty', 'error'); return; }
    updateField(id, 'ean', trimmed);
    setEditingEan(null);
    showToast('EAN updated', 'success');
  };

  const cancelEan = () => {
    setEditingEan(null);
    setEanDraft('');
  };

  const removeItem = (id) => {
    setRemovingIds(prev => [...prev, id]);
    setTimeout(() => {
      setItems(prev => prev.filter(item => item.id !== id));
      setRemovingIds(prev => prev.filter(x => x !== id));
      showToast('Item removed', 'error');
    }, 250);
  };

  const addManualItem = () => {
    const id = nextId.current++;
    setItems(prev => [...prev, {
      id,
      name: 'New Product',
      sku: `NEW-${String(id).padStart(3, '0')}`,
      ean: `858${String(Math.floor(Math.random() * 1e9)).padStart(9, '0')}`,
      qty: 1, plan: 5,
      expDate: '2026-06-01',
      price: 0,
    }]);
    showToast('Item added manually', 'success');
  };

  const saveDraft = () => showToast('Draft saved', 'success');

  const handleConfirmReceipt = async () => {
    if (items.length === 0) { showToast('List is empty!', 'error'); return; }
    setLoading(true);
    let successCount = 0;
    let errorMsg = null;

    for (const item of items) {
      try {
        const res = await fetch(`${BASE_URL}/stock/receive/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ean: item.ean,
            batch_id: `${deliveryNote}-${item.id}`,
            quantity: item.qty,
            expiration_date: item.expDate,
            price: item.price,
          }),
        });
        if (!res.ok) {
          const err = await res.json();
          errorMsg = err.error || `HTTP ${res.status}`;
          break;
        }
        successCount++;
      } catch {
        errorMsg = 'Server unreachable';
        break;
      }
    }

    setLoading(false);
    if (errorMsg) {
      showToast('Error: ' + errorMsg, 'error');
    } else {
      showToast(`${successCount} items processed!`, 'success');
      setTimeout(() => setItems([]), 800);
    }
  };

  return (
    <div className="receipt-container">

      {toast && (
        <div className={`toast toast--${toast.type}`}>{toast.msg}</div>
      )}

      <div className="receipt-header">
        <button className="icon-btn">
          <img src={backArrow} alt="Back" />
        </button>
        <h1>Inventory Receipt</h1>
        <div className="spacer" />
      </div>

      <div className="input-card">
        <label>Delivery note ID</label>
        <div className="input-row">
          <input
            type="text"
            value={deliveryNote}
            onChange={e => setDeliveryNote(e.target.value)}
          />
          <Scan size={18} color="#64748b" />
        </div>
      </div>

      <div className="scanner-preview">
        <img
          src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=1000"
          alt="Warehouse"
          className="bg-img"
        />
        <div className="scan-frame">
          <div className="corner tl" /><div className="corner tr" />
          <div className="corner bl" /><div className="corner br" />
          <div className="scan-line" />
        </div>
        <div className="scanner-tools">
          <button className="tool-btn" onClick={() => showToast('Flash enabled', 'success')}>
            <Zap size={18} />
          </button>
          <button className="main-cam-btn" onClick={() => showToast('Scanning...', 'success')}>
            <Camera size={26} />
          </button>
          <button className="tool-btn" onClick={() => showToast('Opening gallery...', 'success')}>
            <ImageIcon size={18} />
          </button>
        </div>
      </div>

      <div className="list-title-row">
        <h2>Scanned Items ({items.length}/12)</h2>
        <span className="badge">In Progress</span>
      </div>

      <div className="items-list">
        {items.map(item => (
          <div
            key={item.id}
            className={`item-card${removingIds.includes(item.id) ? ' item-card--removing' : ''}`}
          >
            <div className="item-main-info">
              <div className="item-name-block">
                <h3>{item.name}</h3>
                <p className="sku">SKU: {item.sku}</p>

                {/* EAN рядок */}
                {editingEan === item.id ? (
                  <div className="ean-edit-row">
                    <span className="ean-label">EAN:</span>
                    <input
                      ref={eanInputRef}
                      className="ean-input"
                      value={eanDraft}
                      onChange={e => setEanDraft(e.target.value)}
                      onKeyDown={e => {
                        if (e.key === 'Enter') confirmEan(item.id);
                        if (e.key === 'Escape') cancelEan();
                      }}
                      maxLength={13}
                    />
                    <button className="ean-confirm-btn" onClick={() => confirmEan(item.id)}>
                      <Check size={13} />
                    </button>
                    <button className="ean-cancel-btn" onClick={cancelEan}>
                      <X size={13} />
                    </button>
                  </div>
                ) : (
                  <div className="ean-row" onClick={() => startEditEan(item)}>
                    <span className="ean-label">EAN:</span>
                    <span className="ean-value">{item.ean}</span>
                    <Pencil size={11} className="ean-pencil" />
                  </div>
                )}
              </div>

              <button onClick={() => removeItem(item.id)} className="delete-btn">
                <Trash2 size={16} />
              </button>
            </div>

            <div className="item-controls">
              <div className="control-group">
                <label>Quantity (Plan: {item.plan})</label>
                <div className="qty-selector">
                  <button className="qty-btn" onClick={() => updateQty(item.id, -1)}>−</button>
                  <span>{item.qty}</span>
                  <button className="qty-btn plus" onClick={() => updateQty(item.id, 1)}>+</button>
                </div>
              </div>
              <div className="control-group">
                <label>Expiration Date</label>
                <div className="date-display">
                  <input
                    type="date"
                    className="date-input"
                    value={item.expDate}
                    onChange={e => updateField(item.id, 'expDate', e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <button className="add-manual-btn" onClick={addManualItem}>
        <Plus size={16} /> Add Item Manually
      </button>

      <div className="footer-actions">
        <div className="footer-inner">
          <button className="btn-secondary" onClick={saveDraft}>Save Draft</button>
          <button className="btn-primary" onClick={handleConfirmReceipt} disabled={loading}>
            {loading
              ? <Loader2 size={18} className="spin" />
              : <><Check size={16} /> Confirm Receipt</>
            }
          </button>
        </div>
      </div>

    </div>
  );
};

export default InventoryReceipt;