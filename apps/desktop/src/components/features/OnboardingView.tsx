import React, { useState, useEffect } from 'react';
import { useSettingsStore } from '../../stores/settingsStore';

export const OnboardingView: React.FC = () => {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'ok' | 'error'>('checking');
  const setHasCompletedOnboarding = useSettingsStore((state) => state.setHasCompletedOnboarding);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then(res => res.ok ? setBackendStatus('ok') : setBackendStatus('error'))
      .catch(() => setBackendStatus('error'));
  }, []);

  return (
    <div className="bg-gray-900 text-white h-screen flex flex-col items-center justify-center text-center p-8">
      <div className="max-w-md">
        <h1 className="text-3xl font-bold mb-4">Welcome to Universal Memory</h1>
        <p className="text-gray-400 mb-8">
          This application acts as your external brain, automatically capturing your AI conversations so you never lose context again.
        </p>

        <div className="space-y-6 text-left">
          <div className="flex items-start gap-4">
            <div className="text-2xl mt-1">1.</div>
            <div>
              <h2 className="font-semibold">Install the Browser Extension</h2>
              <p className="text-sm text-gray-400">The extension is required to automatically capture conversations from the web.</p>
              <a 
                href="https://chrome.google.com/webstore" // Placeholder URL
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 text-sm"
              >
                Install for Chrome
              </a>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="text-2xl mt-1">2.</div>
            <div>
              <h2 className="font-semibold">Backend Status Check</h2>
              <p className="text-sm text-gray-400">Confirming the local memory service is running.</p>
              <div className="mt-2">
                {backendStatus === 'checking' && <p className="text-yellow-400">Checking...</p>}
                {backendStatus === 'ok' && <p className="text-green-400">✓ Local service connected</p>}
                {backendStatus === 'error' && <p className="text-red-400">✗ Could not connect to local service. Please restart the app.</p>}
              </div>
            </div>
          </div>
        </div>

        <button
          onClick={() => setHasCompletedOnboarding(true)}
          disabled={backendStatus !== 'ok'}
          className="mt-10 w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded disabled:bg-gray-600 disabled:cursor-not-allowed"
        >
          Get Started
        </button>
      </div>
    </div>
  );
};