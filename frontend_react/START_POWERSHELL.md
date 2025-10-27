# 🚀 Start Frontend - PowerShell Commands

## ⚠️ Important for PowerShell Users

PowerShell uses **semicolon (`;`)** instead of `&&` to chain commands.

## 🎯 Quick Start (PowerShell)

### Option 1: Single Command
```powershell
cd frontend_react; npm run dev
```

### Option 2: Separate Commands
```powershell
cd frontend_react
npm run dev
```

### First Time Setup
```powershell
cd frontend_react
npm install
npm run dev
```

## 🌐 Access Application

Once running, open your browser to:
```
http://localhost:5173
```

## 🛑 Stop Server

Press `Ctrl + C` in the terminal

## 📦 Other Useful Commands

### Install Dependencies
```powershell
cd frontend_react; npm install
```

### Build for Production
```powershell
cd frontend_react; npm run build
```

### Preview Production Build
```powershell
cd frontend_react; npm run preview
```

### Lint Code
```powershell
cd frontend_react; npm run lint
```

## 🔧 Troubleshooting

### If Port 5173 is Busy
Vite will automatically use the next available port (5174, 5175, etc.)

### Clear Cache and Reinstall
```powershell
cd frontend_react
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Check Node Version
```powershell
node --version
npm --version
```

You need Node.js v14 or higher.

## ✅ You're All Set!

The frontend should now be running with the beautiful new glassmorphism design!

**Happy coding! 🎨**

