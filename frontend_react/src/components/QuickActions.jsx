import { motion } from 'framer-motion';
import { Brain, FileQuestion, Upload } from 'lucide-react';
import { useUI } from '../contexts/UIContext';

const QuickActions = () => {
  const { setActiveSection } = useUI();

  const actions = [
    {
      id: 'ask-ai',
      title: 'Ask AI',
      description: 'Get instant answers from our AI assistant',
      icon: Brain,
      gradient: 'from-primary to-blue-600',
      section: 'ask-ai',
    },
    {
      id: 'take-quiz',
      title: 'Take Quiz',
      description: 'Start a new quiz or continue where you left off',
      icon: FileQuestion,
      gradient: 'from-accent to-purple-600',
      section: 'available-tests',
    },
    {
      id: 'upload',
      title: 'Upload Document',
      description: 'Upload and analyze new documents',
      icon: Upload,
      gradient: 'from-green-500 to-emerald-600',
      section: 'upload-document',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {actions.map((action, index) => (
        <motion.button
          key={action.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 + index * 0.1 }}
          whileHover={{ y: -5, scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setActiveSection(action.section)}
          className="glass-card p-6 text-left group hover:shadow-2xl transition-all duration-300"
        >
          <div className="flex items-start space-x-4">
            <div
              className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.gradient} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300`}
            >
              <action.icon className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                {action.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {action.description}
              </p>
            </div>
          </div>
        </motion.button>
      ))}
    </div>
  );
};

export default QuickActions;

