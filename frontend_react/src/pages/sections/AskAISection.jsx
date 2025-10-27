import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Send, Mic, Image as ImageIcon, Sparkles, FileText } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../../config/api';

const AskAISection = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    {
      type: 'ai',
      content: 'Hi! I\'m your AI assistant. Ask me anything about your documents or learning materials!',
      time: new Date().toLocaleTimeString(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedDocs, setSelectedDocs] = useState([]);

  // Load user documents
  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await api.get('/api/user/documents');
      setDocuments(response.data);
    } catch (error) {
      console.error('Error loading documents:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    // Add user message
    const userMessage = {
      type: 'user',
      content: question,
      time: new Date().toLocaleTimeString(),
    };
    setMessages([...messages, userMessage]);
    setQuestion('');
    setIsLoading(true);

    try {
      // Make API call to Gemini with selected documents
      const response = await api.post('/api/ai/ask', {
        question: userMessage.content,
        document_ids: selectedDocs.length > 0 ? selectedDocs : null
      });
      
      const aiResponse = {
        type: 'ai',
        content: response.data.answer,
        time: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, aiResponse]);
    } catch (error) {
      console.error('Error asking AI:', error);
      const errorMsg = error.response?.data?.detail || 'Failed to get AI response. Please check if Gemini API is configured.';
      toast.error(errorMsg);
      
      // Add error message to chat
      const errorResponse = {
        type: 'ai',
        content: 'Sorry, I encountered an error. Please make sure the Gemini API is properly configured in the backend.',
        time: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Ask AI Assistant</h1>
            <p className="text-gray-600 dark:text-gray-400">Get instant answers from your documents</p>
          </div>
        </div>
      </motion.div>

      {/* Document Selector */}
      {documents.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-4"
        >
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            <FileText className="w-4 h-4 inline mr-2" />
            Search in Documents (optional)
          </label>
          <select
            multiple
            value={selectedDocs}
            onChange={(e) => setSelectedDocs(Array.from(e.target.selectedOptions, option => parseInt(option.value)))}
            className="glass-input h-24"
          >
            {documents.map((doc) => (
              <option key={doc.id} value={doc.id}>
                {doc.doc_name} ({doc.total_words} words)
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">Hold Ctrl/Cmd to select multiple documents</p>
        </motion.div>
      )}

      <div className="glass-card p-6 h-[600px] flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto mb-6 space-y-4">
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] p-4 rounded-2xl ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-primary to-accent text-white'
                    : 'bg-white/50 dark:bg-gray-700/50 backdrop-blur-lg'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className={`text-xs mt-2 ${message.type === 'user' ? 'text-white/70' : 'text-gray-500'}`}>
                  {message.time}
                </p>
              </div>
            </motion.div>
          ))}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-white/50 dark:bg-gray-700/50 backdrop-blur-lg p-4 rounded-2xl">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask me anything..."
              className="glass-input min-h-[100px] pr-24 resize-none"
              rows={3}
            />
            <div className="absolute right-3 bottom-3 flex space-x-2">
              <button
                type="button"
                className="p-2 rounded-lg hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all"
                title="Voice input"
              >
                <Mic className="w-5 h-5" />
              </button>
              <button
                type="button"
                className="p-2 rounded-lg hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all"
                title="Upload image"
              >
                <ImageIcon className="w-5 h-5" />
              </button>
            </div>
          </div>

          <motion.button
            type="submit"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={isLoading}
            className="btn-primary w-full flex items-center justify-center space-x-2"
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </motion.button>
        </form>
      </div>
    </div>
  );
};

export default AskAISection;

