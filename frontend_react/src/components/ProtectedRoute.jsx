import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LoadingSpinner from './LoadingSpinner';

const ProtectedRoute = ({ children, adminOnly = false, studentOnly = false }) => {
  const { isAuthenticated, isAdmin, loading, user } = useAuth();

  if (loading) {
    return <LoadingSpinner fullScreen text="Authenticating..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check if user is admin
  const userIsAdmin = isAdmin();

  // If admin tries to access student route, redirect to admin dashboard
  if (studentOnly && userIsAdmin) {
    return <Navigate to="/admin/dashboard" replace />;
  }

  // If student tries to access admin route, redirect to student dashboard
  if (adminOnly && !userIsAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children || <Outlet />;
};

export default ProtectedRoute;
