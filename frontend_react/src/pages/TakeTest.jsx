import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Clock, Send, AlertCircle } from 'lucide-react';
import Layout from '../components/Layout';
import ProctoringMonitor from '../components/ProctoringMonitor';
import api from '../config/api';
import toast from 'react-hot-toast';

const TakeTest = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const [test, setTest] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [resultId, setResultId] = useState(null);
  const [isTestBlocked, setIsTestBlocked] = useState(false);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    fetchTestData();
  }, [testId]);

  useEffect(() => {
    if (timeRemaining > 0 && !isTestBlocked) {
      const timer = setTimeout(() => setTimeRemaining(timeRemaining - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeRemaining === 0 && test) {
      toast.error('Time is up! Submitting test...');
      handleSubmit();
    }
  }, [timeRemaining, isTestBlocked]);

  const fetchTestData = async () => {
    try {
      const [testRes, questionsRes] = await Promise.all([
        api.get(`/api/tests/${testId}`),
        api.get(`/api/tests/${testId}/questions`),
      ]);

      setTest(testRes.data);
      setQuestions(questionsRes.data);
      setTimeRemaining(testRes.data.time_limit_minutes * 60);

      // Generate a temporary result ID for proctoring
      setResultId(Date.now());
    } catch (error) {
      console.error('Load error:', error);
      toast.error('Failed to load test');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleViolation = (violationCount) => {
    if (violationCount >= 10) {
      setIsTestBlocked(true);
      toast.error('Test has been blocked due to too many violations!');
      setTimeout(() => navigate('/dashboard'), 3000);
    }
  };

  const handleSubmit = async () => {
    if (isTestBlocked) {
      toast.error('Test submission blocked due to violations');
      return;
    }

    setSubmitting(true);

    try {
      const timeTakenMinutes = (Date.now() - startTime) / 60000;
      
      // Convert answers to object format for backend
      const answersObject = {};
      Object.entries(answers).forEach(([questionId, answer]) => {
        answersObject[questionId] = answer;
      });

      const response = await api.post('/api/tests/submit', {
        test_id: parseInt(testId),
        answers: answersObject,
        time_taken_minutes: timeTakenMinutes,
      });

      toast.success(`Test submitted! Score: ${response.data.correct}/${response.data.total} (${Math.round(response.data.score)}%)`);
      navigate('/dashboard');
    } catch (error) {
      console.error('Submit error:', error);
      toast.error('Failed to submit test');
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="loading-spinner" />
        </div>
      </Layout>
    );
  }

  const currentQ = questions[currentQuestion];

  return (
    <Layout>
      {resultId && (
        <ProctoringMonitor
          onViolation={handleViolation}
          maxViolations={10}
          resultId={resultId}
          testId={parseInt(testId)}
        />
      )}

      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                {test?.test_name}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {test?.topic} • {questions.length} Questions
              </p>
            </div>

            <div className="flex items-center space-x-4">
              <div
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                  timeRemaining < 300
                    ? 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200'
                    : 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200'
                }`}
              >
                <Clock className="w-5 h-5" />
                <span className="font-semibold">{formatTime(timeRemaining)}</span>
              </div>
            </div>
          </div>

          {isTestBlocked && (
            <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg flex items-center text-red-700 dark:text-red-300">
              <AlertCircle className="w-5 h-5 mr-2" />
              <span className="font-medium">
                Test blocked due to excessive proctoring violations
              </span>
            </div>
          )}
        </div>

        {/* Progress */}
        <div className="glass-card p-4">
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
            <span>
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span>
              {Object.keys(answers).length} / {questions.length} Answered
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-primary to-accent h-2 rounded-full transition-all duration-300"
              style={{
                width: `${((currentQuestion + 1) / questions.length) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* Question Card */}
        <motion.div
          key={currentQuestion}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          className="glass-card p-8"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            {currentQ?.question_text}
          </h2>

          <div className="space-y-3">
            {currentQ && ['A', 'B', 'C', 'D'].map((option) => (
              <motion.button
                key={option}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={() => handleAnswerSelect(currentQ.id, option)}
                disabled={isTestBlocked}
                className={`w-full p-4 rounded-lg text-left transition-all ${
                  answers[currentQ.id] === option
                    ? 'bg-primary text-white border-2 border-primary'
                    : 'bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-primary'
                } ${isTestBlocked ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <div className="flex items-center">
                  <span className="font-semibold mr-3">{option}.</span>
                  <span>{currentQ.options[option]}</span>
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
            disabled={currentQuestion === 0 || isTestBlocked}
            className="btn-secondary"
          >
            Previous
          </button>

          <div className="flex items-center space-x-3">
            {currentQuestion < questions.length - 1 ? (
              <button
                onClick={() =>
                  setCurrentQuestion(Math.min(questions.length - 1, currentQuestion + 1))
                }
                disabled={isTestBlocked}
                className="btn-primary"
              >
                Next
              </button>
            ) : (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSubmit}
                disabled={submitting || isTestBlocked}
                className="btn-primary flex items-center space-x-2"
              >
                {submitting ? (
                  <div className="loading-spinner" />
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    <span>Submit Test</span>
                  </>
                )}
              </motion.button>
            )}
          </div>
        </div>

        {/* Question Grid */}
        <div className="glass-card p-6">
          <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
            Question Navigator
          </h3>
          <div className="grid grid-cols-10 gap-2">
            {questions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => setCurrentQuestion(idx)}
                disabled={isTestBlocked}
                className={`aspect-square rounded-lg text-sm font-semibold transition-all ${
                  idx === currentQuestion
                    ? 'bg-primary text-white'
                    : answers[q.id]
                    ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200'
                    : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                } ${isTestBlocked ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {idx + 1}
              </button>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default TakeTest;

