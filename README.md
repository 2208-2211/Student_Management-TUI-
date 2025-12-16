# 🎓 Student Management System - TUI Application

A beautiful and feature-rich Terminal User Interface (TUI) application for managing student records with stunning colors, intuitive navigation, and persistent data storage.

## ✨ Features

### Core Functionality
- ➕ **Add Students** - Register new students with comprehensive details
- 👁️ **View All Students** - Display all records in a beautiful table format
- 🔍 **Search Students** - Find students by ID, name, or email
- ✏️ **Update Records** - Modify existing student information
- 🗑️ **Delete Students** - Remove records with confirmation prompts
- 📊 **Statistics Dashboard** - View analytics including total count, average age, and grade distribution

### Technical Features
- 🎨 **Beautiful UI** - Color-coded menus and panels using Rich library
- 💾 **Data Persistence** - JSON-based storage system
- ✅ **Input Validation** - Email, phone number, and age validation
- 🏗️ **Clean Architecture** - Modular design with separation of concerns
- 🔒 **Error Handling** - Graceful error management and user feedback
- 📱 **Responsive Design** - Works in any terminal size

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/student-management-tui.git
   cd student-management-tui
   ```

2. **Install dependencies**
   ```bash
   pip install rich
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

That's it! The application will start immediately.

## 📁 Project Structure

```
student-management-tui/
│
├── main.py                 # Main application file
├── students.json          # Database file (auto-generated)
├── README.md              # This file
├── LICENSE                # MIT License
└── requirements.txt       # Python dependencies
```

### Architecture Overview

The application follows a clean, modular architecture:

- **Models** - Student data model with serialization
- **Storage** - Database manager for JSON persistence
- **UI** - Menu system, forms, and display components
- **Validators** - Input validation utilities
- **Main App** - Application controller and business logic

## 💻 Usage

### Adding a Student
1. Select option `1` from the main menu
2. Enter student details:
   - Student ID (unique identifier)
   - Name
   - Age (5-100)
   - Grade/Class
   - Email (validated format)
   - Phone number (validated)
3. Student is automatically saved to the database

### Viewing Students
- Select option `2` to view all students in a formatted table
- Information displayed: ID, Name, Age, Grade, Email, Phone

### Searching
- Select option `3`
- Enter any part of: Student ID, Name, or Email
- Results display in a table format

### Updating Records
1. Select option `4`
2. Enter the Student ID to update
3. View current details
4. Enter new values (press Enter to keep current value)
5. Confirm changes

### Deleting Students
1. Select option `5`
2. Enter Student ID
3. Review student details
4. Type `YES` to confirm deletion

### Statistics
- Select option `6` to view:
  - Total student count
  - Average age
  - Grade distribution table

## 🎨 Color Scheme

The application uses a carefully designed color palette:
- **Cyan** - Prompts and labels
- **Green** - Success messages and confirmation
- **Yellow** - Warnings and important info
- **Red** - Errors and delete operations
- **Blue** - Headers and borders
- **Magenta** - Table headers and highlights

## 🔧 Configuration

### Changing the Database File
Edit the `Database` class initialization in `main.py`:
```python
self.db = Database('your_custom_name.json')
```

### Customizing Colors
Modify the color codes in the `UI` class methods. Available colors include:
- `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`
- `bright_red`, `bright_green`, etc.
- `bold`, `dim`, `underline`

## 📊 Data Storage

Student records are stored in JSON format (`students.json`):

```json
{
  "S001": {
    "student_id": "S001",
    "name": "John Doe",
    "age": 20,
    "grade": "Grade 12",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "enrollment_date": "2024-12-16"
  }
}
```

## 🛡️ Input Validation

The application validates:
- **Email**: Must contain `@` and `.`
- **Phone**: Must contain only digits, spaces, and hyphens
- **Age**: Must be between 5 and 100
- **Student ID**: Must be unique
