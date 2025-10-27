# QA Agent - AI-Powered Learning Assistant

A modern, responsive web application for smart document analysis and interactive testing, built with React, TailwindCSS, and Framer Motion.

## 🎨 Design Features

- **Glassmorphism UI**: Beautiful translucent cards with backdrop blur effects
- **Smooth Animations**: Powered by Framer Motion for seamless transitions
- **Dark/Light Mode**: Toggle between themes with a single click
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern Color Palette**:
  - Primary: `#2563eb` (Blue)
  - Accent: `#9333ea` (Purple)
  - Background Light: `#f9fafb`
  - Background Dark: `#0f172a`

## 🚀 Quick Start

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
frontend_react/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── StatCard.jsx
│   │   ├── QuickActions.jsx
│   │   ├── AskAIModal.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ProtectedRoute.jsx
│   ├── contexts/            # React Context providers
│   │   ├── AuthContext.jsx  # Authentication state
│   │   └── UIContext.jsx    # UI state (theme, navigation)
│   ├── pages/               # Page components
│   │   ├── LoginPage.jsx
│   │   ├── SignupPage.jsx
│   │   ├── Dashboard.jsx
│   │   └── sections/        # Dashboard sections
│   │       ├── AskAISection.jsx
│   │       ├── UploadDocumentSection.jsx
│   │       ├── AvailableTestsSection.jsx
│   │       ├── CompletedTestsSection.jsx
│   │       ├── MyDocumentsSection.jsx
│   │       └── SettingsSection.jsx
│   ├── config/
│   │   └── api.js           # API configuration
│   ├── App.jsx              # Main app component with routing
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── tailwind.config.js       # TailwindCSS configuration
├── vite.config.js           # Vite configuration
└── package.json
```

## 🎯 Key Features

### Login/Signup Pages
- Beautiful glassmorphism design
- Animated background shapes
- Form validation
- Password visibility toggle
- Account type selection (Student/Admin)

### Unified Dashboard
- Collapsible sidebar with dropdown menus
- Quick action cards
- Real-time statistics
- Recent activity feed
- Smooth transitions between sections

### Dashboard Sections

1. **Dashboard Home**
   - Welcome message
   - Statistics cards (Available Tests, Completed Tests, Average Score, Documents)
   - Quick action buttons
   - Recent activity

2. **Ask AI**
   - Chat interface
   - Voice input support (placeholder)
   - Image upload support (placeholder)
   - Real-time responses

3. **Upload Documents**
   - Drag and drop interface
   - File preview
   - Upload progress
   - Supported formats: PDF, DOC, DOCX, TXT

4. **Available Tests**
   - Test cards with difficulty levels
   - Duration and question count
   - Category tags
   - Hover animations

5. **Completed Tests**
   - Test history
   - Score tracking
   - Performance statistics
   - Color-coded results

6. **My Documents**
   - Document grid
   - File management (View, Download, Delete)
   - Upload statistics
   - File type filtering

7. **Settings**
   - Profile settings
   - Theme toggle
   - Notification preferences
   - Security options

## 🎨 Design System

### Colors
```css
Primary: #2563eb (Blue)
Accent: #9333ea (Purple)
Success: #10b981 (Green)
Warning: #f59e0b (Orange)
Error: #ef4444 (Red)
```

### Typography
- Font Family: Inter, Poppins, Nunito Sans
- Heading: Bold, 24-48px
- Body: Regular, 14-16px
- Small: 12-14px

### Components
- **Glass Cards**: Semi-transparent with backdrop blur
- **Buttons**: Gradient backgrounds with hover effects
- **Inputs**: Glass effect with focus states
- **Animations**: Fade, slide, and scale transitions

## 🔧 Configuration

### API Configuration
Update `src/config/api.js` to point to your backend:

```javascript
const API_BASE_URL = 'http://localhost:8000';
export default API_BASE_URL;
```

### Theme Customization
Edit `tailwind.config.js` to customize colors, fonts, and animations.

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📄 License

This project is part of the QA Agent system.

## 🤝 Contributing

1. Follow the existing code style
2. Use meaningful component and variable names
3. Add comments for complex logic
4. Test on multiple screen sizes
5. Ensure dark mode compatibility

## 📞 Support

For issues or questions, please contact the development team.

