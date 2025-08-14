import streamlit as st
import pandas as pd
import io
from database import Database
from student import Student
from chatbot import Chatbot
from credentials import Credentials
from user import User

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

@st.cache_resource
def init_components():
    db = Database()
    chatbot = Chatbot(db)
    credentials = Credentials()
    user_manager = User()
    return db, chatbot, credentials, user_manager

db, chatbot, credentials, user_manager = init_components()

def login_page():
    st.title("🎓 Student Database Management System")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        
        user_type = st.selectbox("Login as:", ["Admin", "User"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            if username and password:
                if user_type == "Admin":
                    if credentials.authenticate_credentials(username, password):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "Admin"
                        st.session_state.username = username
                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid admin credentials!")
                else:
                    if user_manager.authenticate_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "User"
                        st.session_state.username = username
                        st.success("User login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid user credentials!")
            else:
                st.error("Please enter both username and password!")
    
    with tab2:
        st.header("Register New User")
        
        new_username = st.text_input("Choose Username", key="reg_username")
        new_password = st.text_input("Choose Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", type="primary"):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    result = user_manager.store_users(new_username, new_password)
                    if result is not False:
                        st.success("Registration successful! You can now login.")
                        st.balloons()
                    else:
                        st.error("Username already exists. Please choose a different one.")
                else:
                    st.error("Passwords do not match!")
            else:
                st.error("Please fill in all fields!")

def admin_dashboard():
    st.title(f"👨‍💼 Admin Dashboard - Welcome {st.session_state.username}!")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Admin Menu")
        menu_option = st.selectbox(
            "Choose Action:",
            ["View Students", "Add Student", "Update Student", "Delete Student", "Bulk Upload", "Chatbot"]
        )
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if menu_option == "View Students":
        view_students()
    elif menu_option == "Add Student":
        add_student()
    elif menu_option == "Update Student":
        update_student()
    elif menu_option == "Delete Student":
        delete_student()
    elif menu_option == "Bulk Upload":
        bulk_upload()
    elif menu_option == "Chatbot":
        chatbot_interface()

def user_dashboard():
    st.title(f"👨‍🎓 User Dashboard - Welcome {st.session_state.username}!")
    st.markdown("---")
    
    with st.sidebar:
        st.header("User Menu")
        menu_option = st.selectbox(
            "Choose Action:",
            ["Chatbot", "View My Info"]
        )
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if menu_option == "Chatbot":
        chatbot_interface()
    elif menu_option == "View My Info":
        st.info("📊 Access student information through the chatbot!")
        st.markdown("""
        **Available chatbot commands:**
        - "list students" - View all students
        - "count students" - Get total number of students
        - "find student [name]" - Search for a specific student
        - "help" - Get list of available commands
        """)

def view_students():
    st.header("📋 All Students")
    
    students = db.fetch_students()
    
    if students:
        df = pd.DataFrame(students, columns=['ID', 'Name', 'Age', 'Grade'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", len(students))
        with col2:
            st.metric("Average Age", f"{df['Age'].mean():.1f}")
        with col3:
            unique_grades = df['Grade'].nunique()
            st.metric("Unique Grades", unique_grades)
        with col4:
            st.metric("Youngest Student", df['Age'].min())
        
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="students.csv",
            mime="text/csv"
        )
    else:
        st.info("No students found in the database.")

def add_student():
    st.header("➕ Add New Student")
    
    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=18)
        grade = st.text_input("Grade")
        
        submitted = st.form_submit_button("Add Student", type="primary")
        
        if submitted:
            if name and grade:
                student = Student(name=name, age=age, grade=grade)
                db.insert_student(student)
                st.success(f"✅ Student '{name}' added successfully!")
                st.balloons() # ahm haga
            else:
                st.error("Please fill in all required fields!")

def update_student():
    st.header("✏️ Update Student")
    
    students = db.fetch_students()
    
    if students:
        student_options = {f"{s[1]} (ID: {s[0]})": s[0] for s in students}
        selected_student = st.selectbox("Select Student to Update:", options=list(student_options.keys()))
        
        if selected_student:
            student_id = student_options[selected_student]
            current_student = db.fetch_student(student_id=student_id)[0]
            
            st.write(f"**Current Information:** ID: {current_student[0]}, Name: {current_student[1]}, Age: {current_student[2]}, Grade: {current_student[3]}")
            
            with st.form("update_student_form"):
                new_name = st.text_input("New Name", value=current_student[1])
                new_age = st.number_input("New Age", min_value=1, max_value=100, value=current_student[2])
                new_grade = st.text_input("New Grade", value=current_student[3])
                
                submitted = st.form_submit_button("Update Student", type="primary")
                
                if submitted:
                    db.delete_student(student_id)
                    updated_student = Student(name=new_name, age=new_age, grade=new_grade)
                    db.insert_student(updated_student)
                    st.success(f"✅ Student information updated successfully!")
                    st.rerun()
    else:
        st.info("No students available to update.")

def delete_student():
    st.header("🗑️ Delete Student")
    
    students = db.fetch_students()
    
    if students:
        student_options = {f"{s[1]} (ID: {s[0]})": s[0] for s in students}
        selected_student = st.selectbox("Select Student to Delete:", options=list(student_options.keys()))
        
        if selected_student:
            student_id = student_options[selected_student]
            current_student = db.fetch_student(student_id=student_id)[0]
            
            st.warning(f"⚠️ You are about to delete: **{current_student[1]}** (ID: {current_student[0]})")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Confirm Delete", type="primary"):
                    db.delete_student(student_id)
                    st.success(f"✅ Student '{current_student[1]}' deleted successfully!")
                    st.rerun()
            with col2:
                if st.button("❌ Cancel"):
                    st.info("Delete operation cancelled.")
    else:
        st.info("No students available to delete.")

def bulk_upload():
    st.header("📤 Bulk Upload Students")
    st.markdown("Upload a CSV file with columns: **Name**, **Age**, **Grade**")
    
    with st.expander("📋 View Sample CSV Format"):
        sample_data = pd.DataFrame({
            'Name': ['Ahmed Ali', 'Sara Mohamed', 'Omar Hassan'],
            'Age': [20, 19, 21],
            'Grade': ['A', 'B+', 'A-']
        })
        st.dataframe(sample_data)
        
        sample_csv = sample_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=sample_csv,
            file_name="sample_students.csv",
            mime="text/csv"
        )
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            required_columns = ['Name', 'Age', 'Grade']
            if all(col in df.columns for col in required_columns):
                st.write("📋 Preview of uploaded data:")
                st.dataframe(df)
                
                if st.button("🚀 Upload All Students", type="primary"):
                    success_count = 0
                    error_count = 0
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for index, row in df.iterrows():
                        try:
                            student = Student(name=row['Name'], age=int(row['Age']), grade=row['Grade'])
                            db.insert_student(student)
                            success_count += 1
                        except Exception as e:
                            error_count += 1
                            st.error(f"Error adding {row['Name']}: {str(e)}")
                        
                        progress = (index + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Processing: {index + 1}/{len(df)}")
                    
                    st.success(f"✅ Bulk upload completed! Added: {success_count}, Errors: {error_count}")
                    if success_count > 0:
                        st.balloons()
            else:
                st.error(f"❌ CSV must contain columns: {', '.join(required_columns)}")
                st.write("Your CSV columns:", list(df.columns))
                
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")

def chatbot_interface():
    st.header("🤖 Student Information Chatbot")
    st.markdown("Ask me about student information! Try commands like 'list students', 'count students', or 'find student [name]'")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["user"])
            with st.chat_message("assistant"):
                st.write(chat["bot"])
    
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        bot_response = chatbot.respond(user_input)
        
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": bot_response
        })
        
        st.rerun()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    with st.expander("❓ Available Commands"):
        st.markdown("""
        - **"list students"** - Display all students in the database
        - **"count students"** - Show total number of students
        - **"find student [name]"** - Search for a specific student by name
        - **"help"** - Show available commands
        
        **Example queries:**
        - "list students"
        - "how many students are there?"
        - "find student Ahmed"
        """)

def main():
    st.set_page_config(
        page_title="Student Database Management System",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_type == "Admin":
            admin_dashboard()
        else:
            user_dashboard()

if __name__ == "__main__":
    main()