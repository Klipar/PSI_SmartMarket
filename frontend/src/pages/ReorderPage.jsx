import React, { useState, useEffect } from 'react';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import './ReorderPage.css';

const API_BASE = "http://localhost:8000/api/orders/";

const ReorderPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedOrderId, setExpandedOrderId] = useState(null);

  // 1. Fetching data from the backend
  const fetchOrders = async () => {
    try {
      const response = await fetch(API_BASE);
      const data = await response.json();
      setOrders(data);
      setLoading(false);
    } catch (err) {
      console.error("Fetch error:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // UC02: 5.1 Adjusting quantity (Backend request)
  const handleQuantityChange = async (orderId, itemId, newQty) => {
    try {
      await fetch(`${API_BASE}${orderId}/update_item_quantity/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: itemId, quantity: newQty })
      });
      // Refreshing locally for immediate feedback
      fetchOrders();
    } catch (err) { alert("Error updating quantity"); }
  };

    const handleConfirmOrder = async (orderId) => {
      alert(`Order #${orderId} has been successfully approved and sent to the supplier!`);
      setOrders(prevOrders => prevOrders.filter(order => order.id !== orderId));

      if (expandedOrderId === orderId) {
        setExpandedOrderId(null);
      }
    };
  // UC02: 6.1 Zamietnutie návrhu
  const handleRejectOrder = async (orderId) => {
    if (!window.confirm("Are you sure you want to delete this order draft?")) return;
    try {
      await fetch(`${API_BASE}${orderId}/`, { method: 'DELETE' });
      setOrders(orders.filter(o => o.id !== orderId));
    } catch (err) { alert("Delete error"); }
  };

  // Export to PDF
  const handleExportPDF = () => {
    try {
      const doc = new jsPDF();

      doc.setFontSize(18);
      doc.text("Suggested Orders Report", 14, 22);

      doc.setFontSize(11);
      doc.setTextColor(100);
      doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 14, 30);

      const tableColumn = ["Order ID", "Supplier", "Items Count", "Total Price", "Status"];
      const tableRows = filteredOrders.map(order => [
        `#${order.id}`,
        order.supplier_name,
        order.items_count,
        `$${Number(order.total_price).toFixed(2)}`,
        order.stav === 'OD' ? 'Sent' : 'Pending'
      ]);

      autoTable(doc, {
        head: [tableColumn],
        body: tableRows,
        startY: 35,
        theme: 'grid',
        headStyles: { fillColor: [37, 99, 235] },
      });

      doc.save("suggested_orders.pdf");
    } catch (error) {
      console.error("PDF Export Error:", error);
      alert("Error generating PDF.");
    }
  };

  // Filtering (Reactive)
  const filteredOrders = orders.filter(order =>
    order.supplier_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    order.id.toString().includes(searchQuery)
  );

  if (loading) return <div className="loading">Connecting to SmartMarket Backend...</div>;

  return (
    <div className="reorder-container">
      <header className="page-header">
        <div className="header-text">
          <h1>Suggested Orders</h1>
          <p>Review and approve automated reorder drafts</p>
        </div>
        <div className="header-actions">
          <button className="btn-secondary" onClick={() => fetchOrders()}>🔄 Refresh</button>
          <button className="btn-secondary" onClick={handleExportPDF}>📤 Export PDF</button>
        </div>
      </header>

      <div className="table-card">
        <div className="table-controls">
          <div className="search-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search by supplier or ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        <table className="reorder-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>SUPPLIER</th>
              <th>ITEMS</th>
              <th>TOTAL</th>
              <th>STATUS</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {filteredOrders.map((order) => (
              <React.Fragment key={order.id}>
                <tr>
                  <td>#{order.id}</td>
                  <td><strong>{order.supplier_name}</strong></td>
                  <td>{order.items_count} items</td>
                  <td>${Number(order.total_price).toFixed(2)}</td>
                  <td>
                    <span className={`status-badge ${order.stav === 'OD' ? 'sent' : 'pending'}`}>
                      {order.stav === 'OD' ? 'Sent' : 'Pending Approval'}
                    </span>
                  </td>
                  <td>
                    <button className="view-btn" onClick={() => setExpandedOrderId(expandedOrderId === order.id ? null : order.id)}>
                      {expandedOrderId === order.id ? 'Hide' : 'Review'}
                    </button>
                  </td>
                </tr>

                {expandedOrderId === order.id && (
                  <tr className="order-details-row">
                    <td colSpan="6">
                      <div className="order-details-card">
                        <table className="inner-table">
                          <thead>
                            <tr><th>Item</th><th>Price</th><th>Quantity</th><th>Subtotal</th></tr>
                          </thead>
                          <tbody>
                            {order.polozky.map(item => (
                              <tr key={item.id}>
                                <td>{item.tovar_name}</td>
                                <td>${item.cena_za_kus}</td>
                                <td>
                                  <input
                                    type="number"
                                    className="qty-input"
                                    defaultValue={item.navrhovane_mnozstvo}
                                    onBlur={(e) => handleQuantityChange(order.id, item.id, e.target.value)}
                                  />
                                </td>
                                <td>${(item.cena_za_kus * item.navrhovane_mnozstvo).toFixed(2)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                        <div className="order-actions">
                          {order.stav !== 'OD' && (
                            <>
                              <button className="btn-danger" onClick={() => handleRejectOrder(order.id)}>Reject</button>
                              <button className="btn-success" onClick={() => handleConfirmOrder(order.id)}>Approve & Send</button>
                            </>
                          )}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ReorderPage;