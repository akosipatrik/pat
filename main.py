from tkinter import *
from PIL import ImageTk, Image, ImageFilter
import customtkinter as ctk
import customtkinter
import os
from tkinter import messagebox
import sqlite3
import bcrypt
import tkinter as tk
import pandas as pd
import csv

# Define an empty dictionary to store the dataset
dataset = {}

# Open and read the CSV file
with open('dataset.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)  # Read the CSV into a dictionary format
    for row in reader:
        # Use the 'Image Name' as the key in the dictionary
        dataset[row['Image Name']] = {
            'description': row['Description'],
            'category': row['Category'],
            'author': row['Author'],
            'genre': row['Genre']
        }

# Example: Accessing data for a specific image name
image_name = 'The_Four_Bad_Boys_and_Me_by_Tina_Lata.jpg'
if image_name in dataset:
    print(f"Description: {dataset[image_name]['description']}")
    print(f"Category: {dataset[image_name]['category']}")
    print(f"Author: {dataset[image_name]['author']}")
    print(f"Genre: {dataset[image_name]['genre']}")

# Main window
window = customtkinter.CTk()
customtkinter.set_appearance_mode("Light")
window.title("Metflix")
window.geometry('1280x720')
window.iconbitmap(r"C:\Users\micae\Downloads\New folder\petask3 HCI\assets\logo.ico")

# Create the main frame (container)
main_frame = ctk.CTkFrame(window, fg_color="white")
main_frame.pack(fill="both", expand=True)

# Create the table when the application starts (if it doesn't already exist)
def setup_database():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

def on_genre_selected(choice):
    filter_by_genre(choice)

# Update the dropdown values to pull unique genres from your dataset
genres = list(dataset.values())[0].get("genre")  # Make sure this is pulled from the dataset
genre_dropdown = customtkinter.CTkOptionMenu(
    master=main_frame,
    values=["All"] + list(set(genres)),  # Add an "All" option to show all genres
    command=on_genre_selected
)
genre_dropdown.pack(pady=10)

# Login Window
def show_login_window():
    global login_window  # Make login_window globally accessible
    login_window = customtkinter.CTkToplevel()
    customtkinter.set_appearance_mode("light")
    login_window.title("Login")
    login_window.geometry("1280x720")
    login_window.iconbitmap(r"C:\Users\micae\Downloads\New folder\petask3 HCI\assets\logo.ico")
    
    # Center the login window on the screen
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    window_width = 1280  # Width of the login window
    window_height = 720  # Height of the login window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a full background frame with the color #e9d1b5
    background_frame = customtkinter.CTkFrame(login_window, width=window_width, height=window_height, fg_color="#e9d1b5")
    background_frame.pack(fill="both", expand=True)

    # Create an inner frame for the login content
    frame = customtkinter.CTkFrame(background_frame, width=400, height=600, fg_color="white")
    frame.pack_propagate(False)  # Prevent the frame from resizing based on its content
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the login frame in the background

    # Title label
    title_label = customtkinter.CTkLabel(frame, text="Metflix Login", font=("Arial", 24))
    title_label.pack(pady=20)

    # Username input
    username_entry = customtkinter.CTkEntry(frame, placeholder_text="Username")
    username_entry.pack(pady=10, padx=20)

    # Password input
    password_entry = customtkinter.CTkEntry(frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=0, padx=20)

    # Place this inside show_login_window(), near the other widgets
    message_label = customtkinter.CTkLabel(frame, text="", text_color="red", font=("Arial", 12))
    message_label.pack(pady=0)

# Updated validate_login function
    def validate_login():
        username = username_entry.get().strip()
        password = password_entry.get()
    
        # Clear the message label first
        message_label.configure(text="", text_color="red")

        if not username:
            message_label.configure(text="Please enter your username.")
            return

        if not password:
            message_label.configure(text="Please enter your password.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
                # Login successful
                login_window.destroy()  # Close login window
                window.deiconify()  # Show the main application window
                clicker("Homepage")
            else:
                # Invalid login
                message_label.configure(text="Incorrect username or password.")
        except Exception as e:
            # Handle unexpected errors
            message_label.configure(text="An error occurred. Please try again.")

    # Login button
    login_button = customtkinter.CTkButton(frame, text="Login", command=validate_login)
    login_button.pack(pady=(0, 5))

    # Register button
    register_button = customtkinter.CTkButton(frame, text="Register", command=switch_to_register)
    register_button.pack(pady=5)

    # Prevent access to the main application until login is completed
    login_window.transient(window)  # Make the login window appear on top of the main window
    login_window.grab_set()  # Disable interactions with the main window
    window.withdraw()  # Hide the main window

# Registration Window
def show_registration_window():
    registration_window = customtkinter.CTkToplevel()
    registration_window.geometry("1280x720")
    registration_window.title("Register")
    registration_window.iconbitmap(r"C:\Users\Admin\Documents\petask3 HCI\assets")

    # Full background frame with the color #e9d1b5
    background_frame = customtkinter.CTkFrame(registration_window, width=1280, height=720, fg_color="#e9d1b5")
    background_frame.pack(fill="both", expand=True)

    # Centered registration frame inside the background
    registration_frame = customtkinter.CTkFrame(background_frame, width=400, height=600, fg_color="white")
    registration_frame.pack_propagate(False)
    registration_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title label
    title_label = customtkinter.CTkLabel(registration_frame, text="Register", font=("Arial", 24))
    title_label.pack(pady=20)

    # Username input
    username_entry = customtkinter.CTkEntry(registration_frame, placeholder_text="Username")
    username_entry.pack(pady=10, padx=20)

    # Password input
    password_entry = customtkinter.CTkEntry(registration_frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=10, padx=20)

    # Confirm Password input
    confirm_password_entry = customtkinter.CTkEntry(registration_frame, placeholder_text="Confirm Password", show="*")
    confirm_password_entry.pack(pady=10, padx=20)

    # Message label for displaying errors
    message_label = customtkinter.CTkLabel(registration_frame, text="", font=("Arial", 12), text_color="red")
    message_label.pack(pady=10)

    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Clear the message label
        message_label.configure(text="")

        if not username or not password or not confirm_password:
            message_label.configure(text="All fields are required!")
            return

        if len(password) < 8:
            message_label.configure(text="Password must be at least 8 characters long!")
            return

        if password != confirm_password:
            message_label.configure(text="Passwords do not match!")
            return

        try:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert user into the database
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()

            # Show success message and switch to login
            message_label.configure(text="Registration successful!", text_color="green")
            registration_window.after(1500, lambda: [registration_window.destroy(), show_login_window()])
        except sqlite3.IntegrityError:
            message_label.configure(text="Username already exists!")

    # Register button
    register_button = customtkinter.CTkButton(registration_frame, text="Register", command=register_user)
    register_button.pack(pady=20)

    # Back to Login button
    back_to_login_button = customtkinter.CTkButton(registration_frame, text="Back to Login", command=lambda: switch_to_login(registration_window))
    back_to_login_button.pack(pady=10)

# Switching Functions
def switch_to_register():
    login_window.destroy()  # Close the login window
    show_registration_window()  # Open the registration window

def switch_to_login(current_window):
    current_window.destroy()  # Close the current window (registration)
    show_login_window()  # Reopen the login window


# Call the login window before the main application
setup_database()
show_login_window()

# Define the image directory
image_directory = r"C:\Users\Admin\Documents\petask3 HCI\assets"


# Frame for the buttons on the left side
button_frame = customtkinter.CTkFrame(window, fg_color="#e9d1b5", corner_radius=0)
button_frame.pack(side='left', fill=BOTH, expand=FALSE, pady=0, padx=0)

# Content frame to hold dynamic content
content_frame = customtkinter.CTkFrame(window, fg_color="white")
content_frame.pack(side='right', fill='both', expand=True)

# Function to filter and display content based on genre
def filter_by_genre(genre):
    # Clear any existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a scrollable frame for the genre content
    genre_frame = customtkinter.CTkScrollableFrame(content_frame, fg_color="white")
    genre_frame.pack(side="top", fill="both", expand=True)

    # Loop through the dataset and display images for the selected genre
    for image_name, data in dataset.items():
        if genre == "All" or data["genre"] == genre:
            # Assuming your images are in the directory you specified
            image_path = os.path.join(image_directory, image_name)
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image_resized = image.resize((200, 320), Image.LANCZOS)
                ctk_image = customtkinter.CTkImage(light_image=image_resized, dark_image=image_resized, size=(200, 320))
            else:
                print(f"Error: {image_path} not found.")
                continue

            # Create button with image
            button = customtkinter.CTkButton(
                genre_frame,
                text="",
                image=ctk_image,
                fg_color="transparent",
                hover_color="white",
                command=lambda img_name=image_name: show_image_details(img_name),
                width=0,
                height=0
            )
            button.grid(row=(i // 4) * 2, column=i % 4, padx=45, pady=(15, 0))

            # Create label with image title
            title = os.path.splitext(image_name)[0]
            label = customtkinter.CTkLabel(
                genre_frame,
                text=title,
                font=("Baskerville Old Face", 20),
                wraplength=200,
                justify="center",
                fg_color="transparent",
                text_color="black"
            )
            label.grid(row=(i // 4) * 2 + 1, column=i % 4, pady=(1, 1))

    # If no images are available for the genre, display a message
    if not button_images:
        no_content_label = customtkinter.CTkLabel(
            genre_frame,
            text="No content available for this genre.",
            font=("Arial", 18),
            fg_color="transparent",
            text_color="black"
        )
        no_content_label.pack(pady=20)


        # Dropdown list for genres
genre_dropdown_label = customtkinter.CTkLabel(button_frame, text="Select Genre:", font=("Baskerville Old Face", 14))
genre_dropdown_label.pack(pady=(20, 5))

# Available genres
genres = ["All", "Fiction", "Romance", "Fantasy", "Horror", "Thriller", "Adventure"]

# Dropdown
genre_dropdown = customtkinter.CTkComboBox(
    button_frame,
    values=genres,
    font=("Baskerville Old Face", 14),
    fg_color="#e9d1b5",
    dropdown_font=("Baskerville Old Face", 14),
    dropdown_hover_color="#d2a167",
    dropdown_fg_color="#e9d1b5",
    corner_radius=15,
    border_width=0,
    button_color="#e9d1b5",
    button_hover_color="#d2a167",
    command=filter_by_genre,  # Calls filter_by_genre when a genre is selected
    width=95,
)
genre_dropdown.set("All")  # Set default value
genre_dropdown.pack(pady=(5, 5))

# Existing code for the Homepage, Trending, and Favorites buttons
options = {
    "Homepage": os.path.join(image_directory, "home.png"),
    "Trending": os.path.join(image_directory, "movie.png"),
    "Favorites": os.path.join(image_directory, "bookmark.png")
}

# Resize the images
resize_size = (60, 60)

# Buttons with images
for option, image_path in options.items():
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Skipping {option} button.")
        continue  # Skip if image is not found

    # Load and resize the image
    original_image = Image.open(image_path)
    resized_image = original_image.resize(resize_size, Image.LANCZOS)

    # CTkImage from the resized image
    ctk_image = customtkinter.CTkImage(light_image=resized_image, 
                                       dark_image=resized_image, 
                                       size=resize_size)

    # Button with the CTkImage
    button = customtkinter.CTkButton(
        button_frame,
        image=ctk_image,
        text="",
        command=lambda opt=option: clicker(opt),  # Pass option to lambda function
        width=10,
        height=100,
        hover_color="#d2a167",
        fg_color=button_frame.cget("fg_color"),
    )
    button.image = ctk_image  # Prevent garbage collection
    button.pack(side='top', anchor='s', pady=40, padx=2.5)

def show_image_details(image_name):
    # Get the details for the clicked image from the dataset
    image_details = dataset.get(image_name)
    if image_details:
        description = image_details["description"]
        author = image_details["author"]
        genre = image_details["genre"]

        # Display this information (create a new window or label for this)
        details_window = customtkinter.CTkToplevel(window)
        details_window.title(f"{image_name} Details")
        details_window.geometry("600x400")

        details_label = customtkinter.CTkLabel(
            details_window, text=f"Title: {image_name}\nDescription: {description}\nAuthor: {author}\nGenre: {genre}",
            font=("Arial", 14)
        )
        details_label.pack(pady=20)
        
        # Function to display a new frame when an image is clicked
def display_details(img_name):
    # Fetch story data from the dataset
    story_data = dataset.get(img_name, {
        "description": "No description available.",
        "category": "Uncategorized",
        "author": "Unknown",
        "genre": "Unknown"
    })

    # Clear the details frame
    for widget in details_frame.winfo_children():
        widget.destroy()
        
        details_frame = customtkinter.CTkFrame(window, fg_color="white")
        details_frame.pack(fill="both", expand=True)

    # Display story details
    description_label = customtkinter.CTkLabel(
        details_frame,
        text=(
            f"Description: {story_data['description']}\n"
            f"Category: {story_data['category']}\n"
            f"Author: {story_data['author']}\n"
            f"Genre: {story_data['genre']}"
        ),
        text_color="black",
        wraplength=500,
        justify="left",
        font=("Arial", 14)
    )
    description_label.place(x=400, y=50)
    
button_images=[]

# Function to handle button clicks
def clicker(option):
    print(f"{option} clicked")

    # Clear any existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a scrollable frame for "Homepage", "Trending", and "Favorites"
    if option in ["Homepage", "Trending", "Favorites"]:
        scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, fg_color="white")
        scrollable_frame.pack(fill="both", expand=True)

        # Define different sets of images for each section
        if option == "Homepage":
            button_images = ["The Four Bad Boys and Me by Tina Lata.jpg", "Daddy Material by Oikawa Tooru.jpg","College Heart-Throb Secret Husband by Winter bear.jpg",
                            "The Love Hypothesis by Ali Hazelwood.jpg", "After by Anna Todd.jpg", "Meant for You by Anya.jpg","Throne of Glass by Sarah J. Maas's.jpg",
                            "A Court of Thorns and Roses by Sarah J Maas.jpg", "The Hunger Games by Suzanne Collins.jpg","Family Comes First by Mason Gitzgibbon.jpg", 
                            "Hide and Seek by Jakayla Toney.jpg", "The Cellar by Natasha Preston.jpg", "Invisible Armies by Jon Evans.jpg", "The Purgatorium by Eva Pohler.jpg", 
                            "The Silent Patient by Alex Michaelides.jpg", "The Rider's Legend by SaoiMarie. Tremble.jpg", 
                            "The Rookie Pirates by Robin Amor.jpg", "Ocean Blue by Olivia Vaughn.jpg"]
        elif option == "Trending":
            button_images = ["The Rookie Pirates by Robin Amor.jpg", "Ocean Blue by Olivia Vaughn.jpg", "The Rider's Legend by SaoiMarie. Tremble.jpg", "The Four Bad Boys and Me by Tina Lata.jpg", 
                             "Daddy Material by Oikawa Tooru.jpg","College Heart-Throb Secret Husband by Winter bear.jpg", "Family Comes First by Mason Gitzgibbon.jpg", "Hide and Seek by Jakayla Toney.jpg"]
        elif option == "Favorites":
            button_images = ["The Rider's Legend by SaoiMarie. Tremble.jpg", "The Rookie Pirates by Robin Amor.jpg", "Ocean Blue by Olivia Vaughn.jpg", "The Hunger Games by Suzanne Collins.jpg", 
                             "Invisible Armies by Jon Evans.jpg", "The Purgatorium by Eva Pohler.jpg", "After by Anna Todd.jpg",
                             "Throne of Glass by Sarah J. Maas's.jpg", "A Court of Thorns and Roses by Sarah J Maas.jpg""The Rider's Legend by SaoiMarie. Tremble.jpg", "The Rookie Pirates by Robin Amor.jpg", 
                             "Ocean Blue by Olivia Vaughn.jpg", "The Hunger Games by Suzanne Collins.jpg", "Invisible Armies by Jon Evans.jpg", "The Purgatorium by Eva Pohler.jpg", 
                             "The Silent Patient by Alex Michaelides.jpg", "Throne of Glass by Sarah J. Maas's.jpg", "A Court of Thorns and Roses by Sarah J Maas.jpg"]


        # To customize the picture size and the spacing
        for i, image_name in enumerate(button_images):
            image_path = os.path.join(image_directory, image_name)
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image_resized = image.resize((200, 320), Image.LANCZOS)
                ctk_image = customtkinter.CTkImage(light_image=image_resized, dark_image=image_resized, size=(200, 320))
            else:
                print(f"Error: {image_path} not found.")
                continue  # Skip if image is not found

            # Create a button with the CTkImage and call show_image_details when clicked
            button = customtkinter.CTkButton(
                scrollable_frame,
                text="",
                image=ctk_image,
                fg_color="transparent",
                hover_color="white",
                command=lambda img_name=image_name: show_image_details(img_name),  # Pass img_name to lambda
                width=0,
                height=0
            )
            # Arrange buttons in a grid with a maximum of 5 buttons per row
            button.grid(row=(i // 4) * 2, column=i % 4, padx=45, pady=(15, 0))
            
            # Extract image name without extension for display as title
            title = os.path.splitext(image_name)[0]
            label = customtkinter.CTkLabel(
                scrollable_frame,
                text=title,
                font=("Baskerville Old Face", 20),
                wraplength=200,
                justify="center",
                fg_color="transparent",
                text_color="black"
            )
            # Place the label below the corresponding button
            label.grid(row=(i // 4) * 2 + 1, column=i % 4, pady=(1, 1))
    
window.mainloop()