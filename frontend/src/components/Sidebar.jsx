import React, { useState } from 'react';
import {
  ShieldAlert,
  Activity,
  Calculator,
  CloudSun,
  Key,
  Layers,
  FileCheck,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, apiKey, setApiKey, isLiveBackend }) {
  const [showEpics, setShowEpics] = useState(false);
  const [showStandards, setShowStandards] = useState(false);

  const navItems = [
    { id: 'safety', label: '1. Site Safety & PPE Audit', icon: ShieldAlert, epic: 'Epic 2' },
    { id: 'cracks', label: '2. Crack Diagnostics & Integrity', icon: Activity, epic: 'Epic 2' },
    { id: 'planning', label: '3. Planning & Real Estate Valuation', icon: Calculator, epic: 'Epic 3' },
    { id: 'daily', label: '4. Daily Assistant & Weather Advisory', icon: CloudSun, epic: 'Epic 5' },
  ];

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="brand-section">
        <div className="brand-icon">🏗️</div>
        <div>
          <div className="brand-title">NirmanVision AI</div>
          <div className="brand-subtitle">Skill Wallet Capstone 1</div>
        </div>
      </div>

      {/* API Key Configuration */}
      <div className="sidebar-card">
        <h4><Key size={16} /> Google Gemini AI Engine</h4>
        <input
          type="password"
          className="api-key-input"
          placeholder="AIzaSy... (Empty for Demo)"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <div className={`engine-status-badge ${apiKey.trim() ? 'live' : 'demo'}`}>
          {apiKey.trim() ? (
            <>
              <CheckCircle2 size={13} /> Live Gemini Multimodal
            </>
          ) : (
            <>
              <AlertTriangle size={13} /> High-Fidelity Demo Engine
            </>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="nav-menu">
        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 4, fontWeight: 700 }}>
          Platform Modules
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <Icon size={18} />
              <div style={{ flex: 1 }}>
                <div>{item.label}</div>
                <div style={{ fontSize: '0.72rem', color: isActive ? 'var(--accent-amber)' : 'var(--text-muted)' }}>
                  {item.epic}
                </div>
              </div>
            </button>
          );
        })}
      </nav>

      {/* Kanban Epics Collapsible */}
      <div className="sidebar-card">
        <div
          onClick={() => setShowEpics(!showEpics)}
          style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
        >
          <h4 style={{ margin: 0 }}><Layers size={15} /> Kanban Epics</h4>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{showEpics ? '▲' : '▼'}</span>
        </div>
        {showEpics && (
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 10, lineHeight: 1.6 }}>
            <div>• <strong>Pre-reqs:</strong> FastAPI + React.js</div>
            <div>• <strong>Epic 1:</strong> Secure Config & Env</div>
            <div>• <strong>Epic 2:</strong> PPE Safety & Crack Vision</div>
            <div>• <strong>Epic 3:</strong> Project Planning & Valuation</div>
            <div>• <strong>Epic 4:</strong> JSON Data Contracts</div>
            <div>• <strong>Epic 5:</strong> Daily Weather Advisory</div>
            <div>• <strong>Epic 6:</strong> Cloud Readiness</div>
          </div>
        )}
      </div>

      {/* Standards Collapsible */}
      <div className="sidebar-card">
        <div
          onClick={() => setShowStandards(!showStandards)}
          style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
        >
          <h4 style={{ margin: 0 }}><FileCheck size={15} /> Governing Standards</h4>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{showStandards ? '▲' : '▼'}</span>
        </div>
        {showStandards && (
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 10, lineHeight: 1.6 }}>
            <div>• <strong>IS 456:2000</strong> Plain & Reinforced Concrete</div>
            <div>• <strong>OSHA 1926</strong> Safety Regulations</div>
            <div>• <strong>IS 15844 / 2925</strong> High-Vis & Hard Hats</div>
            <div>• <strong>IS 3764</strong> Trench Excavation</div>
            <div>• <strong>IS 7861</strong> Hot Weather Concreting</div>
            <div>• <strong>NBC 2016</strong> National Building Code</div>
          </div>
        )}
      </div>

      <div style={{ marginTop: 'auto', textAlign: 'center', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
        FastAPI Backend: <span style={{ color: isLiveBackend ? 'var(--accent-emerald)' : 'var(--accent-red)' }}>
          {isLiveBackend ? '● Connected (8000)' : '○ Reconnecting...'}
        </span>
      </div>
    </aside>
  );
}
