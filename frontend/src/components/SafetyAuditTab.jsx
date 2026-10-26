import React, { useState } from 'react';
import { Upload, Download, CheckCircle, AlertTriangle, XCircle, Shield, FileText } from 'lucide-react';

export default function SafetyAuditTab({ apiKey, backendUrl }) {
  const [sourceType, setSourceType] = useState('sample');
  const [selectedScenario, setSelectedScenario] = useState(0);
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(`${backendUrl}/static/samples/sample_construction_ppe.jpg`);
  const [loading, setLoading] = useState(false);
  const [auditData, setAuditData] = useState(null);
  const [showJson, setShowJson] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      setFile(selected);
      setPreviewUrl(URL.createObjectURL(selected));
    }
  };

  const handleSampleChange = (scenarioIdx) => {
    setSelectedScenario(scenarioIdx);
    setFile(null);
    setPreviewUrl(`${backendUrl}/static/samples/sample_construction_ppe.jpg`);
  };

  const runAudit = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      if (sourceType === 'upload' && file) {
        formData.append('file', file);
      } else {
        formData.append('sample_scenario', selectedScenario);
      }

      const headers = {};
      if (apiKey) {
        headers['X-Gemini-API-Key'] = apiKey;
      }

      const res = await fetch(`${backendUrl}/api/safety/audit`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`API error: ${res.statusText}`);
      }

      const data = await res.json();
      setAuditData(data);
    } catch (err) {
      alert(`Safety Audit Request Failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadJson = () => {
    if (!auditData) return;
    const blob = new Blob([JSON.stringify(auditData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'construction_site_safety_audit.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <div className="section-hero amber">
        <h2>🦺 Epic 2: Site Safety Vision & PPE Compliance Audit</h2>
        <p>
          Automated multi-modal computer vision inspection under <strong>OSHA 1926</strong>, <strong>IS 15844</strong> (High-Vis), 
          <strong>IS 2925</strong> (Hard Hats), and <strong>NBC 2016 Part 7</strong>. Quantifies worker compliance, detects edge & 
          rebar hazards, and outputs strict JSON audit records.
        </p>
      </div>

      <div className="grid-2">
        {/* Input Panel */}
        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
            📷 Site Visual Ingestion
          </h3>

          <div className="form-group" style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer', fontSize: '0.88rem' }}>
              <input
                type="radio"
                name="sourceType"
                checked={sourceType === 'sample'}
                onChange={() => {
                  setSourceType('sample');
                  handleSampleChange(0);
                }}
              />
              Use Built-in Calibrated Sample
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer', fontSize: '0.88rem' }}>
              <input
                type="radio"
                name="sourceType"
                checked={sourceType === 'upload'}
                onChange={() => setSourceType('upload')}
              />
              Upload Custom Site Photo
            </label>
          </div>

          {sourceType === 'sample' ? (
            <div className="form-group">
              <label className="form-label">Select Calibrated Scenario:</label>
              <select
                className="form-select"
                value={selectedScenario}
                onChange={(e) => handleSampleChange(Number(e.target.value))}
              >
                <option value={0}>Scenario A: Scaffolding & Excavation Zone (Mixed Compliance)</option>
                <option value={1}>Scenario B: High-Elevation Shuttering Deck (Critical Fall Hazards)</option>
              </select>
            </div>
          ) : (
            <div className="form-group">
              <label className="form-label">Upload Construction Photo (JPG/PNG):</label>
              <input type="file" accept="image/*" onChange={handleFileChange} className="form-input" />
            </div>
          )}

          <button className="btn-primary" onClick={runAudit} disabled={loading} style={{ marginTop: 12 }}>
            {loading ? '🔍 Running AI Multi-Modal Audit...' : '🚀 Run AI Multimodal Safety Audit'}
          </button>
        </div>

        {/* Preview Panel */}
        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
            🖼️ Visual Inspection Lens
          </h3>
          <div className="preview-box">
            {previewUrl ? (
              <img src={previewUrl} alt="Inspection Scene" onError={(e) => { e.target.style.display = 'none'; }} />
            ) : (
              <span style={{ color: 'var(--text-muted)' }}>No image loaded</span>
            )}
          </div>
        </div>
      </div>

      {/* Audit Results */}
      {auditData && (
        <div style={{ marginTop: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h3 style={{ fontSize: '1.3rem', color: 'var(--text-primary)' }}>📊 Safety Audit Inspection Report</h3>
            <span
              style={{
                background: auditData.is_live ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                color: auditData.is_live ? 'var(--accent-emerald)' : 'var(--accent-amber)',
                border: `1px solid ${auditData.is_live ? 'var(--accent-emerald)' : 'var(--accent-amber)'}`,
                padding: '4px 12px',
                borderRadius: '20px',
                fontSize: '0.8rem',
                fontWeight: 600,
              }}
            >
              {auditData.engine_note}
            </span>
          </div>

          {/* Metric Cards Row */}
          <div className="grid-4">
            <div className="metric-card">
              <div className="metric-label">Safety Index</div>
              <div
                className="metric-value"
                style={{
                  color:
                    auditData.safety_score >= 80
                      ? 'var(--accent-emerald)'
                      : auditData.safety_score >= 60
                      ? 'var(--accent-amber)'
                      : 'var(--accent-red)',
                }}
              >
                {auditData.safety_score}<span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>/100</span>
              </div>
              <div className="metric-sub">OSHA / IS Index</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Site Status</div>
              <div style={{ margin: '14px 0' }}>
                <span
                  style={{
                    background:
                      auditData.overall_status === 'Compliant'
                        ? '#064E3B'
                        : auditData.overall_status === 'Needs Attention'
                        ? '#78350F'
                        : '#7F1D1D',
                    color: '#F8FAFC',
                    padding: '6px 14px',
                    borderRadius: '8px',
                    fontWeight: 700,
                    fontSize: '1rem',
                  }}
                >
                  {auditData.overall_status}
                </span>
              </div>
              <div className="metric-sub">Audit Classification</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Personnel Count</div>
              <div className="metric-value" style={{ color: 'var(--accent-sky)' }}>
                {auditData.workers_detected}
              </div>
              <div className="metric-sub">Workers in Field</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Severe Hazards</div>
              <div
                className="metric-value"
                style={{
                  color:
                    auditData.hazards_identified?.some((h) => h.severity === 'Critical' || h.severity === 'High')
                      ? 'var(--accent-red)'
                      : 'var(--accent-emerald)',
                }}
              >
                {auditData.hazards_identified?.filter((h) => h.severity === 'Critical' || h.severity === 'High').length || 0}
              </div>
              <div className="metric-sub">Immediate Action Required</div>
            </div>
          </div>

          {/* Summary Box */}
          {auditData.audit_summary && (
            <div className="alert-box" style={{ borderColor: 'var(--accent-sky)', color: 'var(--text-primary)' }}>
              <strong style={{ color: 'var(--accent-sky)' }}>Executive Summary:</strong> {auditData.audit_summary}
            </div>
          )}

          {/* PPE & Hazards Split */}
          <div className="grid-2" style={{ marginTop: 24 }}>
            {/* PPE Checklist */}
            <div className="card">
              <h4 style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-primary)' }}>
                <Shield size={18} color="var(--accent-emerald)" /> PPE Verification Matrix
              </h4>

              {Object.entries(auditData.ppe_detection || {}).map(([key, val]) => {
                const isPass = val.status === 'Pass' || val.status === 'Compliant';
                const isWarn = val.status === 'Warning';
                const isFail = val.status === 'Fail' || val.status === 'Non-Compliant';

                const badgeBg = isPass ? '#064E3B' : isWarn ? '#78350F' : isFail ? '#7F1D1D' : '#1E293B';
                const badgeColor = isPass ? '#34D399' : isWarn ? '#FBBF24' : isFail ? '#F87171' : '#94A3B8';

                return (
                  <div
                    key={key}
                    style={{
                      background: 'var(--bg-input)',
                      border: '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '12px 14px',
                      marginBottom: 10,
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontWeight: 600, fontSize: '0.88rem', textTransform: 'capitalize' }}>
                        {key.replace(/_/g, ' ')}
                      </span>
                      <span
                        style={{
                          background: badgeBg,
                          color: badgeColor,
                          padding: '2px 8px',
                          borderRadius: 6,
                          fontSize: '0.74rem',
                          fontWeight: 700,
                        }}
                      >
                        {val.status}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{val.notes}</div>
                    {val.compliant_count !== undefined && (
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: 4 }}>
                        Compliant: {val.compliant_count} | Non-Compliant: {val.non_compliant_count}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Hazards & Directives */}
            <div className="card">
              <h4 style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-primary)' }}>
                <AlertTriangle size={18} color="var(--accent-red)" /> Identified Hazards & Corrective Remedies
              </h4>

              {auditData.hazards_identified?.map((h) => {
                const borderCol =
                  h.severity === 'Critical'
                    ? 'var(--accent-red)'
                    : h.severity === 'High'
                    ? '#F97316'
                    : h.severity === 'Medium'
                    ? 'var(--accent-amber)'
                    : 'var(--accent-sky)';

                return (
                  <div
                    key={h.id}
                    style={{
                      background: 'var(--bg-input)',
                      borderLeft: `4px solid ${borderCol}`,
                      borderTop: '1px solid var(--border-color)',
                      borderRight: '1px solid var(--border-color)',
                      borderBottom: '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '12px 14px',
                      marginBottom: 10,
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <strong style={{ fontSize: '0.88rem', color: 'var(--text-primary)' }}>{h.hazard_title}</strong>
                      <span style={{ fontSize: '0.72rem', fontWeight: 700, color: borderCol }}>
                        {h.severity.toUpperCase()}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)', margin: '4px 0' }}>
                      📜 {h.regulatory_code} | 📍 {h.location_in_image}
                    </div>
                    <div
                      style={{
                        background: '#070A10',
                        padding: '6px 10px',
                        borderRadius: 4,
                        fontSize: '0.8rem',
                        marginTop: 4,
                      }}
                    >
                      <span style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>🛠️ Remedy:</span>{' '}
                      <span style={{ color: 'var(--text-secondary)' }}>{h.corrective_remedy}</span>
                    </div>
                  </div>
                );
              })}

              {auditData.immediate_directives?.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--accent-amber)', marginBottom: 6 }}>
                    ⚡ Immediate Action Directives:
                  </div>
                  {auditData.immediate_directives.map((dir, i) => (
                    <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 4 }}>
                      • {dir}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Export Action */}
          <div style={{ marginTop: 24, display: 'flex', gap: 16 }}>
            <button className="btn-secondary" onClick={downloadJson}>
              <Download size={15} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              Download Official JSON Report
            </button>
            <button className="btn-secondary" onClick={() => setShowJson(!showJson)}>
              <FileText size={15} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              {showJson ? 'Hide Raw JSON' : 'Inspect JSON Contract'}
            </button>
          </div>

          {showJson && (
            <pre
              style={{
                marginTop: 16,
                background: '#070A10',
                border: '1px solid var(--border-color)',
                padding: 16,
                borderRadius: 'var(--radius-md)',
                fontSize: '0.82rem',
                color: '#38BDF8',
                overflowX: 'auto',
              }}
            >
              {JSON.stringify(auditData, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
