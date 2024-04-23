# Password Manager

This is a simple password manager built with Python and SQLite. It uses a master password to unlock the password manager, and stores service names, usernames, and encrypted passwords in a SQLite database.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3.6 or later.
* You have a Windows machine. This code may work on other platforms but it was developed and tested on Windows.

## Installing Password Manager

To install the necessary libraries, follow these steps:

1. Open your terminal.

2. Install the necessary Python libraries with pip:

```bash
pip install tkinter
pip install hashlib
pip install sqlite3
pip install cryptography
pip install pyperclip
pip install random
pip install string
```

## Using Password Manager

To use Password Manager, follow these steps:

1. Run the script in your terminal:(If you're running the script for the first time, you'll be asked to set a master password. This password will be used to unlock the password manager in the future.)
```bash
python password_manager.py
```

2. Once the master password is set, you can unlock the password manager by entering the master password.

* In the password manager, you can add passwords for different services. Each password entry requires a service name, a username, and a password.

* You can view the passwords you've added by clicking the 'View' button. This will open a new window with a list of services.

* Double click on a service to view the username and password for that service.

* You can also copy the username or password to the clipboard by clicking the 'Copy Username' or 'Copy Password' button.

* The password manager now includes a password generator. Click the 'Generate Password' button to generate a random password.

* You can choose to show or hide the password by checking or unchecking the 'Show Password' checkbox.

## Contact
If you want to contact me you can reach me at grantledbetter12@gmail.com.