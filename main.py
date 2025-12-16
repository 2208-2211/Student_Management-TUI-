from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
import time
import json
import os
from datetime import datetime

console = Console()

class Student:
    def __init__(self, student_id, name, age, grade, email, phone):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email
        self.phone = phone
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'email': self.email,
            'phone': self.phone,
            'enrollment_date': self.enrollment_date
        }
    
    @staticmethod
    def from_dict(data):
        student = Student(
            data['student_id'],
            data['name'],
            data['age'],
            data['grade'],
            data['email'],
            data['phone']
        )
        student.enrollment_date = data.get('enrollment_date', datetime.now().strftime("%Y-%m-%d"))
        return student

# ============================================================================
# FILE: storage/database.py
# ============================================================================

class Database:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = {}
        self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.students = {k: Student.from_dict(v) for k, v in data.items()}
            except:
                self.students = {}
    
    def save(self):
        with open(self.filename, 'w') as f:
            data = {k: v.to_dict() for k, v in self.students.items()}
            json.dump(data, f, indent=2)
    
    def add_student(self, student):
        self.students[student.student_id] = student
        self.save()
    
    def get_student(self, student_id):
        return self.students.get(student_id)
    
    def update_student(self, student_id, student):
        if student_id in self.students:
            self.students[student_id] = student
            self.save()
            return True
        return False
    
    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            self.save()
            return True
        return False
    
    def get_all_students(self):
        return list(self.students.values())
    
    def search_students(self, query):
        results = []
        query = query.lower()
        for student in self.students.values():
            if (query in student.name.lower() or 
                query in student.student_id.lower() or
                query in student.email.lower()):
                results.append(student)
        return results

# ============================================================================
# FILE: utils/validators.py
# ============================================================================

class Validator:
    @staticmethod
    def validate_email(email):
        return '@' in email and '.' in email
    
    @staticmethod
    def validate_phone(phone):
        return phone.replace('-', '').replace(' ', '').isdigit()
    
    @staticmethod
    def validate_age(age):
        try:
            age_int = int(age)
            return 5 <= age_int <= 100
        except:
            return False
    
    @staticmethod
    def validate_grade(grade):
        return grade.strip() != ''

class UI:
    @staticmethod
    def show_header():
        console.clear()
        header = Text()
        header.append("╔═══════════════════════════════════════════════════════════╗\n", style="bold cyan")
        header.append("║     ", style="bold cyan")
        header.append("🎓 STUDENT MANAGEMENT SYSTEM 🎓", style="bold yellow")
        header.append("            ║\n", style="bold cyan")
        header.append("╚═══════════════════════════════════════════════════════════╝", style="bold cyan")
        console.print(Align.center(header))
        console.print()
    
    @staticmethod
    def show_menu():
        menu = Panel.fit(
            "[bold cyan]1.[/] [green]➕ Add Student[/]\n"
            "[bold cyan]2.[/] [blue]👁️  View All Students[/]\n"
            "[bold cyan]3.[/] [yellow]🔍 Search Student[/]\n"
            "[bold cyan]4.[/] [magenta]✏️  Update Student[/]\n"
            "[bold cyan]5.[/] [red]🗑️  Delete Student[/]\n"
            "[bold cyan]6.[/] [bright_black]📊 Statistics[/]\n"
            "[bold cyan]7.[/] [red bold]🚪 Exit[/]",
            title="[bold white]📋 MAIN MENU[/]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        console.print(Align.center(menu))
    
    @staticmethod
    def get_input(prompt, style="cyan"):
        return console.input(f"[{style}]{prompt}[/] ").strip()
    
    @staticmethod
    def show_success(message):
        console.print(f"\n[green]✓ {message}[/]")
        time.sleep(1.5)
    
    @staticmethod
    def show_error(message):
        console.print(f"\n[red]✗ {message}[/]")
        time.sleep(1.5)
    
    @staticmethod
    def show_info(message):
        console.print(f"\n[cyan]ℹ {message}[/]")
    
    @staticmethod
    def pause():
        console.input("\n[dim]Press Enter to continue...[/]")

class StudentManagementApp:
    def __init__(self):
        self.db = Database()
        self.validator = Validator()
        self.ui = UI()
    
    def run(self):
        while True:
            self.ui.show_header()
            self.ui.show_menu()
            choice = self.ui.get_input("\n🔹 Enter your choice (1-7): ", "bold yellow")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.exit_app()
                break
            else:
                self.ui.show_error("Invalid choice! Please enter 1-7.")
                time.sleep(1)
    
    def add_student(self):
        self.ui.show_header()
        console.print(Panel("[bold green]➕ ADD NEW STUDENT[/]", border_style="green"))
        console.print()
        
        student_id = self.ui.get_input("Student ID: ", "cyan")
        if self.db.get_student(student_id):
            self.ui.show_error("Student ID already exists!")
            self.ui.pause()
            return
        
        name = self.ui.get_input("Name: ", "cyan")
        
        age = self.ui.get_input("Age: ", "cyan")
        if not self.validator.validate_age(age):
            self.ui.show_error("Invalid age! Must be between 5 and 100.")
            self.ui.pause()
            return
        
        grade = self.ui.get_input("Grade/Class: ", "cyan")
        
        email = self.ui.get_input("Email: ", "cyan")
        if not self.validator.validate_email(email):
            self.ui.show_error("Invalid email format!")
            self.ui.pause()
            return
        
        phone = self.ui.get_input("Phone: ", "cyan")
        if not self.validator.validate_phone(phone):
            self.ui.show_error("Invalid phone number!")
            self.ui.pause()
            return
        
        student = Student(student_id, name, int(age), grade, email, phone)
        self.db.add_student(student)
        self.ui.show_success("Student added successfully!")
        self.ui.pause()
    
    def view_all_students(self):
        self.ui.show_header()
        students = self.db.get_all_students()
        
        if not students:
            self.ui.show_info("No students found in the database.")
            self.ui.pause()
            return
        
        console.print(Panel(f"[bold blue]👥 ALL STUDENTS ({len(students)} total)[/]", border_style="blue"))
        console.print()
        
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta", border_style="blue")
        table.add_column("ID", style="cyan", width=12)
        table.add_column("Name", style="green", width=20)
        table.add_column("Age", style="yellow", width=6)
        table.add_column("Grade", style="blue", width=10)
        table.add_column("Email", style="magenta", width=25)
        table.add_column("Phone", style="cyan", width=15)
        
        for student in students:
            table.add_row(
                student.student_id,
                student.name,
                str(student.age),
                student.grade,
                student.email,
                student.phone
            )
        
        console.print(table)
        self.ui.pause()
    
    def search_student(self):
        self.ui.show_header()
        console.print(Panel("[bold yellow]🔍 SEARCH STUDENT[/]", border_style="yellow"))
        console.print()
        
        query = self.ui.get_input("Enter student ID, name, or email: ", "cyan")
        results = self.db.search_students(query)
        
        if not results:
            self.ui.show_error("No students found matching your search.")
            self.ui.pause()
            return
        
        console.print(f"\n[green]Found {len(results)} student(s):[/]\n")
        
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta", border_style="yellow")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Age", style="yellow")
        table.add_column("Grade", style="blue")
        table.add_column("Email", style="magenta")
        table.add_column("Phone", style="cyan")
        
        for student in results:
            table.add_row(
                student.student_id,
                student.name,
                str(student.age),
                student.grade,
                student.email,
                student.phone
            )
        
        console.print(table)
        self.ui.pause()
    
    def update_student(self):
        self.ui.show_header()
        console.print(Panel("[bold magenta]✏️  UPDATE STUDENT[/]", border_style="magenta"))
        console.print()
        
        student_id = self.ui.get_input("Enter Student ID to update: ", "cyan")
        student = self.db.get_student(student_id)
        
        if not student:
            self.ui.show_error("Student not found!")
            self.ui.pause()
            return
        
        console.print(f"\n[green]Current details for {student.name}:[/]\n")
        console.print(f"[cyan]Name:[/] {student.name}")
        console.print(f"[cyan]Age:[/] {student.age}")
        console.print(f"[cyan]Grade:[/] {student.grade}")
        console.print(f"[cyan]Email:[/] {student.email}")
        console.print(f"[cyan]Phone:[/] {student.phone}\n")
        
        console.print("[dim]Leave blank to keep current value[/]\n")
        
        name = self.ui.get_input(f"New Name [{student.name}]: ", "cyan") or student.name
        age_input = self.ui.get_input(f"New Age [{student.age}]: ", "cyan")
        age = int(age_input) if age_input and self.validator.validate_age(age_input) else student.age
        grade = self.ui.get_input(f"New Grade [{student.grade}]: ", "cyan") or student.grade
        email = self.ui.get_input(f"New Email [{student.email}]: ", "cyan") or student.email
        phone = self.ui.get_input(f"New Phone [{student.phone}]: ", "cyan") or student.phone
        
        updated_student = Student(student_id, name, age, grade, email, phone)
        updated_student.enrollment_date = student.enrollment_date
        self.db.update_student(student_id, updated_student)
        
        self.ui.show_success("Student updated successfully!")
        self.ui.pause()
    
    def delete_student(self):
        self.ui.show_header()
        console.print(Panel("[bold red]🗑️  DELETE STUDENT[/]", border_style="red"))
        console.print()
        
        student_id = self.ui.get_input("Enter Student ID to delete: ", "cyan")
        student = self.db.get_student(student_id)
        
        if not student:
            self.ui.show_error("Student not found!")
            self.ui.pause()
            return
        
        console.print(f"\n[yellow]⚠️  You are about to delete:[/]")
        console.print(f"[cyan]Name:[/] {student.name}")
        console.print(f"[cyan]ID:[/] {student.student_id}\n")
        
        confirm = self.ui.get_input("Type 'YES' to confirm deletion: ", "red")
        
        if confirm.upper() == 'YES':
            self.db.delete_student(student_id)
            self.ui.show_success("Student deleted successfully!")
        else:
            self.ui.show_info("Deletion cancelled.")
        
        self.ui.pause()
    
    def show_statistics(self):
        self.ui.show_header()
        students = self.db.get_all_students()
        
        console.print(Panel("[bold white]📊 STATISTICS[/]", border_style="bright_blue"))
        console.print()
        
        if not students:
            self.ui.show_info("No students in database.")
            self.ui.pause()
            return
        
        total = len(students)
        avg_age = sum(s.age for s in students) / total
        
        grade_dist = {}
        for s in students:
            grade_dist[s.grade] = grade_dist.get(s.grade, 0) + 1
        
        console.print(f"[cyan]Total Students:[/] [bold green]{total}[/]")
        console.print(f"[cyan]Average Age:[/] [bold yellow]{avg_age:.1f}[/]")
        console.print(f"\n[cyan]Grade Distribution:[/]")
        
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
        table.add_column("Grade", style="cyan")
        table.add_column("Count", style="green")
        
        for grade, count in sorted(grade_dist.items()):
            table.add_row(grade, str(count))
        
        console.print(table)
        self.ui.pause()
    
    def exit_app(self):
        self.ui.show_header()
        console.print(Panel.fit(
            "[bold green]Thank you for using Student Management System![/]\n"
            "[cyan]Goodbye! 👋[/]",
            border_style="green"
        ))
        time.sleep(1)

if __name__ == "__main__":
    try:
        app = StudentManagementApp()
        app.run()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Program interrupted by user.[/]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/]")
