import React, { useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Send, 
  Mic, 
  MicOff, 
  Camera, 
  Image as ImageIcon,
  FileText,
  Volume2,
  VolumeX,
  Loader2
} from 'lucide-react'
import api from '../config/api'
import toast from 'react-hot-toast'

const AskAI = () => {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [selectedDocuments, setSelectedDocuments] = useState([])
  const [availableDocuments, setAvailableDocuments] = useState([])
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  
  const fileInputRef = useRef(null)
  const recognitionRef = useRef(null)
  const synthRef = useRef(null)

  React.useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = 'en-US'

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        setQuestion(transcript)
        setIsListening(false)
      }

      recognitionRef.current.onerror = () => {
        setIsListening(false)
        toast.error('Speech recognition failed')
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }

    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      synthRef.current = window.speechSynthesis
    }

    // Fetch available documents
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    try {
      const response = await api.get('/api/user/documents')
      setAvailableDocuments(response.data)
    } catch (error) {
      console.error('Error fetching documents:', error)
      // Silently fail if user isn't authenticated
      if (error.response?.status !== 401) {
        toast.error('Failed to load documents')
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setAnswer('')

    try {
      const response = await api.post('/api/ai/ask', {
        question: question.trim(),
        document_ids: selectedDocuments.length > 0 ? selectedDocuments : null
      })

      setAnswer(response.data.answer)
      toast.success('Answer generated successfully!')
    } catch (error) {
      console.error('Error asking question:', error)
      const errorMsg = error.response?.data?.detail || 'Failed to get answer. Please check if Gemini API is configured.'
      toast.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const startListening = () => {
    if (recognitionRef.current) {
      setIsListening(true)
      recognitionRef.current.start()
    } else {
      toast.error('Speech recognition not supported')
    }
  }

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
      setIsListening(false)
    }
  }

  const speakAnswer = () => {
    if (synthRef.current && answer) {
      if (isSpeaking) {
        synthRef.current.cancel()
        setIsSpeaking(false)
      } else {
        const utterance = new SpeechSynthesisUtterance(answer)
        utterance.onend = () => setIsSpeaking(false)
        utterance.onerror = () => setIsSpeaking(false)
        synthRef.current.speak(utterance)
        setIsSpeaking(true)
      }
    }
  }

  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImageFile(file)
      const reader = new FileReader()
      reader.onload = (e) => setImagePreview(e.target.result)
      reader.readAsDataURL(file)
      
      // Here you would implement OCR to extract text from image
      // For now, we'll just show a placeholder
      toast.info('Image uploaded. OCR processing would happen here.')
    }
  }

  const processImageWithOCR = async () => {
    if (!imageFile) return

    try {
      // This would integrate with Tesseract.js for OCR
      // For now, we'll show a placeholder
      toast.info('OCR processing would extract text from the image')
    } catch (error) {
      console.error('OCR processing failed:', error)
      toast.error('Failed to process image')
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Ask AI Assistant
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Get intelligent answers from your documents or general knowledge
        </p>
      </motion.div>

      {/* Document Selection */}
      {availableDocuments.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6"
        >
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Search in Documents (Optional)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {availableDocuments.map((doc) => (
              <label key={doc.id} className="flex items-center p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedDocuments.includes(doc.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedDocuments([...selectedDocuments, doc.id])
                    } else {
                      setSelectedDocuments(selectedDocuments.filter(id => id !== doc.id))
                    }
                  }}
                  className="mr-3"
                />
                <FileText className="w-4 h-4 mr-2 text-gray-500" />
                <span className="text-sm text-gray-700 dark:text-gray-300 truncate">
                  {doc.doc_name}
                </span>
              </label>
            ))}
          </div>
        </motion.div>
      )}

      {/* Image Upload */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card p-6"
      >
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Image Scanner (OCR)
        </h2>
        <div className="space-y-4">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
          />
          
          {!imagePreview ? (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-primary-500 transition-colors"
            >
              <div className="text-center">
                <Camera className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-600 dark:text-gray-400">Click to upload image</p>
              </div>
            </button>
          ) : (
            <div className="space-y-4">
              <img src={imagePreview} alt="Uploaded" className="max-w-full h-48 object-contain rounded-lg" />
              <div className="flex space-x-2">
                <button
                  onClick={processImageWithOCR}
                  className="btn-primary"
                >
                  Extract Text
                </button>
                <button
                  onClick={() => {
                    setImageFile(null)
                    setImagePreview(null)
                  }}
                  className="btn-secondary"
                >
                  Remove
                </button>
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Question Input */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card p-6"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask your question here..."
              className="w-full p-4 pr-20 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 resize-none"
              rows={4}
            />
            
            {/* Voice Input Button */}
            <button
              type="button"
              onClick={isListening ? stopListening : startListening}
              className={`absolute bottom-2 right-2 p-2 rounded-lg transition-colors ${
                isListening 
                  ? 'bg-red-500 hover:bg-red-600 text-white' 
                  : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300'
              }`}
            >
              {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>
          </div>

          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              {isListening && (
                <div className="flex items-center text-red-500">
                  <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse mr-2"></div>
                  Listening...
                </div>
              )}
            </div>
            
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center">
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </div>
              ) : (
                <div className="flex items-center">
                  <Send className="w-4 h-4 mr-2" />
                  Ask Question
                </div>
              )}
            </button>
          </div>
        </form>
      </motion.div>

      {/* Answer Display */}
      <AnimatePresence>
        {answer && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                AI Response
              </h2>
              <button
                onClick={speakAnswer}
                className={`p-2 rounded-lg transition-colors ${
                  isSpeaking 
                    ? 'bg-primary-600 text-white' 
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                }`}
              >
                {isSpeaking ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
              </button>
            </div>
            
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {answer}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default AskAI
