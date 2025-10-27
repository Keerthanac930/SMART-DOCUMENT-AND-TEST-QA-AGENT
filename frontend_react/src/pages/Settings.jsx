import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { User, Bell, Shield, Palette, Save } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useTheme } from '../contexts/ThemeContext'

const Settings = () => {
  const { user } = useAuth()
  const { isDark, toggleTheme } = useTheme()
  const [settings, setSettings] = useState({
    notifications: true,
    emailUpdates: true,
    darkMode: isDark,
    language: 'en'
  })
  const [loading, setLoading] = useState(false)

  const handleSave = async () => {
    setLoading(true)
    // Save settings logic here
    setTimeout(() => {
      setLoading(false)
    }, 1000)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Settings
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Manage your account preferences and system settings
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6"
        >
          <div className="flex items-center mb-4">
            <User className="w-5 h-5 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Profile Information
            </h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Username
              </label>
              <input
                type="text"
                value={user?.username || ''}
                className="input-field"
                disabled
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>
              <input
                type="email"
                value={user?.email || ''}
                className="input-field"
                disabled
              />
            </div>
          </div>
        </motion.div>

        {/* Notification Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card p-6"
        >
          <div className="flex items-center mb-4">
            <Bell className="w-5 h-5 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Notifications
            </h2>
          </div>
          
          <div className="space-y-4">
            <label className="flex items-center justify-between">
              <span className="text-gray-700 dark:text-gray-300">Push Notifications</span>
              <input
                type="checkbox"
                checked={settings.notifications}
                onChange={(e) => setSettings({...settings, notifications: e.target.checked})}
                className="w-4 h-4 text-primary-600 rounded"
              />
            </label>
            
            <label className="flex items-center justify-between">
              <span className="text-gray-700 dark:text-gray-300">Email Updates</span>
              <input
                type="checkbox"
                checked={settings.emailUpdates}
                onChange={(e) => setSettings({...settings, emailUpdates: e.target.checked})}
                className="w-4 h-4 text-primary-600 rounded"
              />
            </label>
          </div>
        </motion.div>

        {/* Appearance Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card p-6"
        >
          <div className="flex items-center mb-4">
            <Palette className="w-5 h-5 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Appearance
            </h2>
          </div>
          
          <div className="space-y-4">
            <label className="flex items-center justify-between">
              <span className="text-gray-700 dark:text-gray-300">Dark Mode</span>
              <input
                type="checkbox"
                checked={isDark}
                onChange={toggleTheme}
                className="w-4 h-4 text-primary-600 rounded"
              />
            </label>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Language
              </label>
              <select
                value={settings.language}
                onChange={(e) => setSettings({...settings, language: e.target.value})}
                className="input-field"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>
          </div>
        </motion.div>

        {/* Security Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card p-6"
        >
          <div className="flex items-center mb-4">
            <Shield className="w-5 h-5 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Security
            </h2>
          </div>
          
          <div className="space-y-4">
            <button className="w-full btn-secondary">
              Change Password
            </button>
            
            <button className="w-full btn-secondary">
              Two-Factor Authentication
            </button>
            
            <button className="w-full btn-secondary">
              Privacy Settings
            </button>
          </div>
        </motion.div>
      </div>

      {/* Save Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="text-center"
      >
        <button
          onClick={handleSave}
          disabled={loading}
          className="btn-primary disabled:opacity-50"
        >
          {loading ? (
            <div className="flex items-center">
              <div className="loading-spinner mr-2"></div>
              Saving...
            </div>
          ) : (
            <div className="flex items-center">
              <Save className="w-4 h-4 mr-2" />
              Save Settings
            </div>
          )}
        </button>
      </motion.div>
    </div>
  )
}

export default Settings
