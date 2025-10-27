import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, X, CheckCircle } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

const DocumentUpload = () => {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState([])

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files)
    setFiles(selectedFiles)
  }

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index))
  }

  const uploadFiles = async () => {
    if (files.length === 0) return

    setUploading(true)
    const formData = new FormData()

    for (const file of files) {
      formData.append('file', file)
    }

    try {
      const response = await axios.post('/api/user/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setUploadedFiles([...uploadedFiles, response.data])
      setFiles([])
      toast.success('Files uploaded successfully!')
    } catch (error) {
      console.error('Upload error:', error)
      toast.error('Failed to upload files')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Upload Documents
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Upload PDF, DOCX, TXT, or image files for AI analysis
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card p-8"
      >
        <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Drop files here or click to browse
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Supports PDF, DOCX, TXT, and image files up to 200MB
          </p>
          <input
            type="file"
            multiple
            accept=".pdf,.docx,.doc,.txt,.png,.jpg,.jpeg"
            onChange={handleFileSelect}
            className="hidden"
            id="file-input"
          />
          <label
            htmlFor="file-input"
            className="btn-primary cursor-pointer"
          >
            Choose Files
          </label>
        </div>

        {files.length > 0 && (
          <div className="mt-6 space-y-3">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
              Selected Files
            </h4>
            {files.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center">
                  <FileText className="w-5 h-5 text-gray-500 mr-3" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {file.name}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="text-red-500 hover:text-red-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ))}
            
            <button
              onClick={uploadFiles}
              disabled={uploading}
              className="w-full btn-primary disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Upload Files'}
            </button>
          </div>
        )}
      </motion.div>

      {uploadedFiles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Uploaded Documents
          </h2>
          <div className="space-y-3">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900 rounded-lg">
                <div className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {file.doc_name}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Uploaded successfully
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default DocumentUpload
