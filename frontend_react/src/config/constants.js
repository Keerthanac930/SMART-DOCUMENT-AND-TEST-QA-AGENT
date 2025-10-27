// Application constants

export const APP_NAME = 'QA Agent';
export const APP_VERSION = '1.0.0';
export const APP_DESCRIPTION = 'AI-Powered Learning Assistant';

// File upload constants
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const ALLOWED_FILE_TYPES = ['.pdf', '.doc', '.docx', '.txt'];

// Pagination
export const ITEMS_PER_PAGE = 10;

// Toast notification duration
export const TOAST_DURATION = 3000;

// Theme constants
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
};

// User roles
export const USER_ROLES = {
  STUDENT: 'student',
  ADMIN: 'admin',
};

// Test difficulty levels
export const DIFFICULTY_LEVELS = {
  EASY: 'Easy',
  MEDIUM: 'Medium',
  HARD: 'Hard',
};

// Color classes for difficulty levels
export const DIFFICULTY_COLORS = {
  Easy: 'text-green-600 bg-green-100 dark:bg-green-900/30',
  Medium: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30',
  Hard: 'text-red-600 bg-red-100 dark:bg-red-900/30',
};

// Color classes for score ranges
export const SCORE_COLORS = {
  EXCELLENT: 'text-green-600 bg-green-100 dark:bg-green-900/30', // 90-100
  GOOD: 'text-blue-600 bg-blue-100 dark:bg-blue-900/30', // 75-89
  AVERAGE: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30', // 60-74
  POOR: 'text-red-600 bg-red-100 dark:bg-red-900/30', // 0-59
};

export const getScoreColor = (percentage) => {
  if (percentage >= 90) return SCORE_COLORS.EXCELLENT;
  if (percentage >= 75) return SCORE_COLORS.GOOD;
  if (percentage >= 60) return SCORE_COLORS.AVERAGE;
  return SCORE_COLORS.POOR;
};

export const getDifficultyColor = (difficulty) => {
  return DIFFICULTY_COLORS[difficulty] || 'text-gray-600 bg-gray-100 dark:bg-gray-900/30';
};

