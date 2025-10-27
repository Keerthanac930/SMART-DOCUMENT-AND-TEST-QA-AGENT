import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Download, Eye, AlertTriangle, CheckCircle } from 'lucide-react';
import Layout from '../components/Layout';
import api from '../config/api';
import toast from 'react-hot-toast';

const ViewScores = () => {
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, flagged, passed

  useEffect(() => {
    window.scrollTo(0, 0);
    fetchScores();
  }, []);

  const fetchScores = async () => {
    try {
      const response = await api.get('/api/scores/all');
      setScores(response.data);
    } catch (error) {
      toast.error('Failed to load scores');
    } finally {
      setLoading(false);
    }
  };

  const filteredScores = scores.filter((score) => {
    if (filter === 'flagged') return score.is_flagged;
    if (filter === 'passed') return score.score >= 60;
    return true;
  });

  const exportToCSV = () => {
    const headers = ['Student ID', 'Test ID', 'Score', 'Violations', 'Date'];
    const rows = filteredScores.map((score) => [
      score.user_id,
      score.test_id,
      `${score.score.toFixed(2)}%`,
      score.proctoring_violations || 0,
      new Date(score.completed_at).toLocaleDateString(),
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers, ...rows].map((e) => e.join(',')).join('\n');

    const link = document.createElement('a');
    link.setAttribute('href', encodeURI(csvContent));
    link.setAttribute('download', 'test_scores.csv');
    link.click();

    toast.success('Scores exported successfully!');
  };

  if (loading) {
    return (
      <Layout admin={true}>
        <div className="flex items-center justify-center h-96">
          <div className="loading-spinner" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout admin={true}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Student Scores
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              View and analyze student performance
            </p>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={exportToCSV}
            className="btn-primary flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </motion.button>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'all'
                ? 'bg-primary text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            All Scores ({scores.length})
          </button>
          <button
            onClick={() => setFilter('passed')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'passed'
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            Passed ({scores.filter((s) => s.score >= 60).length})
          </button>
          <button
            onClick={() => setFilter('flagged')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'flagged'
                ? 'bg-red-500 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            Flagged ({scores.filter((s) => s.is_flagged).length})
          </button>
        </div>

        {/* Scores Table */}
        <div className="glass-card overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Student
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Test
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Violations
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredScores.map((score) => (
                <tr
                  key={score.id}
                  className="hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    User #{score.user_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                    Test #{score.test_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span
                        className={`text-sm font-semibold ${
                          score.score >= 60 ? 'text-green-600' : 'text-red-600'
                        }`}
                      >
                        {score.score.toFixed(1)}%
                      </span>
                      <span className="ml-2 text-xs text-gray-500">
                        ({score.correct_answers}/{score.total_questions})
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                    {score.time_taken_minutes.toFixed(0)} min
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        (score.proctoring_violations || 0) >= 10
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          : (score.proctoring_violations || 0) > 5
                          ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                          : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      }`}
                    >
                      {score.proctoring_violations || 0}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                    {new Date(score.completed_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {score.is_flagged ? (
                      <span className="flex items-center text-red-600">
                        <AlertTriangle className="w-4 h-4 mr-1" />
                        Flagged
                      </span>
                    ) : score.score >= 60 ? (
                      <span className="flex items-center text-green-600">
                        <CheckCircle className="w-4 h-4 mr-1" />
                        Passed
                      </span>
                    ) : (
                      <span className="text-gray-500">Failed</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {filteredScores.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500 dark:text-gray-400">No scores found</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default ViewScores;

