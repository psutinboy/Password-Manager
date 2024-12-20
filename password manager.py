import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import sqlite3
from cryptography.fernet import Fernet
import pyperclip
import random
import string

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('300x200+500+400')
        self.root.title('Password Manager')

        self.master_password_label = tk.Label(self.root, text='Master Password')
        self.master_password_label.pack()

        self.master_password_entry = tk.Entry(self.root, show='*')
        self.master_password_entry.pack()

        if not os.path.isfile('master_password_hash.txt'):
            self.set_button = tk.Button(self.root, text='Set Master Password', command=self.set_master_password)
            self.set_button.pack()
        else:
            self.check_button = tk.Button(self.root, text='Unlock', command=self.check_master_password)
            self.check_button.pack()

    def set_master_password(self):
        master_password = self.master_password_entry.get()
        with open('master_password_hash.txt', 'w') as f:
            f.write(hashlib.sha256(master_password.encode()).hexdigest())
        messagebox.showinfo('Success', 'Master password set!')
        self.set_button.destroy()
        self.check_button = tk.Button(self.root, text='Unlock', command=self.check_master_password)
        self.check_button.pack()

    def check_master_password(self):
        master_password = self.master_password_entry.get()
        with open('master_password_hash.txt', 'r') as f:
            correct_password_hash = f.read()
        if hashlib.sha256(master_password.encode()).hexdigest() == correct_password_hash:
            messagebox.showinfo('Success', 'Correct password!')
            self.open_password_manager()
        else:
            messagebox.showerror('Error', 'Incorrect password!')
            
    def open_password_manager(self):
        self.password_manager = PasswordManagerWindow(self.root)

class PasswordManagerWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.geometry('285x200+800+400')
        self.root.title('Password Manager')

        self.service_label = tk.Label(self.root, text='Service')
        self.service_label.grid(row=0, column=1, sticky='nsew')

        self.service_entry = tk.Entry(self.root)
        self.service_entry.grid(row=1, column=1, sticky='nsew')

        self.username_label = tk.Label(self.root, text='Username')
        self.username_label.grid(row=2, column=1, sticky='nsew')

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=3, column=1, sticky='nsew')

        self.password_label = tk.Label(self.root, text='Password')
        self.password_label.grid(row=4, column=1, sticky='nsew')

        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.grid(row=5, column=1, sticky='nsew')

        self.show_password = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.root, text='Show Password', variable=self.show_password, command=self.toggle_password)
        self.show_password_checkbutton.grid(row=6, column=1, sticky='nsew')

        self.add_button = tk.Button(self.root, text='Add Entry', command=self.add_password)
        self.add_button.grid(row=7, column=2, padx=5, pady=5)

        self.view_button = tk.Button(self.root, text='View Entries', command=self.view_passwords)
        self.view_button.grid(row=7, column=0, padx=5, pady=5)

        self.generate_button = tk.Button(self.root, text='Generate Password', command=self.generate_password)
        self.generate_button.grid(row=7, column=1, padx=5, pady=5)
        
    def generate_password(self):
        # Define the password length and the characters that can be used
        password_length = 12
        password_characters = string.ascii_letters + string.digits + string.punctuation

        # Generate a random password
        password = ''.join(random.choice(password_characters) for _ in range(password_length))

        # Set the password entry field to the new password
        self.password_entry.delete(0, 'end')
        self.password_entry.insert(0, password)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def add_password(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not password:
            messagebox.showerror('Error', 'Password cannot be empty!')
            return
        encrypted_password = cipher_suite.encrypt(password.encode())
        c.execute('INSERT INTO passwords VALUES (?, ?, ?)', (service, username, encrypted_password))
        conn.commit()
        messagebox.showinfo('Success', 'Password added!')
        self.service_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def view_passwords(self):
        self.view_passwords_window = ViewPasswordsWindow(self.root)
        
class ViewPasswordsWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.geometry('300x200+1085+400')
        self.root.title('View Passwords')
        
        # Add scrollbar to the listbox
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side='right', fill='y')

        self.passwords_listbox = tk.Listbox(self.root, yscrollcommand=self.scrollbar.set)
        self.passwords_listbox.pack(side='left', fill='both', expand=True)
        
        # Bind double click event to the listbox
        self.passwords_listbox.bind('<Double-Button-1>', self.show_password)
        
        self.passwords = {}

        for row in c.execute('SELECT * FROM passwords'):
            service = row[0]
            username = row[1]
            encrypted_password = row[2]
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            self.passwords[service] = (username, decrypted_password)
            
            self.passwords_listbox.insert('end', service)
            
    def show_password(self, event):
        selected_service = self.passwords_listbox.get(self.passwords_listbox.curselection())
        username, password = self.passwords[selected_service]
        
        info_window = tk.Toplevel(self.root)
        info_window.geometry('200x130+1130+430')
        info_window.title('Info')
        
        # Display the Service, Username, and Password
        service_label = tk.Label(info_window, text=f'Service: {selected_service}')
        service_label.pack()
        username_label = tk.Label(info_window, text=f'Username: {username}')
        username_label.pack()
        password_label = tk.Label(info_window, text=f'Password: {password}')
        password_label.pack()
        
        # Add buttons for copying the username and password
        copy_username_button = tk.Button(info_window, text='Copy Username', command=lambda: self.copy_to_clipboard(username))
        copy_username_button.pack()
        copy_password_button = tk.Button(info_window, text='Copy Password', command=lambda: self.copy_to_clipboard(password))
        copy_password_button.pack()
        
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
            
    def on_close(self):
        conn.close()
        self.root.destroy()

KEY_FILE = 'key.key'

def on_close():
    conn.close()
    root.destroy()

# Generate a key for encryption and decryption
if os.path.isfile(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
cipher_suite = Fernet(key)

# Create a SQLite database to store the passwords
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (service text, username text, password blob)''')

root = tk.Tk()
main_window = MainWindow(root)
root.protocol('WM_DELETE_WINDOW', on_close)
root.mainloop()