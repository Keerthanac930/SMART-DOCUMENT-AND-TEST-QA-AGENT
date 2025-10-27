# 🚀 Quick Start Guide - QA Agent Frontend

## Prerequisites

- Node.js (v14 or higher) installed
- Backend FastAPI server running on `http://localhost:8000`

## 🎯 Step 1: Install Dependencies

Open PowerShell/Terminal in the `frontend_react` directory and run:

```powershell
npm install
```

This will install:
- React 18
- TailwindCSS 3
- Framer Motion
- React Router DOM
- React Hot Toast
- Lucide React Icons
- Axios
- And other dependencies

## 🎨 Step 2: Start Development Server

```powershell
npm run dev
```

The application will start at: **http://localhost:5173**

## 🌐 Step 3: Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should see the beautiful glassmorphism login page!

## 👥 Step 4: Create an Account or Login

### Option A: Sign Up
1. Click "Sign up" link
2. Enter username, email, password
3. Select account type (Student or Admin)
4. Click "Create Account"
5. You'll be redirected to login

### Option B: Login
1. Enter your username and password
2. Click "Sign In"
3. You'll be redirected to the dashboard

## 🎛️ Dashboard Navigation

Once logged in, you'll see a unified dashboard with:

### Sidebar Menu:
- 🏠 **Dashboard** - Overview with stats and quick actions
- 📚 **Tests**
  - Available Tests - Browse and start quizzes
  - Completed Tests - View your test history
- 📄 **Documents**
  - Upload Document - Add new learning materials
  - My Documents - Manage uploaded files
- 🤖 **Ask AI** - Chat with AI assistant
- ⚙️ **Settings** - Manage preferences

### Top Bar:
- 🌞/🌙 Theme toggle (switch between light/dark mode)
- 🔔 Notifications
- 👤 Profile menu

## 🎨 Features to Explore

### 1. Dashboard Home
- View your learning statistics
- Quick action cards for common tasks
- Recent activity feed

### 2. Ask AI
- Interactive chat interface
- Ask questions about your documents
- Get instant AI-powered answers

### 3. Upload Documents
- Drag and drop files
- Support for PDF, DOC, DOCX, TXT
- Track upload progress

### 4. Take Tests
- Browse available quizzes
- View difficulty levels and categories
- See estimated duration

### 5. View Results
- Check completed test scores
- Track your progress over time
- See performance statistics

### 6. Manage Documents
- View all uploaded files
- Download or delete documents
- See file details and upload dates

### 7. Settings
- Update profile information
- Toggle dark/light theme
- Manage notifications
- Change password (coming soon)

## 🎨 Design Features

### Glassmorphism UI
Beautiful translucent cards with:
- Backdrop blur effects
- Soft shadows
- Rounded corners
- Semi-transparent backgrounds

### Smooth Animations
Powered by Framer Motion:
- Fade in/out transitions
- Slide animations
- Scale effects on hover
- Page transitions

### Dark/Light Mode
- Toggle in top-right corner
- Persistent theme preference
- Smooth transitions between themes

### Responsive Design
- Works on desktop, tablet, and mobile
- Collapsible sidebar on mobile
- Adaptive layouts

## 🔧 Build Commands

### Development
```powershell
npm run dev
```

### Production Build
```powershell
npm run build
```

### Preview Production Build
```powershell
npm run preview
```

### Lint Code
```powershell
npm run lint
```

## 🐛 Troubleshooting

### Port Already in Use
If port 5173 is busy, Vite will automatically use the next available port (5174, 5175, etc.)

### Backend Connection Issues
Ensure the FastAPI backend is running on `http://localhost:8000`
Check `src/config/api.js` if you need to change the API URL.

### Dependencies Installation Failed
Try:
```powershell
rm -rf node_modules package-lock.json
npm install
```

### Dark Mode Not Working
- Check browser console for errors
- Clear browser cache
- Try toggling the theme switch again

## 🎯 Default Test Credentials (if backend has seed data)

Check with your backend team for test accounts, or create a new account using the signup page.

## 📱 Recommended Browsers

- Chrome (latest) ✅
- Firefox (latest) ✅
- Safari (latest) ✅
- Edge (latest) ✅

## 🌈 Color Palette

- **Primary Blue**: `#2563eb`
- **Accent Purple**: `#9333ea`
- **Background Light**: `#f9fafb`
- **Background Dark**: `#0f172a`
- **Text Light**: `#111827`
- **Text Dark**: `#f1f5f9`

## 🔗 Important Files

- `src/config/api.js` - API configuration
- `tailwind.config.js` - Theme customization
- `src/contexts/UIContext.jsx` - UI state management
- `src/contexts/AuthContext.jsx` - Authentication state

## 💡 Tips

1. **Dark Mode**: Click the sun/moon icon in the top-right
2. **Navigation**: Use the sidebar to switch between sections without page reloads
3. **Quick Actions**: Dashboard home has quick action cards for common tasks
4. **Animations**: Hover over cards and buttons to see smooth animations
5. **Mobile**: Sidebar collapses automatically on smaller screens

## 🎉 Enjoy Your Experience!

The QA Agent frontend is designed to be intuitive, beautiful, and responsive. Explore all the features and enjoy the smooth glassmorphism design!

---

**Need Help?** Check the main README.md or contact the development team.

