import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import os


class StudentSignInApp:
    def __init__(self, master):
        """Initialize the main application."""
        # Set up main window
        self.master = master
        master.title("AI and Robotics Club Sign-In")
        master.geometry("1920x1080")
        master.configure(bg='#005dab')

        # Initialize attributes
        self.status_label = None
        self.admins_button = None
        self.signin_button = None
        self.signup_button = None
        self.id_entry = None
        self.id_label = None
        self.title_label = None

        # Set up paths
        self.setup_paths()

        # Load valid users from CSV
        self.valid_users = self.load_valid_users_from_csv(self.csv_path)

        # Create GUI elements
        self.create_widgets()

    # ------------------------------
    # Setup Methods
    # ------------------------------

    def setup_paths(self):
        """Set up file paths and ensure required files/directories exist."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_path = os.path.join(base_dir, "members.csv")
        self.directory = os.path.join(base_dir, "daily_logs")

        # Ensure directories exist
        os.makedirs(self.directory, exist_ok=True)

        # Ensure members.csv exists
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w') as file:
                file.write("Student ID,First Name,Last Name,Email,Mobile\n")

    @staticmethod
    def load_valid_users_from_csv(file_path):
        """Load valid user data from the specified CSV file."""
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()  # Clean column names

            # Check required columns
            required_columns = {'Student ID', 'First Name', 'Last Name', 'Email', 'Mobile'}
            if not required_columns.issubset(set(df.columns)):
                raise KeyError(f"CSV must contain the columns: {required_columns}")

            # Convert to dictionary: {Student ID: (First Name, Last Name, Email, Mobile)}
            valid_users = {
                str(row['Student ID']): (row['First Name'], row['Last Name'], row['Email'], row['Mobile'])
                for _, row in df.iterrows()
            }
            return valid_users
        except FileNotFoundError:
            messagebox.showerror("Error", f"{file_path} file not found!")
            return {}
        except KeyError as e:
            messagebox.showerror("Error", str(e))
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
            return {}

    # ------------------------------
    # GUI Creation Methods
    # ------------------------------

    def create_widgets(self):
        """Create GUI widgets."""
        # Title Label
        self.title_label = tk.Label(
            self.master,
            text="AI and Robotics Club Sign-In",
            font=("Courier", 25, "bold"),
            bg='#005dab',
            fg='white',
        )
        self.title_label.pack(pady=(250, 10))

        # Student ID Entry
        self.id_label = tk.Label(self.master, text="Enter Student ID:")
        self.id_label.pack()

        self.id_entry = tk.Entry(self.master, font=("Courier", 18), justify='center')
        self.id_entry.pack(pady=(5, 10), padx=50)
        self.id_entry.bind('<Return>', self.sign_in)

        # Sign In Button
        self.signin_button = tk.Button(
            self.master,
            text="Sign In",
            command=self.sign_in,
            font=("Courier", 20, "bold"),
            bg='#005dab',
        )
        self.signin_button.pack(pady=10)

        # Admins Button
        self.admins_button = tk.Button(
            self.master,
            text="Admins",
            command=self.open_admin_login,
            font=("Courier", 10, "bold"),
            bg='#005dab',
        )
        self.admins_button.place(x=10, y=800)

        # Sign Up Frame
        signup_frame = tk.LabelFrame(
            self.master,
            text="Don't have an account?",
            font=("Courier", 18),
            padx=100,
            pady=15,
            bg='#A7C6D9',
            bd=10,
            fg='black',
            labelanchor='n',
        )
        signup_frame.pack(pady=20)

        # Sign Up Button
        self.signup_button = tk.Button(
            signup_frame,
            text="Sign Up",
            command=self.open_signup,
            font=("Courier", 12, "bold"),
            bg='red',
        )
        self.signup_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.master, text="", font=("Courier", 10))
        self.status_label.pack(pady=10)

    # ------------------------------
    # Sign-Up Methods
    # ------------------------------

    def open_signup(self):
        """Open Sign Up Window."""
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("700x400")
        signup_window.configure(bg='#001f3f')

        # Input fields
        tk.Label(signup_window, text="Enter First Name:", bg='#001f3f', fg='white').pack(pady=5)
        first_name_entry = tk.Entry(signup_window, font=("Courier", 12), justify='center')
        first_name_entry.pack(pady=5)

        tk.Label(signup_window, text="Enter Last Name:", bg='#001f3f', fg='white').pack(pady=5)
        last_name_entry = tk.Entry(signup_window, font=("Courier", 12), justify='center')
        last_name_entry.pack(pady=5)

        tk.Label(signup_window, text="Enter Student ID:", bg='#001f3f', fg='white').pack(pady=5)
        student_id_entry = tk.Entry(signup_window, font=("Courier", 12), justify='center')
        student_id_entry.pack(pady=5)

        tk.Label(signup_window, text="Enter Email:", bg='#001f3f', fg='white').pack(pady=5)
        email_entry = tk.Entry(signup_window, font=("Courier", 12), justify='center')
        email_entry.pack(pady=5)

        tk.Label(signup_window, text="Enter Mobile Phone Number:", bg='#001f3f', fg='white').pack(pady=5)
        mobile_entry = tk.Entry(signup_window, font=("Courier", 12), justify='center')
        mobile_entry.pack(pady=5)

        def add_user():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            student_id = student_id_entry.get().strip()
            email = email_entry.get().strip()
            mobile = mobile_entry.get().strip()

            # Validate inputs
            if not first_name or not last_name or not student_id or not email or not mobile:
                messagebox.showerror("Error", "All fields are required!")
                return

            if student_id in self.valid_users:
                messagebox.showerror("Error", "Student ID already exists!")
                return

            # Append to CSV and update in-memory data
            try:
                with open(self.csv_path, 'a') as file:
                    file.write(f"{student_id},{first_name},{last_name},{email},{mobile}\n")
                self.valid_users[student_id] = (first_name, last_name, email, mobile)
                messagebox.showinfo("Success", "User added successfully!")
                signup_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {e}")

        tk.Button(signup_window, text="Add User", command=add_user, bg='#4CAF50').pack(pady=10)

    # ------------------------------
    # Admin Methods
    # ------------------------------

    def open_admin_login(self):
        """Open admin login window."""
        admin_window = tk.Toplevel(self.master)
        admin_window.title("Admin Login")
        admin_window.geometry("300x150")
        admin_window.configure(bg='#001f3f')

        tk.Label(admin_window, text="Enter Admin Password:",).pack(pady=10)
        password_entry = tk.Entry(admin_window, show="*", font=("Courier", 12), justify='center')
        password_entry.pack(pady=5)

        def verify_password():
            if password_entry.get() == "123":
                self.open_admin_dashboard()
                admin_window.destroy()
            else:
                messagebox.showerror("Error", "Incorrect Password")

        tk.Button(admin_window, text="Submit", command=verify_password, bg='#4CAF50',).pack(pady=10)

    def open_admin_dashboard(self):
        """Open admin dashboard."""
        admin_dashboard = tk.Toplevel(self.master)
        admin_dashboard.title("Admin Dashboard")
        admin_dashboard.geometry("1000x600")
        admin_dashboard.configure(bg='#001f3f')

        # Admin Dashboard Label
        tk.Label(
            admin_dashboard,
            text="Admin Dashboard",
            font=("Courier", 20, "bold"),
            bg='#001f3f',
            fg='white',
        ).pack(pady=10)

        # Create a Notebook widget for tabs
        notebook = ttk.Notebook(admin_dashboard)
        notebook.pack(expand=True, fill='both', pady=10)

        # Tab 1: Members Table
        members_tab = ttk.Frame(notebook)
        notebook.add(members_tab, text="Members")

        # Tab 2: Daily Logs Table
        daily_logs_tab = ttk.Frame(notebook)
        notebook.add(daily_logs_tab, text="Daily Logs")

        # Members Table
        members_tree = ttk.Treeview(members_tab, columns=("Student ID", "First Name", "Last Name", "Email", "Mobile"), show="headings")
        members_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Define column headings for Members Table
        for col in ("Student ID", "First Name", "Last Name", "Email", "Mobile"):
            members_tree.heading(col, text=col)
            members_tree.column(col, width=150, anchor="center")

        # Load members data into the table
        try:
            with open(self.csv_path, 'r') as file:
                next(file)  # Skip the header row
                for line in file:
                    members_tree.insert("", "end", values=line.strip().split(","))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")

        # Daily Logs Table
        daily_logs_tree = ttk.Treeview(daily_logs_tab, columns=("Student ID", "First Name", "Last Name", "Email", "Mobile", "Timestamp"), show="headings")
        daily_logs_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Define column headings for Daily Logs Table
        for col in ("Student ID", "First Name", "Last Name", "Email", "Mobile", "Timestamp"):
            daily_logs_tree.heading(col, text=col)
            daily_logs_tree.column(col, width=150, anchor="center")

        # Dropdown to select a daily log file
        tk.Label(
            daily_logs_tab,
            text="Select a Daily Log File:",
            font=("Courier", 14),
            bg='#001f3f',
            fg='white'
        ).pack(pady=5)

        log_files = [f for f in os.listdir(self.directory) if f.endswith(".csv")]
        selected_log = tk.StringVar(daily_logs_tab)
        if log_files:
            selected_log.set(log_files[0])  # Set the first log file as default
        else:
            selected_log.set("No logs available")

        log_dropdown = ttk.Combobox(daily_logs_tab, textvariable=selected_log, values=log_files, state="readonly", font=("Courier", 12))
        log_dropdown.pack(pady=5)

        def load_selected_log():
            """Load the selected daily log file into the table."""
            daily_logs_tree.delete(*daily_logs_tree.get_children())  # Clear existing data
            log_file_name = selected_log.get()
            if log_file_name == "No logs available":
                messagebox.showinfo("Info", "No logs available to load.")
                return

            log_file_path = os.path.join(self.directory, log_file_name)
            try:
                with open(log_file_path, 'r') as file:
                    next(file)  # Skip the header row
                    for line in file:
                        daily_logs_tree.insert("", "end", values=line.strip().split(","))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load daily log: {e}")

        # Load Button
        tk.Button(
            daily_logs_tab,
            text="Load Log",
            command=load_selected_log,
            font=("Courier", 12),
            bg='#4CAF50',
        ).pack(pady=10)

        # Automatically load the first log file if available
        if log_files:
            load_selected_log()

    # ------------------------------
    # Sign-In Methods
    # ------------------------------
    def sign_in(self):
        """Handle sign-in process."""
        self.status_label.config(text="", fg='black')
        student_id = self.id_entry.get().strip()

        # Validate input
        if not student_id:
            self.status_label.config(text="Please enter a Student ID", fg='red')
            return

        if student_id not in self.valid_users:
            self.status_label.config(text="Please enter a valid STUDENT ID", fg='red')
            self.id_entry.delete(0, tk.END)
            return

        # Get user details
        first_name, last_name, email, mobile = self.valid_users[student_id]

        # Prepare log file path
        today = datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(self.directory, f"{today}.csv")

        try:
            # Check if the student has already signed in
            already_signed_in = False
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r') as log_file:
                    for line in log_file:
                        if line.startswith(student_id + ","):
                            already_signed_in = True
                            break

            if already_signed_in:
                # Student has already signed in
                self.status_label.config(text=f"{first_name} {last_name} has already signed in today.", fg='orange')
            else:
                # Log the sign-in
                with open(log_file_path, 'a') as log_file:
                    # Write the header if the file is new or empty
                    if os.stat(log_file_path).st_size == 0:
                        log_file.write("Student ID,First Name,Last Name,Email,Mobile,Timestamp\n")

                    # Write the log entry
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"{student_id},{first_name},{last_name},{email},{mobile},{timestamp}\n")

                # Update status label
                self.status_label.config(text=f"Welcome, {first_name} {last_name}!", fg='green')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to log sign-in: {e}")

        # Clear the input field
        self.id_entry.delete(0, tk.END)
        self.id_entry.focus_set()
        

# ------------------------------
# Main Function
# ------------------------------

def main():
    root = tk.Tk()
    StudentSignInApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()