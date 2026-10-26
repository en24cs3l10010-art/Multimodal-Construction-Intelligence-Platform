import React, { useState, useEffect } from 'react';
import { Calculator, Sparkles, TrendingUp, Layers, Box } from 'lucide-react';

export default function PlanningValuationTab({ backendUrl }) {
  const [metadata, setMetadata] = useState(null);
  const [selectedTier, setSelectedTier] = useState('');
  const [selectedStructure, setSelectedStructure] = useState('');
  const [builtUpSqft, setBuiltUpSqft] = useState(25000);
  const [completionPct, setCompletionPct] = useState(45);
  const [archStyle, setArchStyle] = useState('Modern Glass & Steel Biophilic High-Rise');
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showRender, setShowRender] = useState(false);

  // Fetch metadata on mount
  useEffect(() => {
    fetch(`${backendUrl}/api/planning/metadata`)
      .then((res) => res.json())
      .then((data) => {
        setMetadata(data);
        const firstTier = Object.keys(data)[0];
        setSelectedTier(firstTier);
        if (data[firstTier]?.structures?.length) {
          setSelectedStructure(data[firstTier].structures[1] || data[firstTier].structures[0]);
        }
      })
      .catch((err) => console.error('Failed to load planning metadata', err));
  }, [backendUrl]);

  // Recalculate estimate whenever inputs change
  useEffect(() => {
    if (!selectedTier || !selectedStructure) return;
    fetchEstimate();
  }, [selectedTier, selectedStructure, builtUpSqft, completionPct, archStyle]);

  const fetchEstimate = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${backendUrl}/api/planning/estimate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          city_tier_key: selectedTier,
          structure_type: selectedStructure,
          built_up_sqft: Number(builtUpSqft),
          completion_pct: Number(completionPct),
          arch_style: archStyle,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setEstimate(data);
      }
    } catch (err) {
      console.error('Estimate error', err);
    } finally {
      setLoading(false);
    }
  };

  const currentStructures = metadata && selectedTier ? metadata[selectedTier]?.structures || [] : [];

  return (
    <div>
      <div className="section-hero sky">
        <h2>🏗️ Epic 3: Construction Project Planning & Real Estate Valuation</h2>
        <p>
          Dynamic cost estimation, CapEx expenditure tracking, and finished market valuation in <strong>INR (Lakhs / Crores)</strong> 
          calibrated for <strong>Tier 1 / 2 / 3 Indian Metro benchmarks</strong>. Computes IS 456 material requirements 
          (Cement bags, Fe500D TMT Steel metric tonnes) and generates conceptual 3D architectural renders.
        </p>
      </div>

      {/* Control Panel */}
      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ marginBottom: 16, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
          ⚙️ Project Parameters & Indian Metro Benchmarks
        </h3>

        <div className="grid-3">
          <div className="form-group">
            <label className="form-label">📍 Location Tier & Metro Cluster:</label>
            <select
              className="form-select"
              value={selectedTier}
              onChange={(e) => {
                const newTier = e.target.value;
                setSelectedTier(newTier);
                if (metadata && metadata[newTier]?.structures?.length) {
                  setSelectedStructure(metadata[newTier].structures[0]);
                }
              }}
            >
              {metadata &&
                Object.keys(metadata).map((tierKey) => (
                  <option key={tierKey} value={tierKey}>
                    {tierKey}
                  </option>
                ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">🏢 Structure & Asset Typology:</label>
            <select
              className="form-select"
              value={selectedStructure}
              onChange={(e) => setSelectedStructure(e.target.value)}
            >
              {currentStructures.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">📐 Built-Up Area (Sq.Ft):</label>
            <input
              type="number"
              className="form-input"
              value={builtUpSqft}
              min={500}
              max={2000000}
              step={1000}
              onChange={(e) => setBuiltUpSqft(Number(e.target.value))}
            />
          </div>
        </div>

        <div className="grid-2" style={{ marginTop: 8 }}>
          <div className="form-group">
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
              <label className="form-label" style={{ margin: 0 }}>
                ⏳ Construction Progress:
              </label>
              <strong style={{ color: 'var(--accent-amber)', fontSize: '0.9rem' }}>{completionPct}% Complete</strong>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={completionPct}
              onChange={(e) => setCompletionPct(Number(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-amber)' }}
            />
          </div>

          <div className="form-group">
            <label className="form-label">🎨 Conceptual Architecture Style:</label>
            <select className="form-select" value={archStyle} onChange={(e) => setArchStyle(e.target.value)}>
              <option value="Modern Glass & Steel Biophilic High-Rise">Modern Glass & Steel Biophilic High-Rise</option>
              <option value="Brutalist Exposed RCC Minimalist Architecture">Brutalist Exposed RCC Minimalist Architecture</option>
              <option value="Sustainable Contemporary Indian Vernacular with Terracotta">
                Sustainable Contemporary Indian Vernacular with Terracotta
              </option>
              <option value="Sleek Neo-Classical Luxury Development">Sleek Neo-Classical Luxury Development</option>
              <option value="Industrial High-Tech Pre-Engineered Structure">Industrial High-Tech Pre-Engineered Structure</option>
            </select>
          </div>
        </div>
      </div>

      {estimate && (
        <div>
          {/* Milestone Progress Bar */}
          <div
            className="card"
            style={{
              padding: '16px 20px',
              marginBottom: 24,
              borderColor: estimate.milestone_color,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <span style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)' }}>
                📍 Milestone Stage: <span style={{ color: estimate.milestone_color }}>{estimate.milestone_title}</span>
              </span>
              <span
                style={{
                  background: 'var(--bg-input)',
                  color: 'var(--accent-sky)',
                  padding: '4px 12px',
                  borderRadius: 12,
                  fontWeight: 700,
                  fontSize: '0.85rem',
                }}
              >
                {completionPct}% Complete
              </span>
            </div>
            <div className="progress-container">
              <div className="progress-fill" style={{ width: `${completionPct}%` }} />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-muted)' }}>
              <span>0% Substructure</span>
              <span>25% RCC Staging</span>
              <span>50% Mid-Rise Slabs</span>
              <span>75% MEP & Envelope</span>
              <span>100% Commissioning</span>
            </div>
          </div>

          {/* Primary Financial & Valuation Cards */}
          <h3 style={{ fontSize: '1.2rem', marginBottom: 16, color: 'var(--text-primary)' }}>
            💰 Capital Expenditure (CapEx) & Real Estate Valuation (INR)
          </h3>

          <div className="grid-4">
            <div className="metric-card">
              <div className="metric-label">Total Project Budget</div>
              <div className="metric-value" style={{ color: 'var(--text-primary)' }}>
                {estimate.total_project_budget_formatted}
              </div>
              <div className="metric-sub">₹{estimate.cost_per_sqft?.toLocaleString()}/sqft Base Cost</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">CapEx Incurred to Date</div>
              <div className="metric-value" style={{ color: 'var(--accent-amber)' }}>
                {estimate.capex_incurred_formatted}
              </div>
              <div className="metric-sub">Remaining: {estimate.capex_remaining_formatted}</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Current Stage Asset Value</div>
              <div className="metric-value" style={{ color: 'var(--accent-sky)' }}>
                {estimate.current_asset_valuation_formatted}
              </div>
              <div className="metric-sub">Market Stage Equity</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Finished Market Valuation</div>
              <div className="metric-value" style={{ color: 'var(--accent-emerald)' }}>
                {estimate.finished_market_valuation_formatted}
              </div>
              <div className="metric-sub" style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>
                Gain: +{estimate.unrealized_equity_spread_formatted}
              </div>
            </div>
          </div>

          {/* Material Quantification & 3D Render Split */}
          <div className="grid-2" style={{ marginTop: 28 }}>
            {/* IS 456 Materials */}
            <div className="card">
              <h4 style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-primary)' }}>
                <Layers size={18} color="var(--accent-amber)" /> IS 456 Material Quantification
              </h4>

              <div
                style={{
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '14px 16px',
                  marginBottom: 12,
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>🏗️ Cement Requirement (50 kg Bags)</span>
                  <strong style={{ color: 'var(--accent-sky)', fontSize: '1.15rem' }}>
                    {estimate.materials?.cement_bags_total?.toLocaleString()} Bags
                  </strong>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  Consumed to date: <strong>{estimate.materials?.cement_bags_used?.toLocaleString()} Bags</strong>
                </div>
              </div>

              <div
                style={{
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '14px 16px',
                  marginBottom: 12,
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>⚙️ TMT Fe500D Reinforcement Steel</span>
                  <strong style={{ color: 'var(--accent-amber)', fontSize: '1.15rem' }}>
                    {estimate.materials?.steel_tonnes_total} MT
                  </strong>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  Procured & tied: <strong>{estimate.materials?.steel_tonnes_used} MT</strong>
                </div>
              </div>

              <div
                style={{
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '14px 16px',
                  marginBottom: 12,
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>🪨 Coarse Aggregate (20mm / 10mm)</span>
                  <strong style={{ color: 'var(--accent-purple)', fontSize: '1.15rem' }}>
                    {estimate.materials?.coarse_aggregate_cuft?.toLocaleString()} cu.ft
                  </strong>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  Standard IS 383 grading specification.
                </div>
              </div>

              <div
                style={{
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '14px 16px',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>🏖️ Manufactured Sand (M-Sand)</span>
                  <strong style={{ color: 'var(--accent-emerald)', fontSize: '1.15rem' }}>
                    {estimate.materials?.msand_cuft?.toLocaleString()} cu.ft
                  </strong>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  Eco-friendly Zone II crushed rock fine aggregate.
                </div>
              </div>
            </div>

            {/* Pollinations 3D Render Studio */}
            <div className="card">
              <h4 style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-primary)' }}>
                <Sparkles size={18} color="var(--accent-sky)" /> Conceptual 3D Architectural Studio
              </h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: 12 }}>
                Synthesized architectural visualization generated dynamically via Pollinations AI.
              </p>

              <div
                style={{
                  background: '#070A10',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '10px 12px',
                  fontSize: '0.78rem',
                  color: '#94A3B8',
                  marginBottom: 14,
                  lineHeight: 1.4,
                }}
              >
                <strong style={{ color: 'var(--accent-amber)' }}>Prompt:</strong> {estimate.pollinations_prompt}
              </div>

              <button
                className="btn-secondary"
                style={{ width: '100%', marginBottom: 14 }}
                onClick={() => setShowRender(!showRender)}
              >
                <Sparkles size={14} style={{ verticalAlign: 'middle', marginRight: 6 }} />
                {showRender ? 'Refresh 3D Visualization' : 'Generate 3D Concept Visual'}
              </button>

              {showRender && (
                <div className="preview-box" style={{ height: 260 }}>
                  <img
                    src={estimate.pollinations_url}
                    alt="Conceptual 3D Architecture"
                    onError={(e) => {
                      e.target.alt = 'Generating render... please click again in a few seconds.';
                    }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
