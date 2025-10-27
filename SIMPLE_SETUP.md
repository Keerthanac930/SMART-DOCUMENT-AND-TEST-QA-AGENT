# 🚀 Simple Setup Guide - QA Agent

This guide will help you run the QA Agent project with minimal setup using SQLite database.

## 📋 Prerequisites

- **Python 3.10+** - Download from [python.org](https://python.org)
- **Node.js 18+** - Download from [nodejs.org](https://nodejs.org)

## 🎯 Quick Start (One Command)

### Windows Users:
```bash
# Double-click start_project.bat
# OR run in command prompt:
start_project.bat
```

### Linux/macOS Users:
```bash
# Make executable and run:
chmod +x start_project.sh
./start_project.sh
```

### Manual Start:
```bash
# Run the Python startup script:
python start_project.py
```

## 🔧 What the Script Does

The startup script will automatically:

1. ✅ **Check Prerequisites** - Verify Python and Node.js are installed
2. ✅ **Create Virtual Environment** - Set up Python virtual environment
3. ✅ **Install Dependencies** - Install all required packages
4. ✅ **Create Database** - Set up SQLite database with tables
5. ✅ **Create Sample Data** - Add test users and sample quiz
6. ✅ **Start Backend** - Launch FastAPI server on port 8000
7. ✅ **Start Frontend** - Launch React development server on port 3000

## 🌐 Access Points

After the script completes, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 👤 Test Accounts

The script creates sample accounts for testing:

- **Admin Account**: 
  - Username: `admin`
  - Password: `admin123`
  
- **User Account**: 
  - Username: `user`
  - Password: `user123`

## 🎯 Features Available

- ✅ **User Registration/Login** - Create accounts and authenticate
- ✅ **Document Upload** - Upload PDF, DOCX, TXT, and image files
- ✅ **AI Q&A** - Ask questions and get AI-powered answers
- ✅ **Quiz System** - Take quizzes and view results
- ✅ **Admin Panel** - Manage users, tests, and documents
- ✅ **Analytics** - View performance statistics and charts

## 🐛 Troubleshooting

### Common Issues:

1. **Python Not Found**:
   - Install Python 3.10+ from python.org
   - Make sure Python is added to PATH

2. **Node.js Not Found**:
   - Install Node.js 18+ from nodejs.org
   - Make sure Node.js is added to PATH

3. **Port Already in Use**:
   - Close other applications using ports 3000 or 8000
   - Or modify the ports in the configuration files

4. **Permission Errors**:
   - Run as administrator (Windows) or use sudo (Linux/macOS)
   - Make sure you have write permissions in the project directory

### Manual Setup (If Script Fails):

1. **Backend Setup**:
   ```bash
   cd backend_fastapi
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/macOS: source venv/bin/activate
   pip install -r requirements.txt
   python run_simple.py
   ```

2. **Frontend Setup** (in new terminal):
   ```bash
   cd frontend_react
   npm install
   npm run dev
   ```

## 📁 Project Structure

```
QA_Agent/
├── backend_fastapi/          # FastAPI Backend
├── frontend_react/           # React Frontend
├── start_project.py          # Main startup script
├── start_project.bat         # Windows batch file
├── start_project.sh          # Linux/macOS shell script
└── SIMPLE_SETUP.md          # This file
```

## 🎉 Success!

If everything works correctly, you should see:

1. **Backend Server** running on port 8000
2. **Frontend Server** running on port 3000
3. **Database** created with sample data
4. **Test Accounts** ready for use

## 🚀 Next Steps

1. **Open Browser** - Go to http://localhost:3000
2. **Login** - Use admin or user account
3. **Explore Features** - Try document upload, Q&A, and quizzes
4. **Customize** - Modify the application to your needs

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check the console output for error messages
4. Make sure ports 3000 and 8000 are available

---

**🎉 Enjoy using your QA Agent Dashboard!**
