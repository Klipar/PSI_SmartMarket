import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Barcode, ChevronLeft, CheckCircle, Minus, Plus, Search, X, Check } from 'lucide-react';
import './InventoryAudit.css';

const BASE_URL = 'http://127.0.0.1:8000/api';

const InventoryAudit = () => {
  const navigate = useNavigate();

  const [inventuraId, setInventuraId] = useState(null);
  const [kategoria, setKategoria] = useState('All');
  const [started, setStarted] = useState(false);
  const [startLoading, setStartLoading] = useState(false);

  const [items, setItems] = useState([]);
  const [manualSku, setManualSku] = useState('');
  const [toast, setToast] = useState(null);
  const [checkingId, setCheckingId] = useState(null);

  const toastTimer = useRef(null);
  const manualInputRef = useRef(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(null), 2500);
  };

  // Step 1 — Start inventory
  const handleStart = async () => {
    setStartLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/inventory/start/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kategoria }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setInventuraId(data.id);
      setStarted(true);
      showToast('Inventory started', 'success');
    } catch (e) {
      showToast('Error: ' + e.message, 'error');
    } finally {
      setStartLoading(false);
    }
  };

  // Add item manually by ID/SKU
  const handleAddManual = () => {
    const val = manualSku.trim();
    if (!val) return;
    if (items.find(i => i.tovarId === val)) {
      showToast('Item already added', 'error');
      return;
    }
    setItems(prev => [...prev, {
      tovarId: val,
      name: `Product #${val}`,
      sku: val,
      qty: 0,
      plan: '—',
      status: 'pending',
      checked: false,
    }]);
    setManualSku('');
    manualInputRef.current?.focus();
  };

  const updateQty = (tovarId, delta) => {
    setItems(prev => prev.map(i =>
      i.tovarId === tovarId ? { ...i, qty: Math.max(0, i.qty + delta) } : i
    ));
  };

  const removeItem = (tovarId) => {
    setItems(prev => prev.filter(i => i.tovarId !== tovarId));
  };

  // Step 2 — Record check for a single item
  const handleCheck = async (item) => {
    if (!inventuraId) { showToast('Start inventory first', 'error'); return; }
    setCheckingId(item.tovarId);
    try {
      const res = await fetch(`${BASE_URL}/inventory/${inventuraId}/check/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tovar_id: item.tovarId,
          real_qty: item.qty,
        }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setItems(prev => prev.map(i =>
        i.tovarId === item.tovarId ? {
          ...i,
          checked: true,
          plan: data.system_qty,
          status: data.status,
          difference: data.difference,
        } : i
      ));
      showToast(
        data.status === 'match' ? `${data.tovar}: Match!` : `${data.tovar}: Diff ${data.difference > 0 ? '+' : ''}${data.difference}`,
        data.status === 'match' ? 'success' : 'error'
      );
    } catch (e) {
      showToast('Error: ' + e.message, 'error');
    } finally {
      setCheckingId(null);
    }
  };

  const checkedCount = items.filter(i => i.checked).length;

  return (
    <div className="audit-container">
      {toast && <div className={`audit-toast audit-toast--${toast.type}`}>{toast.msg}</div>}

      {/* Header */}
      <div className="audit-header">
        <button className="audit-back-btn" onClick={() => navigate(-1)}>
          <ChevronLeft size={22} />
        </button>
        <div className="audit-title-block">
          <h1>Inventory Audit</h1>
          {started && (
            <span className="audit-badge">In Progress</span>
          )}
        </div>
      </div>

      {/* Step 1: Start section */}
      {!started ? (
        <div className="audit-start-block">
          <p className="audit-section-label">Category</p>
          <div className="audit-input-card">
            <input
              type="text"
              value={kategoria}
              onChange={e => setKategoria(e.target.value)}
              placeholder="e.g. Bearings, All..."
            /> {/* Правильно закритий тег */}
          </div>
          <button className="audit-start-btn" onClick={handleStart} disabled={startLoading}>
            {startLoading ? 'Starting...' : 'Start Inventory'}
          </button>
        </div>
      ) : (
        <div className="audit-body">

          {/* Progress */}
          <div className="audit-progress-row">
            <span className="audit-section-label">
              Checked {checkedCount}/{items.length} items
            </span>
            <div className="audit-progress-bar">
              <div
                className="audit-progress-fill"
                style={{ width: items.length ? `${(checkedCount / items.length) * 100}%` : '0%' }}
              />
            </div>
          </div>

          {/* Scan button */}
          <button className="audit-scan-btn" onClick={() => showToast('Scanner coming soon', 'success')}>
            <Barcode size={28} />
            <span>Scan Barcode</span>
          </button>

          <p className="audit-divider">— or add manually —</p>

          {/* Manual input */}
          <div className="audit-manual-row">
            <div className="audit-manual-input-wrap">
              <Search size={15} className="audit-search-icon" />
              <input
                ref={manualInputRef}
                type="text"
                value={manualSku}
                onChange={e => setManualSku(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleAddManual()}
                placeholder="Enter product ID or SKU..."
              />
            </div>
            <button className="audit-add-btn" onClick={handleAddManual}>
              Add
            </button>
          </div>

          {/* Items list */}
          {items.length === 0 && (
            <p className="audit-empty">No items yet. Scan or add manually.</p>
          )}

          <div className="audit-items-list">
            {items.map(item => (
              <div key={item.tovarId} className={`audit-card ${item.checked ? `audit-card--${item.status}` : ''}`}>
                <div className="audit-card-top">
                  <div>
                    <h3>{item.name}</h3>
                    <p className="audit-sku">ID: {item.tovarId}</p>
                  </div>
                  <div className="audit-card-right">
                    {item.checked ? (
                      <span className={`audit-status-tag audit-status-tag--${item.status}`}>
                        {item.status === 'match' ? '✓ Match' : `Δ ${item.difference > 0 ? '+' : ''}${item.difference}`}
                      </span>
                    ) : (
                      <button className="audit-remove-btn" onClick={() => removeItem(item.tovarId)}>
                        <X size={14} />
                      </button>
                    )}
                  </div>
                </div>

                <div className="audit-card-bottom">
                  <div className="audit-qty-group">
                    <label>
                      Quantity
                      {item.checked && <span className="audit-plan-hint"> (system: {item.plan})</span>}
                    </label>
                    <div className="audit-qty-selector">
                      <button
                        className="audit-qty-btn"
                        onClick={() => updateQty(item.tovarId, -1)}
                        disabled={item.checked}
                      >
                        <Minus size={16} />
                      </button>
                      <span>{item.qty}</span>
                      <button
                        className="audit-qty-btn plus"
                        onClick={() => updateQty(item.tovarId, 1)}
                        disabled={item.checked}
                      >
                        <Plus size={16} />
                      </button>
                    </div>
                  </div>

                  {!item.checked && (
                    <button
                      className="audit-check-btn"
                      onClick={() => handleCheck(item)}
                      disabled={checkingId === item.tovarId}
                    >
                      {checkingId === item.tovarId
                        ? '...'
                        : <><Check size={14} /> Confirm</>
                      }
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      {started && (
        <div className="audit-footer">
          <button className="audit-footer-outline" onClick={() => navigate(-1)}>
            Cancel
          </button>
          <button
            className="audit-footer-filled"
            onClick={() => {
              if (checkedCount === 0) { showToast('Check at least one item', 'error'); return; }
              showToast(`Audit complete: ${checkedCount} items checked`, 'success');
              setTimeout(() => navigate('/'), 1200);
            }}
          >
            Finish <CheckCircle size={16} />
          </button>
        </div>
      )}
    </div>
  );
};

export default InventoryAudit;