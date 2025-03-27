import pandas as pd
import tkinter
from tkinter import messagebox
import musicplayer
import subprocess
import os

df = pd.read_csv(r"C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\user_db.csv")

# To create the main window + program size
main_window = tkinter.Tk()
main_window.title("Login Window")
canvas = tkinter.Canvas(main_window, width = 500, height = 300, bg="alice blue")
canvas.pack()

# Main title + subtitle
main_title = tkinter.Label(main_window, text="Music Player", font=("Brush Script MT", 24), bg="alice blue")
main_title.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
subtitle = tkinter.Label(main_window, text="By: Loke Sue-Vyen", font=("Arial", 8), bg="alice blue")
subtitle.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)


# to validate the login details
def login():
    email = email_entry.get()
    password = password_entry.get()
    
    # to update the system's reading
    df = pd.read_csv(r"C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\user_db.csv")
    
    # check whether the login details match those in the user_db.csv
    successful_login = False
    for index, row in df.iterrows():
        if row['Email'] == email and row['Password'] == password:
            successful_login = True
            break
        elif not email.endswith('@gmail.com'):
             successful_login = False
             messagebox.showinfo("Login Failed", "Dear Music Lover, we need an email")
             break
    
    # directs the user to the music player program
    if successful_login:
            messagebox.showinfo("Login Successful", "Welcome to the Music Player!")
            main_window.destroy()
            subprocess.Popen(["python", "musicplayer.py", email])
    
    else:
            messagebox.showerror("Login Failed", "Invalid email or password")

def signup():
    email = email_entry.get()
    password = password_entry.get()
    
    df = pd.read_csv(r"C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\user_db.csv")
    
    # cross checks if the email is being used already
    if email in df['Email'].values:
        messagebox.showinfo("Failed Sign-Up", "Dear Music Lover, this email has been used, try again.")

    # checks if the inputted email value is an email
    elif not email.endswith('@gmail.com'):
             messagebox.showinfo("Login Failed", "Dear Music Lover, we need an email")

    # adds the new email and password to the user_db
    else:
         new_data = pd.DataFrame({
            "Email": [email],
            "Password": [password]
        })
         new_data.to_csv("C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\user_db.csv", mode='a', index=False, header=False)
         
         messagebox.showinfo("Loading", "Creating your playlist platform...")
         user_directory = f"C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\{email[:-10]}"
         os.makedirs(user_directory)
         messagebox.showinfo("Sign-Up Successful", "Welcome New User!")

         main_window.destroy()
         subprocess.Popen(["python", "musicplayer.py", email])


# To create the email input
email_label = tkinter.Label(main_window, text = "Email: ")
email_label.place(relx = 0.5, rely = 0.4, anchor=tkinter.CENTER)
email_entry = tkinter.Entry(main_window)
email_entry.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

# To create the password input
password_label = tkinter.Label(main_window, text = "Password: ")
password_label.place(relx = 0.5, rely = 0.55, anchor=tkinter.CENTER)
password_entry = tkinter.Entry(main_window, show = "*")
password_entry.place(relx = 0.5, rely = 0.6, anchor=tkinter.CENTER)

# login button
login_button = tkinter.Button(main_window, text = "Login", command = login)
login_button.place(relx = 0.55, rely = 0.7, anchor=tkinter.CENTER)

# sign up button
sign_up_button = tkinter.Button(main_window, text = "Sign Up", command = signup)
sign_up_button.place(relx = 0.45, rely = 0.7, anchor=tkinter.CENTER)
main_window.mainloop()