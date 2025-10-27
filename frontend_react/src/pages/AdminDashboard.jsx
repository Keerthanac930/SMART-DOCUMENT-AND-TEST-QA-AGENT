import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  FilePlus,
  BarChart3,
  Users,
  FileText,
  TrendingUp,
  Clock,
  CheckCircle,
} from 'lucide-react';
import Layout from '../components/Layout';
import StatCard from '../components/StatCard';
import api from '../config/api';
import toast from 'react-hot-toast';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recentTests, setRecentTests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    window.scrollTo(0, 0);
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, testsRes] = await Promise.all([
        api.get('/api/admin/dashboard/stats'),
        api.get('/api/admin/tests'),
      ]);

      setStats(statsRes.data);
      setRecentTests(testsRes.data.slice(0, 5));
    } catch (error) {
      console.error('Dashboard fetch error:', error);
      toast.error('Failed to load dashboard data');
      // Set empty data to prevent blank screen
      setStats({
        users: { total_users: 0, active_users: 0, new_users_this_month: 0 },
        tests: { total_tests: 0, active_tests: 0, total_attempts: 0, average_score: 0 },
        documents: { total_documents: 0, total_words: 0, documents_by_type: {} }
      });
      setRecentTests([]);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Create Test',
      icon: FilePlus,
      color: 'from-blue-500 to-blue-600',
      action: () => navigate('/admin/create-test'),
    },
    {
      title: 'View Scores',
      icon: BarChart3,
      color: 'from-green-500 to-green-600',
      action: () => navigate('/admin/scores'),
    },
    {
      title: 'Manage Users',
      icon: Users,
      color: 'from-purple-500 to-purple-600',
      action: () => navigate('/admin/users'),
    },
    {
      title: 'Documents',
      icon: FileText,
      color: 'from-orange-500 to-orange-600',
      action: () => navigate('/admin/documents'),
    },
  ];

  if (loading) {
    return (
      <Layout admin={true}>
        <div className="flex items-center justify-center h-96">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-900 dark:text-white ml-4 text-lg">Loading dashboard...</p>
        </div>
      </Layout>
    );
  }

  if (!stats) {
    return (
      <Layout admin={true}>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Welcome to Admin Dashboard</h2>
            <p className="text-gray-600 dark:text-gray-400">Unable to load statistics. Please refresh the page.</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout admin={true}>
      <div className="space-y-4">
        {/* Header */}
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
            Admin Dashboard
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage tests, view analytics, and oversee student performance
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Users"
            value={stats?.users?.total_users || 0}
            icon={Users}
            trend="+12%"
            color="blue"
          />
          <StatCard
            title="Total Tests"
            value={stats?.tests?.total_tests || 0}
            icon={FileText}
            trend="+8%"
            color="green"
          />
          <StatCard
            title="Test Attempts"
            value={stats?.tests?.total_attempts || 0}
            icon={TrendingUp}
            trend="+23%"
            color="purple"
          />
          <StatCard
            title="Avg Score"
            value={`${(stats?.tests?.average_score || 0).toFixed(1)}%`}
            icon={CheckCircle}
            trend="+5%"
            color="orange"
          />
        </div>

        {/* Quick Actions */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={action.action}
                className="cursor-pointer"
              >
                <div className={`glass-card p-6 bg-gradient-to-br ${action.color}`}>
                  <action.icon className="w-8 h-8 text-white mb-3" />
                  <h3 className="text-lg font-semibold text-white">
                    {action.title}
                  </h3>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Recent Tests */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Recent Tests
          </h2>
          <div className="glass-card overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Test Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Topic
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Questions
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Created
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {recentTests.map((test) => (
                  <tr
                    key={test.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer"
                    onClick={() => navigate(`/admin/tests/${test.id}`)}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      {test.test_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      {test.topic}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      {test.questions?.length || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-semibold rounded-full ${
                          test.is_active
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                        }`}
                      >
                        {test.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      {new Date(test.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AdminDashboard;
