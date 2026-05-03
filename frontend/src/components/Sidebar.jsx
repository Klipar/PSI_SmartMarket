import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">📦</div>
        <span className="logo-text">Smart-Market</span>
      </div>

      <div className="sidebar-menu">
        <p className="menu-label">MENU</p>
        <nav>
          <NavLink to="/notifications" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <span className="icon">🔔</span> Notifications
          </NavLink>

          <NavLink to="/reorder" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <span className="icon">📋</span> Reorder
          </NavLink>

          <NavLink to="/revaluation" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <span className="icon">📉</span> Revaluation
          </NavLink>

          <NavLink to="/preferences" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <span className="icon">⚙️</span> Preferences
          </NavLink>
        </nav>
      </div>

      <div className="sidebar-footer">
  <div className="user-profile">
    <div className="user-avatar-placeholder">JD</div>
    <div className="user-info">
      <span className="user-name">Jason Duong</span>
      <span className="user-role">Procurement Mgr</span>
    </div>
    <span className="chevron">›</span>
  </div>
</div>
    </aside>
  );
};

export default Sidebar;