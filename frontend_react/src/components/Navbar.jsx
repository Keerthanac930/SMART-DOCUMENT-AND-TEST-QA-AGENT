import { motion } from 'framer-motion';
import { Bell, User, Sun, Moon, Menu } from 'lucide-react';
import { useUI } from '../contexts/UIContext';
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';

const Navbar = () => {
  const { theme, toggleTheme, toggleSidebar } = useUI();
  const { user, logout } = useAuth();
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass-card sticky top-0 z-40 px-6 py-4 mb-6"
    >
      <div className="flex items-center justify-between">
        {/* Left - Menu Toggle */}
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-xl hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all duration-200 lg:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Center - Search (optional, can be added later) */}
        <div className="flex-1"></div>

        {/* Right - Actions */}
        <div className="flex items-center space-x-4">
          {/* Theme Toggle */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleTheme}
            className="p-2 rounded-xl hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all duration-200"
          >
            {theme === 'light' ? (
              <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            ) : (
              <Sun className="w-5 h-5 text-yellow-500" />
            )}
          </motion.button>

          {/* Notifications */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="relative p-2 rounded-xl hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all duration-200"
          >
            <Bell className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </motion.button>

          {/* Profile Dropdown */}
          <div className="relative">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              className="flex items-center space-x-2 p-2 pr-4 rounded-xl hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all duration-200"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary to-accent flex items-center justify-center text-white font-semibold">
                {user?.username?.charAt(0).toUpperCase() || 'U'}
              </div>
              <span className="text-sm font-medium hidden md:block">
                {user?.username || 'User'}
              </span>
            </motion.button>

            {/* Dropdown Menu */}
            {showProfileMenu && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute right-0 mt-2 w-48 glass-card p-2 shadow-xl"
              >
                <button className="w-full text-left px-4 py-2 rounded-lg hover:bg-white/50 dark:hover:bg-gray-700/50 transition-all">
                  <div className="flex items-center space-x-2">
                    <User className="w-4 h-4" />
                    <span>View Profile</span>
                  </div>
                </button>
                <button
                  onClick={logout}
                  className="w-full text-left px-4 py-2 rounded-lg hover:bg-red-500/10 text-red-600 dark:text-red-400 transition-all"
                >
                  Logout
                </button>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;

