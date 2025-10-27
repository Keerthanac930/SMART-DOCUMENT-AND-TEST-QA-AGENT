import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, Award, Clock, Target } from 'lucide-react'
import axios from 'axios'

const Analytics = () => {
  const [analytics, setAnalytics] = useState({
    performance: [],
    timeSpent: [],
    topics: [],
    improvements: []
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get('/api/user/results')
      // Process data for charts
      setAnalytics({
        performance: response.data.map((result, index) => ({
          test: `Test ${index + 1}`,
          score: result.score
        })),
        timeSpent: response.data.map((result, index) => ({
          test: `Test ${index + 1}`,
          time: result.time_taken_minutes
        })),
        topics: [
          { name: 'Correct', value: response.data.reduce((sum, r) => sum + r.correct_answers, 0), color: '#10B981' },
          { name: 'Incorrect', value: response.data.reduce((sum, r) => sum + (r.total_questions - r.correct_answers), 0), color: '#EF4444' }
        ]
      })
    } catch (error) {
      console.error('Error fetching analytics:', error)
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

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Performance Analytics
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track your learning progress and identify areas for improvement
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Test Performance
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analytics.performance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="test" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="score" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Answer Distribution
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analytics.topics}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {analytics.topics.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card p-6"
      >
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Learning Insights
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
            <TrendingUp className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-blue-600">85%</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Average Score</p>
          </div>
          <div className="text-center p-4 bg-green-50 dark:bg-green-900 rounded-lg">
            <Award className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-green-600">12</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Tests Completed</p>
          </div>
          <div className="text-center p-4 bg-purple-50 dark:bg-purple-900 rounded-lg">
            <Clock className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-purple-600">45m</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Avg Time</p>
          </div>
          <div className="text-center p-4 bg-orange-50 dark:bg-orange-900 rounded-lg">
            <Target className="w-8 h-8 text-orange-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-orange-600">3</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Areas to Improve</p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Analytics
