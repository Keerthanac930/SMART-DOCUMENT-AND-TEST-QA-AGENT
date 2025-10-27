import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  FileText, 
  TrendingUp, 
  Clock,
  Users,
  Award,
  Brain,
  Upload
} from 'lucide-react'
import api from '../config/api'
import toast from 'react-hot-toast'

const UserDashboard = () => {
  const [stats, setStats] = useState({
    totalTests: 0,
    completedTests: 0,
    averageScore: 0,
    totalDocuments: 0,
    recentResults: []
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch user stats and recent activity
      const [statsResponse, resultsResponse, documentsResponse] = await Promise.all([
        api.get('/api/user/stats'),
        api.get('/api/user/results'),
        api.get('/api/user/documents')
      ])

      const statsData = statsResponse.data
      const results = resultsResponse.data
      const documents = documentsResponse.data

      setStats({
        totalTests: statsData.total_tests || 0,
        completedTests: statsData.completed_tests || 0,
        averageScore: statsData.average_score || 0,
        totalDocuments: statsData.total_documents || 0,
        recentResults: results.slice(0, 5)
      })
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      // Don't show error if user isn't authenticated yet
      if (error.response?.status !== 401) {
        toast.error('Failed to load dashboard data')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-spinner"></div>
      </div>
    )
  }

  const statCards = [
    {
      title: 'Available Tests',
      value: stats.totalTests,
      icon: BookOpen,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100 dark:bg-blue-900'
    },
    {
      title: 'Completed Tests',
      value: stats.completedTests,
      icon: Award,
      color: 'text-green-600',
      bgColor: 'bg-green-100 dark:bg-green-900'
    },
    {
      title: 'Average Score',
      value: `${stats.averageScore.toFixed(1)}%`,
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100 dark:bg-purple-900'
    },
    {
      title: 'My Documents',
      value: stats.totalDocuments,
      icon: FileText,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100 dark:bg-orange-900'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-6 text-white"
      >
        <h1 className="text-2xl font-bold mb-2">Welcome back!</h1>
        <p className="text-primary-100">
          Ready to continue your learning journey? Explore tests, upload documents, or ask AI questions.
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="card p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    {stat.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stat.value}
                  </p>
                </div>
                <div className={`${stat.bgColor} p-3 rounded-lg`}>
                  <Icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card p-6"
      >
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900 transition-all duration-200">
            <Brain className="w-6 h-6 text-primary-600 mr-3" />
            <div className="text-left">
              <p className="font-medium text-gray-900 dark:text-white">Ask AI</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Get instant answers</p>
            </div>
          </button>
          
          <button className="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900 transition-all duration-200">
            <BookOpen className="w-6 h-6 text-primary-600 mr-3" />
            <div className="text-left">
              <p className="font-medium text-gray-900 dark:text-white">Take Quiz</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Test your knowledge</p>
            </div>
          </button>
          
          <button className="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900 transition-all duration-200">
            <Upload className="w-6 h-6 text-primary-600 mr-3" />
            <div className="text-left">
              <p className="font-medium text-gray-900 dark:text-white">Upload Document</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Add learning materials</p>
            </div>
          </button>
        </div>
      </motion.div>

      {/* Recent Results */}
      {stats.recentResults.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card p-6"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Recent Test Results
          </h2>
          <div className="space-y-3">
            {stats.recentResults.map((result, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 text-gray-500 mr-2" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {new Date(result.completed_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Score: {result.score.toFixed(1)}%
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    result.score >= 80 ? 'bg-green-100 text-green-800' :
                    result.score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {result.score >= 80 ? 'Excellent' :
                     result.score >= 60 ? 'Good' : 'Needs Improvement'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default UserDashboard
