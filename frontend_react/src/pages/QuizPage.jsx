import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Clock, CheckCircle, XCircle, ArrowRight } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

const QuizPage = () => {
  const [availableTests, setAvailableTests] = useState([])
  const [selectedTest, setSelectedTest] = useState(null)
  const [questions, setQuestions] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState({})
  const [timeLeft, setTimeLeft] = useState(0)
  const [testStarted, setTestStarted] = useState(false)
  const [testCompleted, setTestCompleted] = useState(false)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAvailableTests()
  }, [])

  const fetchAvailableTests = async () => {
    try {
      const response = await axios.get('/api/user/tests')
      setAvailableTests(response.data)
    } catch (error) {
      console.error('Error fetching tests:', error)
      toast.error('Failed to load tests')
    } finally {
      setLoading(false)
    }
  }

  const startTest = async (testId) => {
    try {
      const response = await axios.get(`/api/user/tests/${testId}`)
      setSelectedTest(response.data)
      setQuestions(response.data.questions)
      setTimeLeft(response.data.time_limit_minutes * 60)
      setTestStarted(true)
      setTestCompleted(false)
      setAnswers({})
      setCurrentQuestion(0)
      
      // Start timer
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timer)
            submitTest()
            return 0
          }
          return prev - 1
        })
      }, 1000)
    } catch (error) {
      console.error('Error starting test:', error)
      toast.error('Failed to start test')
    }
  }

  const submitTest = async () => {
    if (!selectedTest) return

    try {
      const answersArray = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: parseInt(questionId),
        answer: answer
      }))

      const response = await axios.post(`/api/user/tests/${selectedTest.id}/submit`, {
        test_id: selectedTest.id,
        answers: answersArray,
        time_taken_minutes: (selectedTest.time_limit_minutes * 60 - timeLeft) / 60
      })

      setResults(response.data)
      setTestCompleted(true)
      toast.success('Test submitted successfully!')
    } catch (error) {
      console.error('Error submitting test:', error)
      toast.error('Failed to submit test')
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-spinner"></div>
      </div>
    )
  }

  if (testCompleted && results) {
    return (
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-8 text-center"
        >
          <div className="mb-6">
            {results.score >= 80 ? (
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            ) : (
              <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            )}
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Test Completed!
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {selectedTest?.test_name}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <p className="text-4xl font-bold text-primary-600 mb-2">
                {results.score.toFixed(1)}%
              </p>
              <p className="text-gray-600 dark:text-gray-400">Final Score</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-green-600 mb-2">
                {results.correct_answers}
              </p>
              <p className="text-gray-600 dark:text-gray-400">Correct Answers</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-600 mb-2">
                {results.time_taken_minutes.toFixed(1)}m
              </p>
              <p className="text-gray-600 dark:text-gray-400">Time Taken</p>
            </div>
          </div>

          <button
            onClick={() => {
              setTestCompleted(false)
              setResults(null)
              setSelectedTest(null)
              setTestStarted(false)
            }}
            className="btn-primary"
          >
            Take Another Test
          </button>
        </motion.div>
      </div>
    )
  }

  if (testStarted && selectedTest && questions.length > 0) {
    const currentQ = questions[currentQuestion]
    const progress = ((currentQuestion + 1) / questions.length) * 100

    return (
      <div className="max-w-4xl mx-auto">
        {/* Test Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-6 mb-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              {selectedTest.test_name}
            </h1>
            <div className="flex items-center text-red-600">
              <Clock className="w-5 h-5 mr-2" />
              <span className="text-lg font-semibold">
                {formatTime(timeLeft)}
              </span>
            </div>
          </div>
          
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Question {currentQuestion + 1} of {questions.length}
          </p>
        </motion.div>

        {/* Question */}
        <motion.div
          key={currentQuestion}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6 mb-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            {currentQ.question_text}
          </h2>

          <div className="space-y-3">
            {Object.entries(currentQ.options).map(([option, text]) => (
              <label
                key={option}
                className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  answers[currentQ.id] === option
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                <input
                  type="radio"
                  name={`question-${currentQ.id}`}
                  value={option}
                  checked={answers[currentQ.id] === option}
                  onChange={(e) => {
                    setAnswers({
                      ...answers,
                      [currentQ.id]: e.target.value
                    })
                  }}
                  className="sr-only"
                />
                <span className="font-semibold text-primary-600 mr-3">
                  {option}.
                </span>
                <span className="text-gray-700 dark:text-gray-300">
                  {text}
                </span>
              </label>
            ))}
          </div>
        </motion.div>

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
            disabled={currentQuestion === 0}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          <div className="flex space-x-2">
            {currentQuestion === questions.length - 1 ? (
              <button
                onClick={submitTest}
                className="btn-primary"
              >
                Submit Test
              </button>
            ) : (
              <button
                onClick={() => setCurrentQuestion(Math.min(questions.length - 1, currentQuestion + 1))}
                className="btn-primary"
              >
                Next
                <ArrowRight className="w-4 h-4 ml-2" />
              </button>
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Available Tests
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Choose a test to begin your quiz
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {availableTests.map((test, index) => (
          <motion.div
            key={test.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card p-6 hover:shadow-xl transition-shadow cursor-pointer"
            onClick={() => startTest(test.id)}
          >
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              {test.test_name}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              {test.description}
            </p>
            <div className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
              <p>Topic: {test.topic}</p>
              <p>Time Limit: {test.time_limit_minutes} minutes</p>
              <p>Questions: {test.questions?.length || 0}</p>
            </div>
            <button className="w-full mt-4 btn-primary">
              Start Test
            </button>
          </motion.div>
        ))}
      </div>

      {availableTests.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 dark:text-gray-400">
            No tests available at the moment.
          </p>
        </div>
      )}
    </div>
  )
}

export default QuizPage
