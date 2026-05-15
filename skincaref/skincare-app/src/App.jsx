import { Routes, Route } from 'react-router-dom';
import './App.css';
import Hero from './components/Hero';
import DiseaseDetection from './components/DiseaseDetection';
import SkincareAnalysis from './components/SkincareAnalysis';
import Chatbot from './components/Chatbot';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className="App">
      <Navbar />
      
      <Routes>
        <Route path="/" element={<Hero />} />
        <Route path="/disease-detection" element={<DiseaseDetection />} />
        <Route path="/skincare-analysis" element={<SkincareAnalysis />} />
        <Route path="/chatbot" element={<Chatbot />} />
      </Routes>
    </div>
  );
}

export default App;