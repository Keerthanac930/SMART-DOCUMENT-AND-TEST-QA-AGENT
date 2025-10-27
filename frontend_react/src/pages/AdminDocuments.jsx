import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FileText, Upload, Trash2, Eye, Search, Download, RefreshCw } from 'lucide-react';
import Layout from '../components/Layout';
import api from '../config/api';
import toast from 'react-hot-toast';

const AdminDocuments = () => {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await api.get('/api/admin/documents');
      setDocuments(response.data);
    } catch (error) {
      toast.error('Failed to load documents');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error('Please select a file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await api.post('/api/admin/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success('Document uploaded successfully');
      setSelectedFile(null);
      fetchDocuments();
    } catch (error) {
      toast.error('Failed to upload document');
      console.error('Error:', error);
    } finally {
      setUploading(false);
    }
  };

  const deleteDocument = async (docId) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await api.delete(`/api/admin/documents/${docId}`);
      toast.success('Document deleted successfully');
      fetchDocuments();
    } catch (error) {
      toast.error('Failed to delete document');
      console.error('Error:', error);
    }
  };

  const processDocument = async (docId) => {
    try {
      await api.post(`/api/admin/documents/${docId}/process`);
      toast.success('Document processing started');
      fetchDocuments();
    } catch (error) {
      toast.error('Failed to process document');
    }
  };

  const filteredDocuments = documents.filter(
    (doc) =>
      doc.doc_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.file_type?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <Layout admin={true}>
        <div className="flex items-center justify-center h-96">
          <div className="loading-spinner" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout admin={true}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Document Management
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Upload and manage all documents in the system
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="glass-card p-3 flex items-center">
              <FileText className="w-5 h-5 text-gray-400 mr-2" />
              <span className="text-lg font-semibold text-gray-900 dark:text-white">
                {documents.length} Documents
              </span>
            </div>
          </div>
        </div>

        {/* Upload Section */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Upload New Document
          </h2>
          <div className="flex items-center space-x-4">
            <label className="btn-primary cursor-pointer flex items-center space-x-2">
              <Upload className="w-4 h-4" />
              <span>Choose File</span>
              <input
                type="file"
                onChange={handleFileSelect}
                className="hidden"
                accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
              />
            </label>
            {selectedFile && (
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {selectedFile.name}
              </span>
            )}
            {selectedFile && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleUpload}
                disabled={uploading}
                className="btn-primary flex items-center space-x-2"
              >
                {uploading ? (
                  <div className="loading-spinner" />
                ) : (
                  <Upload className="w-4 h-4" />
                )}
                <span>Upload</span>
              </motion.button>
            )}
          </div>
        </div>

        {/* Search Bar */}
        <div className="glass-card p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search documents by name or type..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="glass-input pl-10 w-full"
            />
          </div>
        </div>

        {/* Documents Table */}
        <div className="glass-card overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Pages
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Words
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredDocuments.map((doc) => (
                <tr
                  key={doc.id}
                  className="hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    #{doc.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <FileText className="w-5 h-5 text-gray-400 mr-2" />
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {doc.doc_name}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        doc.file_type === 'pdf'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          : doc.file_type === 'docx'
                          ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {doc.file_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                    {doc.total_pages || 0}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                    {doc.total_words || 0}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        doc.is_processed
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                      }`}
                    >
                      {doc.is_processed ? 'Processed' : 'Pending'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    {!doc.is_processed && (
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => processDocument(doc.id)}
                        className="text-blue-600 hover:text-blue-900 dark:hover:text-blue-300"
                        title="Process Document"
                      >
                        <RefreshCw className="w-4 h-4 inline" />
                      </motion.button>
                    )}
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => deleteDocument(doc.id)}
                      className="text-red-600 hover:text-red-900 dark:hover:text-red-300"
                      title="Delete Document"
                    >
                      <Trash2 className="w-4 h-4 inline" />
                    </motion.button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {filteredDocuments.length === 0 && (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">
                {searchTerm ? 'No documents found matching your search' : 'No documents uploaded yet'}
              </p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default AdminDocuments;

