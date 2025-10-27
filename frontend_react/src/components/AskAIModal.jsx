import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, Mic, Image as ImageIcon } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';

const AskAIModal = ({ isOpen, onClose }) => {
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    try {
      // API call will go here
      toast.success('Question sent to AI!');
      setQuestion('');
    } catch (error) {
      toast.error('Failed to send question');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
          >
            <div className="glass-card max-w-2xl w-full p-6 shadow-2xl">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                  Ask AI Assistant
                </h2>
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask me anything..."
                  className="glass-input min-h-[150px] resize-none"
                  rows={6}
                />

                {/* Action Buttons */}
                <div className="flex items-center justify-between">
                  <div className="flex space-x-2">
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

                  <motion.button
                    type="submit"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    disabled={isLoading}
                    className="btn-primary flex items-center space-x-2"
                  >
                    {isLoading ? (
                      <div className="loading-spinner" />
                    ) : (
                      <>
                        <Send className="w-4 h-4" />
                        <span>Send</span>
                      </>
                    )}
                  </motion.button>
                </div>
              </form>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default AskAIModal;

