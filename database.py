import sqlite3
from student import Student

class Database:
    def __init__(self, db_name = "students.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread = False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(""" 
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='students';
        """)
        table_exists = self.cursor.fetchone()

        if not table_exists:
            self._create_students_table()



    def _create_students_table(self):
        self.cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                grade TEXT
            )
        """)

        self.conn.commit()




    def insert_student(self, student):
        self.cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
            (student.name, student.age, student.grade))
        self.conn.commit()




    def fetch_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()
    


    
    def fetch_student(self, student_id = None, student_name = None):
        if student_id and student_name:
            self.cursor.execute("SELECT * FROM students WHERE id=? AND name=?", (student_id, student_name))
        elif student_id:
            self.cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        elif student_name:
            self.cursor.execute("SELECT * FROM students WHERE name=?", (student_name,))
        else:
            return []  

        return self.cursor.fetchall()
    


    
    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()






    