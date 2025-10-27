import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus, Trash2, Save, Sparkles, Loader2 } from 'lucide-react';
import Layout from '../components/Layout';
import api from '../config/api';
import toast from 'react-hot-toast';

const CreateTest = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [formData, setFormData] = useState({
    test_name: '',
    topic: '',
    description: '',
    time_limit_minutes: 20,
    questions: [
      {
        question_text: '',
        options: { A: '', B: '', C: '', D: '' },
        correct_answer: 'A',
        explanation: '',
        difficulty: 'medium',
      },
    ],
  });

  // Scroll to top on component mount
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleQuestionChange = (index, field, value) => {
    const updatedQuestions = [...formData.questions];
    updatedQuestions[index][field] = value;
    setFormData({ ...formData, questions: updatedQuestions });
  };

  const handleOptionChange = (qIndex, option, value) => {
    const updatedQuestions = [...formData.questions];
    updatedQuestions[qIndex].options[option] = value;
    setFormData({ ...formData, questions: updatedQuestions });
  };

  const addQuestion = () => {
    setFormData({
      ...formData,
      questions: [
        ...formData.questions,
        {
          question_text: '',
          options: { A: '', B: '', C: '', D: '' },
          correct_answer: 'A',
          explanation: '',
          difficulty: 'medium',
        },
      ],
    });
  };

  const removeQuestion = (index) => {
    const updatedQuestions = formData.questions.filter((_, i) => i !== index);
    setFormData({ ...formData, questions: updatedQuestions });
  };

  const handleGenerateWithAI = async () => {
    if (!formData.test_name || !formData.topic) {
      toast.error('Please enter test name and topic first');
      return;
    }

    setGenerating(true);

    try {
      const response = await api.post('/api/admin/tests/generate', null, {
        params: {
          test_name: formData.test_name,
          topic: formData.topic,
          num_questions: 25,
          difficulty: formData.questions[0]?.difficulty || 'medium',
          time_limit_minutes: formData.time_limit_minutes,
          description: formData.description || `AI-generated test on ${formData.topic}`
        }
      });

      toast.success(`✨ Test generated with ${response.data.num_questions} questions!`);
      navigate('/admin/dashboard');
    } catch (error) {
      console.error('Generation error:', error);
      toast.error('Failed to generate test with AI');
    } finally {
      setGenerating(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post('/api/admin/tests', formData);
      toast.success('Test created successfully!');
      navigate('/admin/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create test');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout admin={true}>
      <div className="w-full">
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-4"
        >
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
            Create New Test
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Design a comprehensive test for your students
          </p>
        </motion.div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Basic Info */}
          <div className="glass-card p-4 md:p-6 space-y-4">
            <h2 className="text-lg md:text-xl font-semibold text-gray-900 dark:text-white">
              Test Information
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Test Name
              </label>
              <input
                type="text"
                name="test_name"
                value={formData.test_name}
                onChange={handleInputChange}
                required
                autoFocus
                className="glass-input"
                placeholder="e.g., Mathematics Final Exam"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Topic/Category
                </label>
                <input
                  type="text"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  required
                  className="glass-input"
                  placeholder="e.g., Algebra"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Time Limit (minutes)
                </label>
                <input
                  type="number"
                  name="time_limit_minutes"
                  value={formData.time_limit_minutes}
                  onChange={handleInputChange}
                  required
                  min="1"
                  className="glass-input"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows="3"
                className="glass-input"
                placeholder="Brief description of the test..."
              />
            </div>

            {/* AI Generation Button */}
            <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
              <motion.button
                type="button"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleGenerateWithAI}
                disabled={generating || !formData.test_name || !formData.topic}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-lg font-medium flex items-center justify-center space-x-2 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {generating ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Generating with AI...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    <span>✨ Generate 25 Questions with AI (Gemini)</span>
                  </>
                )}
              </motion.button>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                Or manually add questions below
              </p>
            </div>
          </div>

          {/* Questions */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                Manual Questions ({formData.questions.length})
              </h2>
              <motion.button
                type="button"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={addQuestion}
                className="btn-primary flex items-center space-x-2"
              >
                <Plus className="w-4 h-4" />
                <span>Add Question</span>
              </motion.button>
            </div>

            {formData.questions.map((question, qIndex) => (
              <div key={qIndex} className="glass-card p-6 space-y-4">
                <div className="flex items-start justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Question {qIndex + 1}
                  </h3>
                  {formData.questions.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeQuestion(qIndex)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Question Text
                  </label>
                  <textarea
                    value={question.question_text}
                    onChange={(e) =>
                      handleQuestionChange(qIndex, 'question_text', e.target.value)
                    }
                    required
                    rows="2"
                    className="glass-input"
                    placeholder="Enter your question..."
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {['A', 'B', 'C', 'D'].map((option) => (
                    <div key={option}>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Option {option}
                      </label>
                      <input
                        type="text"
                        value={question.options[option]}
                        onChange={(e) =>
                          handleOptionChange(qIndex, option, e.target.value)
                        }
                        required
                        className="glass-input"
                        placeholder={`Option ${option}`}
                      />
                    </div>
                  ))}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Correct Answer
                    </label>
                    <select
                      value={question.correct_answer}
                      onChange={(e) =>
                        handleQuestionChange(qIndex, 'correct_answer', e.target.value)
                      }
                      className="glass-input"
                    >
                      <option value="A">A</option>
                      <option value="B">B</option>
                      <option value="C">C</option>
                      <option value="D">D</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Difficulty
                    </label>
                    <select
                      value={question.difficulty}
                      onChange={(e) =>
                        handleQuestionChange(qIndex, 'difficulty', e.target.value)
                      }
                      className="glass-input"
                    >
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Explanation
                  </label>
                  <textarea
                    value={question.explanation}
                    onChange={(e) =>
                      handleQuestionChange(qIndex, 'explanation', e.target.value)
                    }
                    rows="2"
                    className="glass-input"
                    placeholder="Explain why this answer is correct..."
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Submit Button */}
          <div className="flex items-center space-x-4">
            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <div className="loading-spinner" />
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  <span>Save Test</span>
                </>
              )}
            </motion.button>

            <button
              type="button"
              onClick={() => navigate('/admin/dashboard')}
              className="btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default CreateTest;

