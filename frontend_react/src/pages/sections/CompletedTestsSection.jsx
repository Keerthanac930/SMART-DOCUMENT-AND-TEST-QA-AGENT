import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Award, TrendingUp, Calendar, Loader2 } from 'lucide-react';
import api from '../../config/api';
import toast from 'react-hot-toast';

const CompletedTestsSection = () => {
  const [completedTests, setCompletedTests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMyScores();
  }, []);

  const fetchMyScores = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/scores/my');
      
      // Transform data for display
      const transformedTests = response.data.map(score => ({
        id: score.id,
        title: score.test_name,
        score: score.correct_answers,
        maxScore: score.total_questions,
        percentage: Math.round(score.score),
        date: score.submitted_at,
        duration: `${Math.round(score.time_taken)} min`,
        category: score.category
      }));
      
      setCompletedTests(transformedTests);
    } catch (error) {
      console.error('Error fetching scores:', error);
      toast.error('Failed to load completed tests');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (percentage) => {
    if (percentage >= 90) return 'text-green-600 bg-green-100 dark:bg-green-900/30';
    if (percentage >= 75) return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30';
    if (percentage >= 60) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30';
    return 'text-red-600 bg-red-100 dark:bg-red-900/30';
  };

  const averageScore = completedTests.length > 0
    ? Math.round(completedTests.reduce((sum, test) => sum + test.percentage, 0) / completedTests.length)
    : 0;

  const bestScore = completedTests.length > 0
    ? Math.max(...completedTests.map((t) => t.percentage))
    : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-green-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center space-x-3"
      >
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center">
          <CheckCircle className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Completed Tests</h1>
          <p className="text-gray-600 dark:text-gray-400">View your test history and scores</p>
        </div>
      </motion.div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-6"
        >
          <div className="flex items-center space-x-3 mb-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Tests</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{completedTests.length}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card p-6"
        >
          <div className="flex items-center space-x-3 mb-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Average Score</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{averageScore}%</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card p-6"
        >
          <div className="flex items-center space-x-3 mb-2">
            <Award className="w-5 h-5 text-yellow-600" />
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Best Score</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{bestScore}%</p>
        </motion.div>
      </div>

      {/* Tests List */}
      {completedTests.length === 0 ? (
        <div className="text-center py-12">
          <CheckCircle className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No completed tests yet</p>
          <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">Take a test to see your results here</p>
        </div>
      ) : (
        <div className="space-y-4">
          {completedTests.map((test, index) => (
            <motion.div
              key={test.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 + index * 0.1 }}
              whileHover={{ y: -3 }}
              className="glass-card p-6 cursor-pointer hover:shadow-xl transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white">{test.title}</h3>
                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-600 dark:bg-blue-900/30">
                      {test.category}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(test.date).toLocaleDateString()}</span>
                    </div>
                    <span>Duration: {test.duration}</span>
                  </div>
                </div>

                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      {test.score}/{test.maxScore}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Points</p>
                  </div>
                  <div className={`px-4 py-2 rounded-xl font-bold text-lg ${getScoreColor(test.percentage)}`}>
                    {test.percentage}%
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CompletedTestsSection;

