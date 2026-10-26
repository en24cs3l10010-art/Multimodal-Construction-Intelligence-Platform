import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import SafetyAuditTab from './components/SafetyAuditTab';
import CrackDiagnosticsTab from './components/CrackDiagnosticsTab';
import PlanningValuationTab from './components/PlanningValuationTab';
import DailyAssistantTab from './components/DailyAssistantTab';

const BACKEND_URL = 'http://127.0.0.1:8000';

export default function App() {
  const [activeTab, setActiveTab] = useState('safety');
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('gemini_api_key') || '');
  const [isLiveBackend, setIsLiveBackend] = useState(false);

  // Sync API key to localStorage
  useEffect(() => {
    localStorage.setItem('gemini_api_key', apiKey);
  }, [apiKey]);

  // Health check polling on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/health`);
        if (res.ok) {
          setIsLiveBackend(true);
        } else {
          setIsLiveBackend(false);
        }
      } catch (err) {
        setIsLiveBackend(false);
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-layout">
      {/* Sidebar Navigation & Engine Configuration */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiKey={apiKey}
        setApiKey={setApiKey}
        isLiveBackend={isLiveBackend}
      />

      {/* Main Panel */}
      <div className="main-wrapper">
        <Navbar isLiveBackend={isLiveBackend} />

        <main className="content-area">
          {activeTab === 'safety' && (
            <SafetyAuditTab apiKey={apiKey} backendUrl={BACKEND_URL} />
          )}

          {activeTab === 'cracks' && (
            <CrackDiagnosticsTab apiKey={apiKey} backendUrl={BACKEND_URL} />
          )}

          {activeTab === 'planning' && (
            <PlanningValuationTab backendUrl={BACKEND_URL} />
          )}

          {activeTab === 'daily' && (
            <DailyAssistantTab apiKey={apiKey} backendUrl={BACKEND_URL} />
          )}
        </main>
      </div>
    </div>
  );
}
