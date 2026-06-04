import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import AutoServicioBannerPage from './pages/AutoServicioBannerPage';
import BolsaEmpleoPage from './pages/BolsaEmpleoPage';
import TeacherDashboard from './pages/TeacherDashboard';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/banner" element={<AutoServicioBannerPage />} />
        <Route path="/empleo" element={<BolsaEmpleoPage />} />

        {/* Protected Dashboard */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute allowedRoles={['student', 'admin']}>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        <Route
          path="/teacher"
          element={
            <ProtectedRoute allowedRoles={['teacher']}>
              <TeacherDashboard />
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<LandingPage />} />
      </Routes>
    </Router>
  );
}

export default App;
