import React, { useState, useEffect } from 'react';
import './RevaluationPage.css';

const RevaluationPage = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState("");

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedItemId, setSelectedItemId] = useState(null);
  const [selectedDiscount, setSelectedDiscount] = useState(50);

  const fetchExpiringItems = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/stock/expiring/?days=7');
      if (response.ok) {
        const data = await response.json();
        setItems(data);
      }
    } catch (error) {
      console.error("Error fetching items:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpiringItems();
  }, []);

  const filteredItems = items.filter(item =>
    item.tovar_nazov.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const openDiscountModal = (id) => {
    setSelectedItemId(id);
    setIsModalOpen(true);
  };

  const handleApplyDiscount = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/stock/expiring/${selectedItemId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ discount: selectedDiscount })
      });

      if (response.ok) {
        setIsModalOpen(false);
        fetchExpiringItems();
      }
    } catch (error) {
      alert("Error updating price");
    }
  };

  return (
    <div className="revaluation-container">
      <header className="page-header">
        <h1>Items that will expire soon</h1>
      </header>

      <div className="table-card">
        <div className="search-bar">
          <div className="search-input-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search table"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        <table className="revaluation-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Quantity</th>
              <th>Expiration date</th>
              <th>Current price</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {!loading && filteredItems.map((item) => (
              <tr key={item.id}>
                <td className="product-name">{item.tovar_nazov}</td>
                <td>{item.mnozstvo}</td>
                <td className="date-text">{item.datum_exspiracie}</td>
                <td className="price-bold">${item.aktualna_cena}</td>
                <td>
                  <button className="set-discount-btn" onClick={() => openDiscountModal(item.id)}>
                    Set discount
                  </button>
                </td>
              </tr>
            ))}
            {!loading && filteredItems.length === 0 && (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#64748b' }}>
                  No items found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* MODAL POPUP */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Enter discount size</h2>
            <div className="discount-options">
              {[10, 25, 50, 75].map((value) => (
                <div
                  key={value}
                  className={`discount-box ${selectedDiscount === value ? 'active' : ''}`}
                  onClick={() => setSelectedDiscount(value)}
                >
                  {value}%
                </div>
              ))}
            </div>

            <div className="modal-actions">
              <button className="btn-cancel" onClick={() => setIsModalOpen(false)}>Cancel</button>
              <button className="btn-confirm" onClick={handleApplyDiscount}>Set discount</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RevaluationPage;