import { motion } from 'framer-motion';
import { useState, useRef } from 'react';
import { Upload, File, X, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../../config/api';
import { useAuth } from '../../contexts/AuthContext';

const UploadDocumentSection = () => {
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);
  const { user } = useAuth();

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    addFiles(droppedFiles);
  };

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    addFiles(selectedFiles);
  };

  const addFiles = (newFiles) => {
    const fileObjects = newFiles.map((file) => ({
      file,
      id: Math.random().toString(36),
      name: file.name,
      size: (file.size / 1024).toFixed(2) + ' KB',
      status: 'pending',
    }));
    setFiles([...files, ...fileObjects]);
  };

  const removeFile = (id) => {
    setFiles(files.filter((f) => f.id !== id));
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      toast.error('Please select files to upload');
      return;
    }

    setIsUploading(true);
    let uploadedCount = 0;

    try {
      // Upload files one by one
      for (let i = 0; i < files.length; i++) {
        const fileObj = files[i];
        
        // Skip already uploaded files
        if (fileObj.status === 'completed') continue;

        try {
          const formData = new FormData();
          formData.append('file', fileObj.file);

          // Use correct endpoint based on user role
          const endpoint = user?.role === 'admin' 
            ? '/api/admin/documents' 
            : '/api/user/documents';

          console.log('📤 Uploading to:', endpoint);
          console.log('📄 File:', fileObj.name);

          const response = await api.post(endpoint, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          console.log('✅ Upload success:', response.data);

          // Mark file as completed
          setFiles((prevFiles) =>
            prevFiles.map((f) =>
              f.id === fileObj.id ? { ...f, status: 'completed' } : f
            )
          );
          uploadedCount++;
        } catch (error) {
          console.error(`❌ Error uploading ${fileObj.name}:`, error);
          console.error('Error details:', error.response?.data || error.message);
          toast.error(`Failed to upload ${fileObj.name}: ${error.response?.data?.detail || error.message}`);
          setFiles((prevFiles) =>
            prevFiles.map((f) =>
              f.id === fileObj.id ? { ...f, status: 'error' } : f
            )
          );
        }
      }

      if (uploadedCount > 0) {
        toast.success(`${uploadedCount} document(s) uploaded successfully!`);
        // Trigger dashboard refresh by dispatching a custom event
        window.dispatchEvent(new Event('documents-updated'));
      } else {
        toast.info('No new documents to upload');
      }
    } catch (error) {
      toast.error('Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center space-x-3"
      >
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
          <Upload className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Upload Documents</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Upload documents for AI analysis and quiz generation
          </p>
        </div>
      </motion.div>

      {/* Drag and Drop Zone */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`glass-card p-12 text-center transition-all ${
          isDragging ? 'border-2 border-primary bg-primary/5' : ''
        }`}
      >
        <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Drag and drop files here
        </h3>
        <p className="text-gray-600 dark:text-gray-400 mb-4">or</p>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          accept=".pdf,.doc,.docx,.txt"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          className="btn-primary"
        >
          Browse Files
        </button>
        <p className="text-sm text-gray-500 mt-4">
          Supported formats: PDF, DOC, DOCX, TXT
        </p>
      </motion.div>

      {/* File List */}
      {files.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Selected Files ({files.length})
          </h3>
          <div className="space-y-3 mb-6">
            {files.map((file) => (
              <motion.div
                key={file.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center justify-between p-4 rounded-xl bg-white/50 dark:bg-gray-700/50"
              >
                <div className="flex items-center space-x-3">
                  <File className="w-5 h-5 text-primary" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{file.name}</p>
                    <p className="text-sm text-gray-500">{file.size}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {file.status === 'completed' && (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  )}
                  <button
                    onClick={() => removeFile(file.id)}
                    className="p-2 rounded-lg hover:bg-red-500/10 text-red-500 transition-all"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleUpload}
            disabled={isUploading}
            className="btn-primary w-full"
          >
            {isUploading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="loading-spinner" />
                <span>Uploading...</span>
              </div>
            ) : (
              'Upload Documents'
            )}
          </motion.button>
        </motion.div>
      )}
    </div>
  );
};

export default UploadDocumentSection;

