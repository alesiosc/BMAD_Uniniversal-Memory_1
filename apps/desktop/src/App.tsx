import './App.css';
import { MemoryFeed } from './components/features/MemoryFeed';
import { ConversationView } from './components/features/ConversationView';
import { ModelComparisonView } from './components/features/ModelComparisonView';
import { SettingsView } from './components/features/SettingsView';
import { OnboardingView } from './components/features/OnboardingView';
import { SearchBar } from './components/ui/SearchBar';
import { ImportButton } from './components/features/ImportButton';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useSettingsStore } from './stores/settingsStore';

const MainApp = () => (
  <BrowserRouter>
    <main className="bg-gray-900 text-white h-screen flex flex-col">
      <header className="p-4 border-b border-gray-700 flex justify-between items-center gap-4">
        <div className="flex items-center gap-4">
          <Link to="/"><h1 className="text-xl font-bold">Universal Memory</h1></Link>
          <nav className="flex items-center gap-4">
            <Link to="/compare" className="text-sm text-gray-300 hover:text-white">Compare Models</Link>
            <Link to="/settings" className="text-sm text-gray-300 hover:text-white">Settings</Link>
          </nav>
        </div>
        <div className="flex-grow flex justify-center"><SearchBar /></div>
        <ImportButton />
      </header>
      <div className="flex-grow overflow-hidden">
        <Routes>
          <Route path="/" element={<MemoryFeed />} />
          <Route path="/conversation/:id" element={<ConversationView />} />
          <Route path="/compare" element={<ModelComparisonView />} />
          <Route path="/settings" element={<SettingsView />} />
        </Routes>
      </div>
    </main>
  </BrowserRouter>
);

function App() {
  const hasCompletedOnboarding = useSettingsStore((state) => state.hasCompletedOnboarding);
  return hasCompletedOnboarding ? <MainApp /> : <OnboardingView />;
}

export default App;