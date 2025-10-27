import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, Camera, Brain, Plus } from 'lucide-react'

const FloatingButtons = () => {
  const [isOpen, setIsOpen] = useState(false)

  const buttons = [
    {
      icon: Mic,
      label: 'Voice Input',
      color: 'bg-green-500 hover:bg-green-600',
      action: () => {
        console.log('Voice input activated')
        // Implement voice input functionality
      }
    },
    {
      icon: Camera,
      label: 'Image Scanner',
      color: 'bg-blue-500 hover:bg-blue-600',
      action: () => {
        console.log('Image scanner activated')
        // Implement image scanner functionality
      }
    },
    {
      icon: Brain,
      label: 'Quick Quiz',
      color: 'bg-purple-500 hover:bg-purple-600',
      action: () => {
        console.log('Quick quiz activated')
        // Navigate to quiz page
      }
    }
  ]

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Floating Action Button */}
      <AnimatePresence>
        {isOpen && (
          <div className="absolute bottom-16 right-0 space-y-3">
            {buttons.map((button, index) => {
              const Icon = button.icon
              return (
                <motion.button
                  key={button.label}
                  initial={{ opacity: 0, scale: 0, x: 20 }}
                  animate={{ opacity: 1, scale: 1, x: 0 }}
                  exit={{ opacity: 0, scale: 0, x: 20 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={button.action}
                  className={`${button.color} text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center space-x-3 group`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">
                    {button.label}
                  </span>
                </motion.button>
              )
            })}
          </div>
        )}
      </AnimatePresence>

      {/* Main FAB */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-primary-600 hover:bg-primary-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <motion.div
          animate={{ rotate: isOpen ? 45 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <Plus className="w-6 h-6" />
        </motion.div>
      </motion.button>
    </div>
  )
}

export default FloatingButtons
