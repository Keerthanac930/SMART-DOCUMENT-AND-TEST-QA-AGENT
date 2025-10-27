import { motion } from 'framer-motion';

const LoadingSpinner = ({ fullScreen = false, text = 'Loading...' }) => {
  const containerClass = fullScreen
    ? 'fixed inset-0 flex items-center justify-center bg-background-light dark:bg-background-dark z-50'
    : 'flex items-center justify-center p-8';

  return (
    <div className={containerClass}>
      <div className="text-center">
        <motion.div
          animate={{
            rotate: 360,
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="w-16 h-16 mx-auto mb-4"
        >
          <div className="w-full h-full rounded-full border-4 border-gray-200 dark:border-gray-700 border-t-primary"></div>
        </motion.div>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-gray-600 dark:text-gray-400 font-medium"
        >
          {text}
        </motion.p>
      </div>
    </div>
  );
};

export default LoadingSpinner;

