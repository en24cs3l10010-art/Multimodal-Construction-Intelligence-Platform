import React from 'react';
import { ShieldCheck, Cpu } from 'lucide-react';

export default function Navbar({ isLiveBackend }) {
  return (
    <header className="top-header">
      <div className="header-title-group">
        <h1>
          🏗️ Multimodal Construction Intelligence Platform
          <span className="badge-capstone">FASTAPI + REACT</span>
        </h1>
        <p>
          Decision-Support AI for Safety Vision, Structural Diagnostics, CapEx Valuation in INR & Daily Site Protocols
        </p>
      </div>

      <div className="header-status-group">
        <div
          className="status-pill"
          style={{
            background: isLiveBackend ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
            color: isLiveBackend ? 'var(--accent-emerald)' : 'var(--accent-red)',
            border: `1px solid ${isLiveBackend ? 'var(--accent-emerald)' : 'var(--accent-red)'}`
          }}
        >
          <Cpu size={14} />
          {isLiveBackend ? 'FastAPI Backend Online' : 'FastAPI Connecting...'}
        </div>

        <div
          className="status-pill"
          style={{
            background: 'rgba(56, 189, 248, 0.12)',
            color: 'var(--accent-sky)',
            border: '1px solid var(--accent-sky)'
          }}
        >
          <ShieldCheck size={14} />
          IS 456 • OSHA 1926 • NBC
        </div>
      </div>
    </header>
  );
}
