import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { UIProvider } from './contexts/UIContext';
import { ThemeProvider } from './contexts/ThemeContext';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import AdminUsers from './pages/AdminUsers';
import AdminDocuments from './pages/AdminDocuments';
import CreateTest from './pages/CreateTest';
import ViewScores from './pages/ViewScores';
import TakeTest from './pages/TakeTest';
import ProtectedRoute from './components/ProtectedRoute';

// Smart redirect component based on user role
const SmartRedirect = () => {
  const { isAdmin } = useAuth();
  return <Navigate to={isAdmin() ? '/admin/dashboard' : '/dashboard'} replace />;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <ThemeProvider>
          <UIProvider>
            <div className="min-h-screen">
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              
              {/* Student Routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute studentOnly={true}>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/tests/:testId"
                element={
                  <ProtectedRoute>
                    <TakeTest />
                  </ProtectedRoute>
                }
              />
              
              {/* Admin Routes */}
              <Route
                path="/admin/dashboard"
                element={
                  <ProtectedRoute adminOnly={true}>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/users"
                element={
                  <ProtectedRoute adminOnly={true}>
                    <AdminUsers />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/documents"
                element={
                  <ProtectedRoute adminOnly={true}>
                    <AdminDocuments />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/create-test"
                element={
                  <ProtectedRoute adminOnly={true}>
                    <CreateTest />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/scores"
                element={
                  <ProtectedRoute adminOnly={true}>
                    <ViewScores />
                  </ProtectedRoute>
                }
              />
              
              {/* Default redirect */}
              <Route 
                path="/" 
                element={
                  <ProtectedRoute>
                    <SmartRedirect />
                  </ProtectedRoute>
                } 
              />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>

            {/* Toast Notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 3000,
                style: {
                  background: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '12px',
                  padding: '16px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                },
                success: {
                  iconTheme: {
                    primary: '#10b981',
                    secondary: '#fff',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: '#fff',
                  },
                },
              }}
            />
          </div>
          </UIProvider>
        </ThemeProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
