import React, { useState, useEffect } from 'react';

const ReorderPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  // Функція для виклику твого ендпоінту (створення нових чернек)
  const generateSmartReorder = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/orders/smart-reorder/', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'X-CSRFTOKEN': 'ТВІЙ_ТОКЕН', // В реальному проекті брати з cookies
        },
        body: '',
      });
      const data = await response.json();
      console.log("Generated:", data);
      // Після генерації варто оновити список (якщо є GET ендпоінт)
      // fetchOrders(); 
    } catch (error) {
      console.error("Error generating orders:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reorder-container">
      <div className="header-section">
        <div>
          <h1>Suggested Orders</h1>
          <p>Review and approve automated reorder drafts based on current inventory level</p>
        </div>
        <div className="actions">
          <button className="filter-btn">Filter</button>
          <button className="export-btn">Export</button>
          <button className="new-order-btn" onClick={generateSmartReorder}>
            {loading ? 'Processing...' : '+ New Order'}
          </button>
        </div>
      </div>

      <div className="table-card">
        <div className="table-filters">
          <span className="chip">Status: Pending Approval ✕</span>
          <input type="text" placeholder="Search table" className="search-input" />
        </div>

        <table className="orders-table">
          <thead>
            <tr>
              <th><input type="checkbox" /></th>
              <th>SUPPLIER</th>
              <th>ITEMS COUNT</th>
              <th>TOTAL PRICE</th>
              <th>STATUS</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {/* Тимчасовий рендер на основі твоєї відповіді від API */}
            {orders.length > 0 ? orders.map(order => (
              <tr key={order.id}>
                <td><input type="checkbox" /></td>
                <td>
                  <div className="supplier-info">
                    <div className="supplier-icon">FC</div>
                    <div>
                      <div className="supplier-name">Supplier ID: {order.dodavatel}</div>
                      <div className="order-id">ID: #ORD-{order.id}</div>
                    </div>
                  </div>
                </td>
                <td>12 items</td> {/* Треба буде додати в API */}
                <td>$ 2,300.00</td> {/* Треба буде додати в API */}
                <td><span className="status-pending">Pending Approval</span></td>
                <td></td>
              </tr>
            )) : (
              <tr style={{textAlign: 'center'}}><td colSpan="6">No orders found. Click "New Order" to generate.</td></tr>
            )}
          </tbody>
        </table>

        <div className="pagination">
          <span>Showing 1 to {orders.length} entities</span>
          <div className="page-buttons">
            <button disabled>Prev</button>
            <button className="active">1</button>
            <button disabled>Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReorderPage;