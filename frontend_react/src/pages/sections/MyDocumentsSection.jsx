import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, Trash2, Eye, Calendar, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { API_BASE_URL } from '../../config/api';

const MyDocumentsSection = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalDocuments: 0,
    totalSize: '0 MB',
    pdfFiles: 0,
    otherFiles: 0
  });

  // Fetch documents on mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      const response = await fetch(`${API_BASE_URL}/api/documents/all`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to fetch documents');

      const data = await response.json();
      setDocuments(data);

      // Calculate stats
      const pdfCount = data.filter(d => d.file_type === 'pdf').length;
      setStats({
        totalDocuments: data.length,
        totalSize: formatTotalSize(data),
        pdfFiles: pdfCount,
        otherFiles: data.length - pdfCount
      });
    } catch (error) {
      console.error('Error fetching documents:', error);
      toast.error('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const formatTotalSize = (docs) => {
    const totalBytes = docs.reduce((sum, doc) => sum + (doc.file_size || 0), 0);
    if (totalBytes >= 1024 * 1024) {
      return `${(totalBytes / (1024 * 1024)).toFixed(1)} MB`;
    } else if (totalBytes >= 1024) {
      return `${(totalBytes / 1024).toFixed(1)} KB`;
    }
    return `${totalBytes} B`;
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return '0 B';
    if (bytes >= 1024 * 1024) {
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    } else if (bytes >= 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }
    return `${bytes} B`;
  };

  const handleDownload = async (doc) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/documents/${doc.id}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Download failed');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.doc_name;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success(`Downloaded ${doc.doc_name}`);
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download document');
    }
  };

  const handleDelete = async (doc) => {
    if (!confirm(`Are you sure you want to delete "${doc.doc_name}"?`)) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/documents/${doc.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Delete failed');

      toast.success(`Deleted ${doc.doc_name}`);
      fetchDocuments(); // Refresh the list
    } catch (error) {
      console.error('Delete error:', error);
      toast.error('Failed to delete document');
    }
  };

  const handleView = async (doc) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/documents/${doc.id}/content`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to load content');

      const data = await response.json();
      
      // Open content in a new modal or window
      const newWindow = window.open('', '_blank');
      newWindow.document.write(`
        <html>
          <head>
            <title>${doc.doc_name}</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
              h1 { color: #333; }
              pre { white-space: pre-wrap; word-wrap: break-word; }
            </style>
          </head>
          <body>
            <h1>${doc.doc_name}</h1>
            <p><strong>Pages:</strong> ${data.pages} | <strong>Words:</strong> ${data.word_count}</p>
            <hr>
            <pre>${data.content}</pre>
          </body>
        </html>
      `);
      newWindow.document.close();

      toast.success(`Opened ${doc.doc_name}`);
    } catch (error) {
      console.error('View error:', error);
      toast.error('Failed to view document');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );
  }

  const getFileIcon = (type) => {
    const colors = {
      PDF: 'text-red-600 bg-red-100 dark:bg-red-900/30',
      DOCX: 'text-blue-600 bg-blue-100 dark:bg-blue-900/30',
      TXT: 'text-gray-600 bg-gray-100 dark:bg-gray-900/30',
    };
    return colors[type] || colors.TXT;
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 flex items-center justify-center">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Documents</h1>
            <p className="text-gray-600 dark:text-gray-400">Manage your uploaded documents</p>
          </div>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-4"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Documents</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalDocuments}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card p-4"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Size</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalSize}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card p-4"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">PDF Files</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.pdfFiles}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card p-4"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Other Files</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.otherFiles}</p>
        </motion.div>
      </div>

      {/* Documents Grid */}
      {documents.length === 0 ? (
        <div className="text-center py-12">
          <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No documents uploaded yet</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {documents.map((doc, index) => (
            <motion.div
              key={doc.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              whileHover={{ y: -5 }}
              className="glass-card p-6 hover:shadow-xl transition-all"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-start space-x-3 flex-1">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${getFileIcon(doc.file_type?.toUpperCase() || 'TXT')}`}>
                    <FileText className="w-5 h-5" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1 break-words">
                      {doc.doc_name}
                    </h3>
                    <div className="flex items-center space-x-3 text-xs text-gray-600 dark:text-gray-400">
                      <span>{formatFileSize(doc.file_size)}</span>
                      <span>•</span>
                      <span>{doc.total_pages} pages</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                  <Calendar className="w-4 h-4" />
                  <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                </div>

                <div className="flex items-center space-x-2">
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleView(doc)}
                    className="p-2 rounded-lg hover:bg-blue-500/10 text-blue-600 transition-all"
                    title="View"
                  >
                    <Eye className="w-4 h-4" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleDownload(doc)}
                    className="p-2 rounded-lg hover:bg-green-500/10 text-green-600 transition-all"
                    title="Download"
                  >
                    <Download className="w-4 h-4" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleDelete(doc)}
                    className="p-2 rounded-lg hover:bg-red-500/10 text-red-600 transition-all"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4" />
                  </motion.button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyDocumentsSection;

