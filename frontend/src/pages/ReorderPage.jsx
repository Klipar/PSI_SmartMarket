import React, { useState, useEffect } from 'react';

const ReorderPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/orders/');
      if (response.ok) {
        const data = await response.json();
        setOrders(data);
      }
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleSmartReorder = async () => {
    setLoading(true);
    try {
      await fetch('http://127.0.0.1:8000/api/orders/smart-reorder/', {
        method: 'POST',
        headers: { 'accept': 'application/json' },
      });
      await fetchOrders(); // Оновлюємо список
    } catch (error) {
      alert("Error generating orders");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Header як на макеті */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Suggested Orders</h1>
          <p style={styles.subtitle}>Review and approve automated reorder drafts based on current inventory level</p>
        </div>
        <div style={styles.headerActions}>
          <button style={styles.btnOutline}>Filter</button>
          <button style={styles.btnOutline}>Export</button>
          <button style={styles.btnPrimary} onClick={handleSmartReorder}>+ New Order</button>
        </div>
      </div>

      {/* Таблиця */}
      <div style={styles.card}>
        <div style={styles.tableFilterBar}>
          <span style={styles.statusChip}>Status: Pending Approval ✕</span>
          <input type="text" placeholder="Search table" style={styles.searchInput} />
        </div>

        <table style={styles.table}>
          <thead>
            <tr style={styles.tableHeadRow}>
              <th style={styles.th}><input type="checkbox" /></th>
              <th style={styles.th}>SUPPLIER</th>
              <th style={styles.th}>ITEMS COUNT</th>
              <th style={styles.th}>TOTAL PRICE</th>
              <th style={styles.th}>STATUS</th>
              <th style={styles.th}>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="6" style={{textAlign:'center', padding:'20px'}}>Loading data...</td></tr>
            ) : orders.length > 0 ? (
              orders.map(order => (
                <tr key={order.id} style={styles.tr}>
                  <td style={styles.td}><input type="checkbox" /></td>
                  <td style={styles.td}>
                    <div style={styles.supplierCell}>
                      <div style={styles.avatar}>FC</div>
                      <div>
                        <div style={styles.supplierName}>{order.dodavatel_meno || 'Supplier'}</div>
                        <div style={styles.orderId}>ID: #ORD-{order.id}</div>
                      </div>
                    </div>
                  </td>
                  <td style={styles.td}>{order.items_count} items</td>
                  <td style={styles.td}><strong>${order.total_price}</strong></td>
                  <td style={styles.td}>
                    <span style={styles.badgePending}>Pending Approval</span>
                  </td>
                  <td style={styles.td}>
                    <button style={styles.btnView}>View</button>
                  </td>
                </tr>
              ))
            ) : (
              <tr><td colSpan="6" style={{textAlign:'center', padding:'20px'}}>No suggested orders found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Об'єкт зі стилями (CSS-in-JS) для швидкого результату
const styles = {
  container: { padding: '32px', backgroundColor: '#f8fafc', minHeight: '100vh', fontFamily: 'Inter, system-ui, sans-serif' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' },
  title: { fontSize: '24px', fontWeight: 'bold', margin: 0, color: '#1e293b' },
  subtitle: { color: '#64748b', margin: '4px 0 0 0' },
  headerActions: { display: 'flex', gap: '12px' },
  btnPrimary: { backgroundColor: '#2563eb', color: 'white', border: 'none', padding: '10px 18px', borderRadius: '6px', cursor: 'pointer', fontWeight: '500' },
  btnOutline: { backgroundColor: 'white', color: '#1e293b', border: '1px solid #e2e8f0', padding: '10px 18px', borderRadius: '6px', cursor: 'pointer' },
  card: { backgroundColor: 'white', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' },
  tableFilterBar: { padding: '16px', borderBottom: '1px solid #e2e8f0', display: 'flex', gap: '12px' },
  statusChip: { backgroundColor: '#f1f5f9', padding: '6px 12px', borderRadius: '20px', fontSize: '14px', color: '#475569' },
  searchInput: { padding: '8px 12px', borderRadius: '6px', border: '1px solid #e2e8f0', width: '200px' },
  table: { width: '100%', borderCollapse: 'collapse', textAlign: 'left' },
  tableHeadRow: { backgroundColor: '#f8fafc' },
  th: { padding: '12px 16px', fontSize: '12px', fontWeight: '600', color: '#64748b', textTransform: 'uppercase' },
  tr: { borderBottom: '1px solid #f1f5f9' },
  td: { padding: '16px', color: '#1e293b', verticalAlign: 'middle' },
  supplierCell: { display: 'flex', alignItems: 'center', gap: '12px' },
  avatar: { width: '36px', height: '36px', backgroundColor: '#eff6ff', color: '#2563eb', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' },
  supplierName: { fontWeight: '600' },
  orderId: { fontSize: '12px', color: '#64748b' },
  badgePending: { backgroundColor: '#fef3c7', color: '#92400e', padding: '4px 10px', borderRadius: '20px', fontSize: '12px', fontWeight: '500' },
  btnView: { background: 'none', border: 'none', color: '#2563eb', cursor: 'pointer', fontWeight: '600' }
};

export default ReorderPage;