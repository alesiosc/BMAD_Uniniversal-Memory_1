import React from 'react';
import { useSettingsStore } from '../../stores/settingsStore';
import { open } from '@tauri-apps/api/dialog';

const SUPPORTED_SITES = [
  "chat.openai.com",
];

export const SettingsView: React.FC = () => {
  const { dataDirectory, setDataDirectory } = useSettingsStore();

  const handleDirectoryChange = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: "Select Data Directory",
      });

      if (typeof selected === 'string' && selected) {
        setDataDirectory(selected);
      }
    } catch (error) {
      console.error("Error selecting directory:", error);
    }
  };

  return (
    <div className="h-full overflow-y-auto p-4 md:p-6 text-white">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      <div className="space-y-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Data Directory</h3>
          <p className="text-sm text-gray-400 mb-4">
            The local folder where your memory database is stored.
          </p>
          <div className="bg-gray-900 p-2 rounded flex items-center justify-between">
            <code className="text-sm">{dataDirectory || "Not set"}</code>
            <button
              onClick={handleDirectoryChange}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm"
            >
              Change
            </button>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Supported Websites for Capture</h3>
          <ul className="list-disc list-inside text-sm text-gray-300">
            {SUPPORTED_SITES.map(site => <li key={site}>{site}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
};