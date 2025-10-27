import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { useUI } from '../contexts/UIContext';
import { useAuth } from '../contexts/AuthContext';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import QuickActions from '../components/QuickActions';
import { CheckSquare, FileText, TrendingUp, Upload } from 'lucide-react';
import api from '../config/api';
import toast from 'react-hot-toast';

// Import dashboard sections
import AskAISection from './sections/AskAISection';
import UploadDocumentSection from './sections/UploadDocumentSection';
import AvailableTestsSection from './sections/AvailableTestsSection';
import CompletedTestsSection from './sections/CompletedTestsSection';
import MyDocumentsSection from './sections/MyDocumentsSection';
import SettingsSection from './sections/SettingsSection';

const Dashboard = () => {
  const { activeSection } = useUI();
  const { user } = useAuth();
  const [stats, setStats] = useState([
    { title: 'Available Tests', value: '0', icon: CheckSquare, color: 'blue' },
    { title: 'Completed Tests', value: '0', icon: CheckSquare, color: 'green' },
    { title: 'Average Score', value: '0%', icon: TrendingUp, color: 'purple' },
    { title: 'Documents', value: '0', icon: FileText, color: 'orange' },
  ]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, [activeSection]); // Refetch when returning to dashboard

  useEffect(() => {
    // Listen for document uploads and test completions
    const handleDocumentsUpdated = () => {
      fetchDashboardStats();
    };

    window.addEventListener('documents-updated', handleDocumentsUpdated);
    window.addEventListener('test-completed', handleDocumentsUpdated);

    return () => {
      window.removeEventListener('documents-updated', handleDocumentsUpdated);
      window.removeEventListener('test-completed', handleDocumentsUpdated);
    };
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await api.get('/api/user/stats');
      const data = response.data;
      
      setStats([
        { title: 'Available Tests', value: String(data.total_tests), icon: CheckSquare, color: 'blue' },
        { title: 'Completed Tests', value: String(data.completed_tests), icon: CheckSquare, color: 'green' },
        { title: 'Average Score', value: `${data.average_score}%`, icon: TrendingUp, color: 'purple' },
        { title: 'Documents', value: String(data.total_documents), icon: FileText, color: 'orange' },
      ]);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      // Don't show error toast if user isn't logged in yet
      if (error.response?.status !== 401) {
        toast.error('Failed to load dashboard statistics');
      }
    } finally {
      setLoading(false);
    }
  };

  const renderSection = () => {
    switch (activeSection) {
      case 'ask-ai':
        return <AskAISection />;
      case 'upload-document':
        return <UploadDocumentSection />;
      case 'available-tests':
        return <AvailableTestsSection />;
      case 'completed-tests':
        return <CompletedTestsSection />;
      case 'my-documents':
        return <MyDocumentsSection />;
      case 'settings':
        return <SettingsSection />;
      default:
        return <DashboardHome stats={stats} user={user} />;
    }
  };

  return (
    <div className="min-h-screen flex bg-background-light dark:bg-background-dark">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 lg:ml-0">
        <div className="p-6">
          <Navbar />

          {/* Dynamic Content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderSection()}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

// Dashboard Home Component
const DashboardHome = ({ stats, user }) => {
  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-8"
      >
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome back, {user?.username || 'User'} 👋
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Ready to continue your learning journey? Here's what's happening today.
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatCard key={stat.title} {...stat} index={index} />
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-2xl font-bold text-gray-900 dark:text-white mb-6"
        >
          Quick Actions
        </motion.h2>
        <QuickActions />
      </div>

      {/* Recent Activity (Optional) */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="glass-card p-6"
      >
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Recent Activity
        </h3>
        <div className="space-y-3">
          {[
            { action: 'Completed Quiz', name: 'Python Basics', time: '2 hours ago' },
            { action: 'Uploaded Document', name: 'Machine Learning Notes', time: '5 hours ago' },
            { action: 'Asked AI', name: 'What is polymorphism?', time: '1 day ago' },
          ].map((activity, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 + index * 0.1 }}
              className="flex items-center justify-between p-4 rounded-xl hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all"
            >
              <div>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {activity.action}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {activity.name}
                </p>
              </div>
              <span className="text-sm text-gray-500">{activity.time}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;

