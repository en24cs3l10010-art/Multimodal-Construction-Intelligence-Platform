import React, { useState, useEffect } from 'react';
import { CloudSun, Send, Trash2, ShieldAlert, Thermometer, Wind, Droplets } from 'lucide-react';

export default function DailyAssistantTab({ apiKey, backendUrl }) {
  const [advisories, setAdvisories] = useState(null);
  const [selectedWeatherKey, setSelectedWeatherKey] = useState('');
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        'Namaste! I am **NirmanAI**, your Senior Construction Project Director and Safety Specialist. Ask me anything regarding **IS 456 concrete standards**, **OSHA safety protocols**, **reinforcement detailing**, **rate analysis**, or **daily site execution problems**.',
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loadingChat, setLoadingChat] = useState(false);

  useEffect(() => {
    fetch(`${backendUrl}/api/weather/advisories`)
      .then((res) => res.json())
      .then((data) => {
        setAdvisories(data);
        const firstKey = Object.keys(data)[0];
        setSelectedWeatherKey(firstKey);
      })
      .catch((err) => console.error('Failed to load weather advisories', err));
  }, [backendUrl]);

  const activeWeather = advisories && selectedWeatherKey ? advisories[selectedWeatherKey] : null;

  const handleSendMessage = async (textToSend) => {
    const prompt = textToSend || inputMessage;
    if (!prompt.trim() || loadingChat) return;

    const newMsgs = [...messages, { role: 'user', content: prompt }];
    setMessages(newMsgs);
    setInputMessage('');
    setLoadingChat(true);

    try {
      const res = await fetch(`${backendUrl}/api/assistant/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMsgs,
          api_key: apiKey || null,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setMessages([...newMsgs, { role: 'assistant', content: data.response, engine: data.engine_note }]);
      }
    } catch (err) {
      setMessages([
        ...newMsgs,
        {
          role: 'assistant',
          content: `⚠️ Failed to receive response from backend: ${err.message}`,
        },
      ]);
    } finally {
      setLoadingChat(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content:
          'Namaste! I am **NirmanAI**, your Senior Construction Project Director and Safety Specialist. How can I assist with your site operations today?',
      },
    ]);
  };

  return (
    <div>
      <div className="section-hero emerald">
        <h2>🌤️ Epic 5: Daily Site Assistant & Weather-Aware Advisory</h2>
        <p>
          Dynamic micro-climate intelligence cross-referencing <strong>OSHA 1926.1431</strong> (Tower Cranes), 
          <strong>IS 7861 Part 1 & 2</strong> (Extreme Weather Concreting), and <strong>IS 3764</strong> (Excavation). 
          Includes <strong>NirmanAI</strong>, an interactive multi-turn civil engineering consultant.
        </p>
      </div>

      {/* Section 1: Weather Advisory */}
      <div className="card" style={{ marginBottom: 28 }}>
        <h3 style={{ marginBottom: 14, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
          🌦️ Site Environmental Conditions & Safety Protocol Matrix
        </h3>

        <div className="form-group">
          <label className="form-label">Select Active Site Micro-Climate / Forecast:</label>
          <select
            className="form-select"
            value={selectedWeatherKey}
            onChange={(e) => setSelectedWeatherKey(e.target.value)}
          >
            {advisories &&
              Object.keys(advisories).map((k) => (
                <option key={k} value={k}>
                  {k}
                </option>
              ))}
          </select>
        </div>

        {activeWeather && (
          <div style={{ marginTop: 16 }}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 14,
              }}
            >
              <h4 style={{ margin: 0, fontSize: '1rem', color: 'var(--text-primary)' }}>
                Alert Status: <span style={{ color: activeWeather.badge_color }}>{activeWeather.alert_level}</span>
              </h4>
              <span
                style={{
                  background: `${activeWeather.badge_color}22`,
                  color: activeWeather.badge_color,
                  border: `1px solid ${activeWeather.badge_color}`,
                  padding: '3px 12px',
                  borderRadius: 16,
                  fontWeight: 700,
                  fontSize: '0.8rem',
                }}
              >
                Condition: {activeWeather.condition_key}
              </span>
            </div>

            <div className="grid-3" style={{ marginBottom: 16 }}>
              <div
                style={{
                  background: 'var(--bg-input)',
                  borderLeft: '3px solid var(--accent-amber)',
                  padding: '12px 14px',
                  borderRadius: 'var(--radius-sm)',
                }}
              >
                <strong style={{ color: 'var(--accent-amber)', fontSize: '0.86rem' }}>
                  🏗️ Tower Crane & Lifting Status:
                </strong>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', marginTop: 4 }}>
                  {activeWeather.crane_status}
                </div>
              </div>

              <div
                style={{
                  background: 'var(--bg-input)',
                  borderLeft: '3px solid var(--accent-sky)',
                  padding: '12px 14px',
                  borderRadius: 'var(--radius-sm)',
                }}
              >
                <strong style={{ color: 'var(--accent-sky)', fontSize: '0.86rem' }}>
                  🧪 Concreting & Curing Protocol:
                </strong>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', marginTop: 4 }}>
                  {activeWeather.concreting}
                </div>
              </div>

              <div
                style={{
                  background: 'var(--bg-input)',
                  borderLeft: '3px solid var(--accent-red)',
                  padding: '12px 14px',
                  borderRadius: 'var(--radius-sm)',
                }}
              >
                <strong style={{ color: 'var(--accent-red)', fontSize: '0.86rem' }}>
                  ⚡ Electrical & Plant Safeguards:
                </strong>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', marginTop: 4 }}>
                  {activeWeather.electrical}
                </div>
              </div>
            </div>

            {/* Protocols checklist */}
            <div
              style={{
                background: 'var(--bg-input)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '14px 18px',
              }}
            >
              <strong style={{ fontSize: '0.86rem', color: 'var(--text-primary)', display: 'block', marginBottom: 8 }}>
                Mandatory Safety Protocols Checklist:
              </strong>
              {activeWeather.protocols?.map((p, i) => (
                <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 4 }}>
                  • ⚠️ {p}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Section 2: NirmanAI Multi-turn Chatbot */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.15rem', color: 'var(--text-primary)' }}>
              💬 NirmanAI: Senior Construction Engineering & Safety Consultant
            </h3>
            <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Multi-turn decision support for IS codes, structural formulas, concrete mixes, and site troubleshooting.
            </p>
          </div>
          <button className="btn-secondary" onClick={clearChat} style={{ padding: '6px 12px', fontSize: '0.78rem' }}>
            <Trash2 size={13} style={{ verticalAlign: 'middle', marginRight: 4 }} /> Clear Chat
          </button>
        </div>

        {/* Quick query chips */}
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 14 }}>
          <button
            className="btn-secondary"
            style={{ fontSize: '0.76rem', padding: '6px 10px' }}
            onClick={() =>
              handleSendMessage(
                'What is the mandatory nominal cover to reinforcement for footings, columns, and beams as per IS 456:2000 Clause 26.4?'
              )
            }
          >
            📏 IS 456 Nominal Cover
          </button>
          <button
            className="btn-secondary"
            style={{ fontSize: '0.76rem', padding: '6px 10px' }}
            onClick={() =>
              handleSendMessage(
                'What are the recommended mix proportions, W/C ratio, and cube testing requirements for M25 grade concrete?'
              )
            }
          >
            🧪 M25 Mix Design
          </button>
          <button
            className="btn-secondary"
            style={{ fontSize: '0.76rem', padding: '6px 10px' }}
            onClick={() =>
              handleSendMessage(
                'What are the safety shoring and trench protection protocols for excavations deeper than 1.5 meters under IS 3764?'
              )
            }
          >
            🚜 Deep Excavation Shoring
          </button>
          <button
            className="btn-secondary"
            style={{ fontSize: '0.76rem', padding: '6px 10px' }}
            onClick={() =>
              handleSendMessage(
                'What are the curing duration and hessian wrapping rules for concrete in hot weather as per IS 456 and IS 7861?'
              )
            }
          >
            💧 Hot-Weather Curing Rules
          </button>
        </div>

        {/* Chat Messages */}
        <div className="chat-window">
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`chat-bubble ${m.role}`}>
                <div className="chat-avatar">{m.role === 'assistant' ? '🏗️' : '👷'}</div>
                <div className="chat-text">
                  <div style={{ whiteSpace: 'pre-line' }}>{m.content}</div>
                  {m.engine && (
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 6 }}>
                      ⚡ {m.engine}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loadingChat && (
              <div className="chat-bubble assistant">
                <div className="chat-avatar">🏗️</div>
                <div className="chat-text" style={{ color: 'var(--accent-amber)' }}>
                  Consulting IS Codes & Engineering Knowledge Base...
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-bar">
            <input
              type="text"
              placeholder="Ask NirmanAI a construction engineering, IS code, or safety question..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSendMessage();
              }}
            />
            <button className="btn-primary" style={{ width: 'auto', padding: '0 18px' }} onClick={() => handleSendMessage()}>
              <Send size={15} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
