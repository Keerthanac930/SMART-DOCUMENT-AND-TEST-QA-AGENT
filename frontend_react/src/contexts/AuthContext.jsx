import React, { createContext, useContext, useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import api from '../config/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))

  // Update token in localStorage
  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await api.get('/api/auth/me')
          setUser(response.data)
        } catch (error) {
          console.error('Auth check failed:', error)
          logout()
        }
      }
      setLoading(false)
    }

    checkAuth()
  }, [token])

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/auth/login', {
        email,
        password
      })

      const { access_token, role } = response.data
      setToken(access_token)

      // Get user profile
      const profileResponse = await api.get('/api/auth/me')
      const userData = profileResponse.data
      setUser(userData)

      toast.success('Login successful!')
      
      // Return role for route redirection
      return { success: true, role: userData.role }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      throw new Error(message)
    }
  }

  const register = async (userData, userType = 'student') => {
    try {
      const payload = {
        ...userData,
        role: userType === 'admin' ? 'admin' : 'student'
      }
      
      const response = await api.post('/api/auth/register', payload)

      const { access_token, role } = response.data
      setToken(access_token)

      // Get user profile
      const profileResponse = await api.get('/api/auth/me')
      setUser(profileResponse.data)

      toast.success('Registration successful!')
      return { success: true, role }
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed'
      throw new Error(message)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    toast.success('Logged out successfully!')
  }

  const isAdmin = () => {
    return user && user.role && user.role.toLowerCase() === 'admin'
  }

  const value = {
    user,
    login,
    register,
    logout,
    isAdmin,
    loading,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
