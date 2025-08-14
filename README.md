# 🎓 Student Database Management System

A comprehensive web-based Student Database Management System built with Python and Streamlit, featuring user authentication, admin dashboard, chatbot interface, and secure credential management.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [User Guide](#user-guide)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Future Enhancements](#future-enhancements)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🌟 Project Overview

This Student Database Management System is designed to provide a secure, user-friendly platform for managing student records with the following capabilities:

- **Dual User System**: Separate interfaces for Administrators and regular Users
- **Secure Authentication**: SHA-256 password hashing and JSON-based credential storage
- **Interactive Chatbot**: AI-like chatbot interface for querying student information
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for student records
- **Bulk Operations**: CSV upload capability for adding multiple students at once
- **Modern UI**: Clean, responsive web interface built with Streamlit

## ✨ Features

### 🔐 Authentication System
- **Admin Login**: Secure admin access with predefined credentials
- **User Registration**: New user registration with automatic credential storage
- **Password Security**: SHA-256 hashing for secure password storage
- **Session Management**: Proper login/logout functionality with session state

### 👨‍💼 Admin Dashboard
- **Student Management**: Add, view, update, and delete student records
- **Bulk Upload**: CSV file upload for adding multiple students
- **Data Export**: Download student data as CSV files
- **Statistics Dashboard**: View student statistics and metrics
- **Chatbot Access**: Full access to chatbot functionality

### 👨‍🎓 User Dashboard
- **Chatbot Interface**: Interactive chat system for querying student data
- **Limited Access**: Secure, read-only access to student information
- **Help System**: Built-in command reference and assistance

### 🤖 Intelligent Chatbot
- **Natural Language Processing**: Understands various query formats
- **Student Queries**: Search, list, and count student records
- **Interactive Chat**: Modern chat interface with conversation history
- **Help Commands**: Built-in assistance and command reference

## 🏗️ System Architecture

The system follows Object-Oriented Programming (OOP) principles with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Streamlit)   │◄──►│   (Python OOP)  │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │  Login  │             │Student  │             │students │
    │Register │             │Database │             │  table  │
    │Dashboard│             │Chatbot  │             │         │
    │Chatbot  │             │User     │             │         │
    └─────────┘             │Creds    │             │         │
                            └─────────┘             └─────────┘
```

## 🔧 Prerequisites

Before running the application, ensure you have:

- **Python 3.7+** installed on your system
- **pip** (Python package installer)
- **Git** (optional, for cloning the repository)
- **Web browser** (Chrome, Firefox, Safari, etc.)

## 🚀 Installation & Setup

### Step 1: Download the Project

**Option A: Download ZIP**
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the project directory

**Option B: Clone Repository (if available)**
```bash
git clone <repository-url>
cd student-database-management
```

### Step 2: Set Up Python Environment (Recommended)

Create a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv student_db_env

# Activate virtual environment
# On Windows:
student_db_env\Scripts\activate

# On macOS/Linux:
source student_db_env/bin/activate
```

### Step 3: Install Dependencies

Install all required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

**If requirements.txt is not available, install manually:**
```bash
pip install streamlit pandas hashlib sqlite3
```

### Step 4: Initialize Project Files

Ensure all project files are in the correct directory:

```
student_management_system/
├── app.py
├── student.py
├── database.py
├── chatbot.py
├── credentials.py
├── user.py
├── credentials.json (will be created automatically)
├── users.json (will be created automatically)
├── requirements.txt
└── README.md
```

### Step 5: Set Up Admin Credentials

Create initial admin credentials by running:

```python
python -c "
from credentials import Credentials
creds = Credentials()
creds.store_credentials('admin', 'admin123')
print('Admin credentials created successfully!')
"
```

## 🎯 Running the Application

### Start the Application

1. **Navigate to project directory:**
   ```bash
   cd path/to/student_management_system
   ```

2. **Activate virtual environment (if using):**
   ```bash
   # Windows
   student_db_env\Scripts\activate
   
   # macOS/Linux
   source student_db_env/bin/activate
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   - The application will automatically open in your default web browser
   - If not, navigate to: `http://localhost:8501`

### Default Login Credentials

**Admin Access:**
- Username: `admin`
- Password: `admin123`

**User Access:**
- Register a new account using the "Register" tab on the login page

## 📖 User Guide

### For Administrators

1. **Login**: Use admin credentials to access the admin dashboard
2. **View Students**: See all student records with statistics
3. **Add Student**: Add individual student records using the form
4. **Update Student**: Modify existing student information
5. **Delete Student**: Remove student records with confirmation
6. **Bulk Upload**: Upload CSV files to add multiple students
7. **Chatbot**: Access the intelligent chatbot for queries

### For Regular Users

1. **Register**: Create a new account on the registration page
2. **Login**: Use your credentials to access the user dashboard
3. **Chatbot**: Interact with the chatbot to query student information
4. **Commands**: Use natural language or specific commands like:
   - "list students"
   - "count students" 
   - "find student [name]"
   - "help"

### Chatbot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list students` | Display all students | "list students" |
| `count students` | Show total number | "how many students?" |
| `find student [name]` | Search by name | "find student Ahmed" |
| `help` | Show available commands | "help" |

## 📁 Project Structure

```
student_management_system/
│
├── app.py                 # Main Streamlit application
├── student.py            # Student class (data model)
├── database.py           # Database operations class
├── chatbot.py            # Chatbot logic class
├── credentials.py        # Admin credentials management
├── user.py               # User credentials management
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
│
├── credentials.json     # Admin credentials (auto-generated)
├── users.json          # User credentials (auto-generated)
├── students.db         # SQLite database (auto-generated)
│
└── sample_data/        # Sample CSV files (optional)
    └── sample_students.csv
```

## 🔧 Technical Details

### Database Schema

**Students Table:**
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
);
```

### Security Features

- **Password Hashing**: SHA-256 encryption for all passwords
- **Session Management**: Secure login/logout with session state
- **Input Validation**: Comprehensive form validation and error handling
- **Access Control**: Role-based access (Admin vs User)

### File Formats

**CSV Upload Format:**
```csv
Name,Age,Grade
Ahmed Ali,20,A
Sara Mohamed,19,B+
Omar Hassan,21,A-
```

## 🚀 Future Enhancements

- **Advanced AI Integration**: Integration with LLM-powered chatbots
- **Database Migration**: Support for MySQL/PostgreSQL databases
- **Advanced Analytics**: Student performance analytics and reports
- **Multi-language Support**: Internationalization capabilities
- **API Integration**: REST API for external integrations
- **Mobile Responsive**: Enhanced mobile user experience

## 🔍 Troubleshooting

### Common Issues

**1. Import Errors:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.7+
```

**2. Port Already in Use:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

**3. Database Connection Issues:**
```bash
# Delete existing database and restart
rm students.db
streamlit run app.py
```

**4. Permission Errors:**
```bash
# Ensure proper file permissions
chmod 755 *.py
chmod 666 *.json
```

### Getting Help

If you encounter issues:

1. Check the error messages in the terminal
2. Ensure all files are in the correct directory
3. Verify Python and pip versions
4. Check that all dependencies are installed
5. Restart the application after making changes