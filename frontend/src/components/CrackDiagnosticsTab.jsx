import React, { useState } from 'react';
import { Upload, Download, Activity, AlertOctagon, Wrench, FileText } from 'lucide-react';

export default function CrackDiagnosticsTab({ apiKey, backendUrl }) {
  const [sourceType, setSourceType] = useState('sample');
  const [selectedScenario, setSelectedScenario] = useState(0);
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(`${backendUrl}/static/samples/sample_concrete_crack.jpg`);
  const [loading, setLoading] = useState(false);
  const [diagData, setDiagData] = useState(null);
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
    if (scenarioIdx === 1) {
      setPreviewUrl(`${backendUrl}/static/samples/sample_hairline_crack.jpg`);
    } else {
      setPreviewUrl(`${backendUrl}/static/samples/sample_concrete_crack.jpg`);
    }
  };

  const runDiagnosis = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      if (sourceType === 'upload' && file) {
        formData.append('file', file);
      } else {
        formData.append('defect_scenario', selectedScenario);
      }

      const headers = {};
      if (apiKey) {
        headers['X-Gemini-API-Key'] = apiKey;
      }

      const res = await fetch(`${backendUrl}/api/cracks/diagnose`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`API error: ${res.statusText}`);
      }

      const data = await res.json();
      setDiagData(data);
    } catch (err) {
      alert(`Crack Diagnosis Request Failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadJson = () => {
    if (!diagData) return;
    const blob = new Blob([JSON.stringify(diagData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'structural_crack_diagnostic_report.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <div className="section-hero red">
        <h2>🧱 Epic 2: Concrete Crack Diagnostics & Structural Integrity</h2>
        <p>
          Forensic structural computer vision classifying crack typologies (<strong>Hairline</strong>, <strong>Settlement</strong>, 
          <strong>Structural Shear</strong>, <strong>Thermal Expansion</strong>, <strong>Spalling</strong>). 
          Measures crack width aperture (mm), evaluates compliance against <strong>IS 456:2000 Cl. 35.3.2</strong>, and 
          prescribes structural engineering repair specifications.
        </p>
      </div>

      <div className="grid-2">
        {/* Input Panel */}
        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
            📸 Surface Image Ingestion
          </h3>

          <div className="form-group" style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer', fontSize: '0.88rem' }}>
              <input
                type="radio"
                name="crackSource"
                checked={sourceType === 'sample'}
                onChange={() => {
                  setSourceType('sample');
                  handleSampleChange(0);
                }}
              />
              Use Built-in Calibrated Defect Samples
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer', fontSize: '0.88rem' }}>
              <input
                type="radio"
                name="crackSource"
                checked={sourceType === 'upload'}
                onChange={() => setSourceType('upload')}
              />
              Upload Custom Surface Photo
            </label>
          </div>

          {sourceType === 'sample' ? (
            <div className="form-group">
              <label className="form-label">Select Defect Scenario:</label>
              <select
                className="form-select"
                value={selectedScenario}
                onChange={(e) => handleSampleChange(Number(e.target.value))}
              >
                <option value={0}>Defect 1: Structural Shear Diagonal Crack (RCC Transfer Beam - Critical)</option>
                <option value={1}>Defect 2: Superficial Hairline Shrinkage Crazing (Slab Surface - Minor)</option>
                <option value={2}>Defect 3: Concrete Spalling & Exposed Corroded Rebar (Column Face - Emergency)</option>
              </select>
            </div>
          ) : (
            <div className="form-group">
              <label className="form-label">Upload Concrete / Masonry Photo (JPG/PNG):</label>
              <input type="file" accept="image/*" onChange={handleFileChange} className="form-input" />
            </div>
          )}

          <button className="btn-primary" onClick={runDiagnosis} disabled={loading} style={{ marginTop: 12 }}>
            {loading ? '🔬 Performing Forensic Diagnosis...' : '🔬 Perform Forensic Structural Diagnosis'}
          </button>
        </div>

        {/* Preview Panel */}
        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
            🔍 Surface Inspection Lens
          </h3>
          <div className="preview-box">
            {previewUrl ? (
              <img src={previewUrl} alt="Crack Defect Scene" onError={(e) => { e.target.style.display = 'none'; }} />
            ) : (
              <span style={{ color: 'var(--text-muted)' }}>No image loaded</span>
            )}
          </div>
        </div>
      </div>

      {/* Diagnostics Results */}
      {diagData && (
        <div style={{ marginTop: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h3 style={{ fontSize: '1.3rem', color: 'var(--text-primary)' }}>📋 Forensic Structural Diagnostic Report</h3>
            <span
              style={{
                background: diagData.is_live ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                color: diagData.is_live ? 'var(--accent-emerald)' : 'var(--accent-red)',
                border: `1px solid ${diagData.is_live ? 'var(--accent-emerald)' : 'var(--accent-red)'}`,
                padding: '4px 12px',
                borderRadius: '20px',
                fontSize: '0.8rem',
                fontWeight: 600,
              }}
            >
              {diagData.engine_note}
            </span>
          </div>

          {/* Metric Cards Row */}
          <div className="grid-4">
            <div className="metric-card">
              <div className="metric-label">Defect Typology</div>
              <div className="metric-value" style={{ color: 'var(--text-primary)', fontSize: '1.6rem' }}>
                {diagData.defect_type}
              </div>
              <div className="metric-sub">{diagData.surface_material}</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Aperture Width</div>
              <div
                className="metric-value"
                style={{
                  color:
                    diagData.severity_score >= 7
                      ? 'var(--accent-red)'
                      : diagData.severity_score >= 4
                      ? 'var(--accent-amber)'
                      : 'var(--accent-emerald)',
                }}
              >
                {diagData.estimated_crack_width_mm} <span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>mm</span>
              </div>
              <div className="metric-sub">{diagData.crack_depth_assessment}</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Severity Index</div>
              <div
                className="metric-value"
                style={{
                  color:
                    diagData.severity_score >= 7
                      ? 'var(--accent-red)'
                      : diagData.severity_score >= 4
                      ? 'var(--accent-amber)'
                      : 'var(--accent-emerald)',
                }}
              >
                {diagData.severity_score}<span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>/10</span>
              </div>
              <div className="metric-sub">Structural Collapse Risk</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Structural Urgency</div>
              <div style={{ margin: '14px 0' }}>
                <span
                  style={{
                    background:
                      diagData.structural_urgency.includes('High') || diagData.structural_urgency.includes('Critical')
                        ? '#7F1D1D'
                        : diagData.structural_urgency.includes('Medium')
                        ? '#78350F'
                        : '#064E3B',
                    color: '#F8FAFC',
                    padding: '6px 12px',
                    borderRadius: '8px',
                    fontWeight: 700,
                    fontSize: '0.9rem',
                  }}
                >
                  {diagData.structural_urgency}
                </span>
              </div>
              <div
                className="metric-sub"
                style={{
                  color: diagData.is_structural_threat ? 'var(--accent-red)' : 'var(--accent-emerald)',
                  fontWeight: 600,
                }}
              >
                {diagData.is_structural_threat ? '⚠️ THREATENS INTEGRITY' : '✅ Non-Structural'}
              </div>
            </div>
          </div>

          {/* IS 456 Compliance Banner */}
          {diagData.is456_compliance_status && (
            <div
              className="alert-box"
              style={{
                borderColor: diagData.is_structural_threat ? 'var(--accent-red)' : 'var(--accent-emerald)',
                color: 'var(--text-primary)',
              }}
            >
              <strong
                style={{ color: diagData.is_structural_threat ? 'var(--accent-red)' : 'var(--accent-emerald)' }}
              >
                IS 456:2000 Code Compliance Audit:
              </strong>{' '}
              {diagData.is456_compliance_status}
            </div>
          )}

          {/* Causes & Repairs Grid */}
          <div className="grid-2" style={{ marginTop: 24 }}>
            {/* Root Causes & Monitoring */}
            <div className="card">
              <h4 style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-primary)' }}>
                <Activity size={18} color="var(--accent-amber)" /> Forensic Root Cause Analysis
              </h4>

              {diagData.root_causes?.map((cause, i) => (
                <div
                  key={i}
                  style={{
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '12px 14px',
                    marginBottom: 10,
                    fontSize: '0.88rem',
                    color: 'var(--text-secondary)',
                  }}
                >
                  🔍 {cause}
                </div>
              ))}

              <div style={{ marginTop: 20 }}>
                <h5 style={{ color: 'var(--accent-sky)', marginBottom: 8, fontSize: '0.9rem' }}>
                  📡 Preventive Structural Monitoring:
                </h5>
                {diagData.preventive_monitoring?.map((m, i) => (
                  <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: 6 }}>
                    • <strong>{m}</strong>
                  </div>
                ))}
              </div>
            </div>

            {/* Engineering Repairs */}
            <div className="card">
              <h4 style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-primary)' }}>
                <Wrench size={18} color="var(--accent-emerald)" /> Recommended Engineering Repairs
              </h4>

              {diagData.recommended_engineering_repairs?.map((repair, i) => (
                <div
                  key={i}
                  style={{
                    background: 'var(--bg-input)',
                    borderLeft: '4px solid var(--accent-emerald)',
                    borderTop: '1px solid var(--border-color)',
                    borderRight: '1px solid var(--border-color)',
                    borderBottom: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '14px 16px',
                    marginBottom: 12,
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                    <strong style={{ color: 'var(--accent-emerald)', fontSize: '0.95rem' }}>{repair.method}</strong>
                    <span
                      style={{
                        background: '#064E3B',
                        color: '#6EE7B7',
                        padding: '2px 8px',
                        borderRadius: 6,
                        fontSize: '0.75rem',
                        fontWeight: 700,
                      }}
                    >
                      {repair.estimated_repair_cost_range_inr}
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.84rem', margin: 0, lineHeight: 1.45 }}>
                    {repair.specifications}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Export Action */}
          <div style={{ marginTop: 24, display: 'flex', gap: 16 }}>
            <button className="btn-secondary" onClick={downloadJson}>
              <Download size={15} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              Download Diagnostic JSON Report
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
              {JSON.stringify(diagData, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
