from tkinter import messagebox
import customtkinter
from db_manager import setup_database, register_user, validate_user

# Function to show the login window
def show_login_window():
    login_window = customtkinter.CTkToplevel()
    login_window.geometry("400x300")
    login_window.title("Login")
    customtkinter.set_appearance_mode("Dark")

    # Center the login window on the screen
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    login_window.geometry(f"400x300+{x}+{y}")

    title_label = customtkinter.CTkLabel(login_window, text="Metflix Login", font=("Arial", 24))
    title_label.pack(pady=20)

    username_entry = customtkinter.CTkEntry(login_window, placeholder_text="Username")
    username_entry.pack(pady=10, padx=20)

    password_entry = customtkinter.CTkEntry(login_window, placeholder_text="Password", show="*")
    password_entry.pack(pady=10, padx=20)

    def validate_login():
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            if validate_user(username, password):
                messagebox.showinfo("Success", "Login successful!")
                login_window.destroy()
                # Proceed to the main application window
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    login_button = customtkinter.CTkButton(login_window, text="Login", command=validate_login)
    login_button.pack(pady=20)

    # Prevent access to the main application until login is completed
    login_window.transient(window)  # Make the login window appear on top of the main window
    login_window.grab_set()  # Disable interactions with the main window
    window.withdraw()  # Hide the main window

# Function to show the registration window
def show_registration_window():
    registration_window = customtkinter.CTkToplevel()
    registration_window.geometry("400x300")
    registration_window.title("Register")

    title_label = customtkinter.CTkLabel(registration_window, text="Register", font=("Arial", 24))
    title_label.pack(pady=20)

    username_entry = customtkinter.CTkEntry(registration_window, placeholder_text="Username")
    username_entry.pack(pady=10, padx=20)

    password_entry = customtkinter.CTkEntry(registration_window, placeholder_text="Password", show="*")
    password_entry.pack(pady=10, padx=20)

    confirm_password_entry = customtkinter.CTkEntry(registration_window, placeholder_text="Confirm Password", show="*")
    confirm_password_entry.pack(pady=10, padx=20)

    def register_user_action():
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            register_user(username, password)
            messagebox.showinfo("Success", "Registration successful!")
            registration_window.destroy()
            show_login_window()  # Show login window after successful registration
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    register_button = customtkinter.CTkButton(registration_window, text="Register", command=register_user_action)
    register_button.pack(pady=20)

# Main window setup and application initialization
window = customtkinter.CTk()
customtkinter.set_appearance_mode("Dark")
window.title("Metflix")
window.geometry('900x500')

# Initialize database setup and show the login window first
setup_database()
show_login_window()

window.mainloop()
