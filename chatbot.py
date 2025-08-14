class Chatbot:
    def __init__(self, database):
        self.db = database

    def respond(self, query):
        query = query.strip().lower()

        if "list" in query and "students" in query:
            return self._list_students()

        elif "count" in query or "how many" in query:
            return self._count_students()

        elif "help" in query:
            return self._help()

        elif "find student" in query:
            name = self._extract_name(query)
            if name:
                return self._find_student_by_name(name)
            else:
                return "Please specify a student name. For example: 'Find student Ali'."

        else:
            return "Sorry, I didn't understand that. Type 'help' to see what I can do."

    def _list_students(self):
        students = self.db.fetch_students()
        if not students:
            return "No students found in the database."
        return "\n".join([f"ID: {s[0]}, Name: {s[1]}, Age: {s[2]}, Grade: {s[3]}" for s in students])

    def _count_students(self):
        students = self.db.fetch_students()
        return f"Total number of students: {len(students)}"

    def _find_student_by_name(self, name):
        matches = self.db.fetch_student(student_name=name)
        if matches:
            return "\n".join([f"Found: ID {s[0]}, Name: {s[1]}, Age: {s[2]}, Grade: {s[3]}" for s in matches])
        else:
            return f"No student found with the name '{name}'."

    def _extract_name(self, query):
        # crude way to extract name after "find student"
        if "find student" in query:
            parts = query.split("find student")
            return parts[1].strip().capitalize() if len(parts) > 1 else None
        return None

    def _help(self):
        return (
            "You can ask:\n"
            "- 'List students'\n"
            "- 'Count students'\n"
            "- 'Find student <name>'\n"
            "- 'Help'"
        )
