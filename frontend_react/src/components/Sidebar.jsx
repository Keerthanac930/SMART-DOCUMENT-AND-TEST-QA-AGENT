import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Home,
  FileText,
  CheckSquare,
  Brain,
  Settings,
  LogOut,
  ChevronDown,
  ChevronRight,
  Users,
  FilePlus,
  BarChart3,
  LayoutDashboard,
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useUI } from '../contexts/UIContext';

const Sidebar = ({ admin = false }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();
  // Only use UI context for student sidebar
  const uiContextValue = useUI();
  const activeSection = admin ? null : uiContextValue.activeSection;
  const setActiveSection = admin ? (() => {}) : uiContextValue.setActiveSection;
  const [sidebarCollapsed] = useState(false);
  const [expandedMenus, setExpandedMenus] = useState({
    tests: false,
    documents: false,
  });

  const toggleMenu = (menu) => {
    setExpandedMenus((prev) => ({
      ...prev,
      [menu]: !prev[menu],
    }));
  };

  const adminMenuItems = [
    { 
      id: 'admin-dashboard', 
      label: 'Dashboard', 
      icon: LayoutDashboard, 
      path: '/admin/dashboard'
    },
    { 
      id: 'create-test', 
      label: 'Create Test', 
      icon: FilePlus, 
      path: '/admin/create-test'
    },
    { 
      id: 'users', 
      label: 'Users', 
      icon: Users, 
      path: '/admin/users'
    },
    { 
      id: 'documents', 
      label: 'Documents', 
      icon: FileText, 
      path: '/admin/documents'
    },
    { 
      id: 'scores', 
      label: 'Scores', 
      icon: BarChart3, 
      path: '/admin/scores'
    },
  ];

  const studentMenuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home, section: 'dashboard' },
    {
      id: 'tests',
      label: 'Tests',
      icon: CheckSquare,
      hasSubmenu: true,
      submenu: [
        { id: 'available-tests', label: 'Available Tests', section: 'available-tests' },
        { id: 'completed-tests', label: 'Completed Tests', section: 'completed-tests' },
      ],
    },
    {
      id: 'documents',
      label: 'Documents',
      icon: FileText,
      hasSubmenu: true,
      submenu: [
        { id: 'upload-document', label: 'Upload Document', section: 'upload-document' },
        { id: 'my-documents', label: 'My Documents', section: 'my-documents' },
      ],
    },
    { id: 'ask-ai', label: 'Ask AI', icon: Brain, section: 'ask-ai' },
    { id: 'settings', label: 'Settings', icon: Settings, section: 'settings' },
  ];

  const menuItems = admin ? adminMenuItems : studentMenuItems;

  return (
    <motion.aside
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      className={`fixed left-0 top-0 h-screen ${
        sidebarCollapsed ? 'w-20' : 'w-64'
      } glass-card p-4 transition-all duration-300 z-50 lg:relative`}
    >
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="mb-8 px-2">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-3"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-xl">
              Q
            </div>
            {!sidebarCollapsed && (
              <span className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                QA Agent
              </span>
            )}
          </motion.div>
        </div>

        {/* Menu Items */}
        <nav className="flex-1 space-y-2">
          {menuItems.map((item) => (
            <div key={item.id}>
              {item.hasSubmenu ? (
                <>
                  <motion.button
                    whileHover={{ x: 4 }}
                    onClick={() => toggleMenu(item.id)}
                    className={`sidebar-item w-full justify-between ${
                      sidebarCollapsed ? 'justify-center' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <item.icon className="w-5 h-5" />
                      {!sidebarCollapsed && <span>{item.label}</span>}
                    </div>
                    {!sidebarCollapsed &&
                      (expandedMenus[item.id] ? (
                        <ChevronDown className="w-4 h-4" />
                      ) : (
                        <ChevronRight className="w-4 h-4" />
                      ))}
                  </motion.button>
                  {expandedMenus[item.id] && !sidebarCollapsed && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="ml-4 mt-2 space-y-1"
                    >
                      {item.submenu.map((subitem) => (
                        <motion.button
                          key={subitem.id}
                          whileHover={{ x: 4 }}
                          onClick={() => setActiveSection(subitem.section)}
                          className={`sidebar-item w-full text-sm ${
                            activeSection === subitem.section ? 'active' : ''
                          }`}
                        >
                          {subitem.label}
                        </motion.button>
                      ))}
                    </motion.div>
                  )}
                </>
              ) : item.path ? (
                <motion.button
                  whileHover={{ x: 4 }}
                  onClick={() => navigate(item.path)}
                  className={`sidebar-item w-full ${
                    location.pathname === item.path ? 'active' : ''
                  } ${sidebarCollapsed ? 'justify-center' : ''}`}
                >
                  <div className="flex items-center space-x-3">
                    <item.icon className="w-5 h-5" />
                    {!sidebarCollapsed && <span>{item.label}</span>}
                  </div>
                </motion.button>
              ) : (
                <motion.button
                  whileHover={{ x: 4 }}
                  onClick={() => setActiveSection(item.section)}
                  className={`sidebar-item w-full ${
                    activeSection === item.section ? 'active' : ''
                  } ${sidebarCollapsed ? 'justify-center' : ''}`}
                >
                  <div className="flex items-center space-x-3">
                    <item.icon className="w-5 h-5" />
                    {!sidebarCollapsed && <span>{item.label}</span>}
                  </div>
                </motion.button>
              )}
            </div>
          ))}
        </nav>

        {/* Logout */}
        <motion.button
          whileHover={{ x: 4 }}
          onClick={logout}
          className={`sidebar-item w-full text-red-600 dark:text-red-400 hover:bg-red-500/10 ${
            sidebarCollapsed ? 'justify-center' : ''
          }`}
        >
          <div className="flex items-center space-x-3">
            <LogOut className="w-5 h-5" />
            {!sidebarCollapsed && <span>Logout</span>}
          </div>
        </motion.button>
      </div>
    </motion.aside>
  );
};

export default Sidebar;
