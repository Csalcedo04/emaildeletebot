# Email Message Deletion Script

This repository contains a Python script that allows users to connect to their email accounts and delete messages from a specified sender. The script supports multiple email services, including Outlook and Gmail, if you need a diferent service, checkout for the IMAP connection server: https://www.systoolsgroup.com/imap/.

## Features

- Connect to multiple email services (Outlook, Gmail, University mail).
- Delete all emails from a specified sender.
- Load credentials from a `.env` file for security.

## Getting Started

### Prerequisites

- Python 3.x
- `imaplib` library
- `python-dotenv` library

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/email-deletion-script.git
    cd email-deletion-script
    ```

2. Install the required Python libraries:
    ```bash
    pip install python-dotenv
    ```

3. Create a `.env` file in the root directory of the project and add your email credentials:
    ```env
    userNameGoogle=your_google_username
    passwordGoogle=your_google_password
    userNameGoogle2=your_google2_username
    passwordGoogle2=your_google2_password
    userNameOutlook=your_outlook_username
    passwordOutlook=your_outlook_password
    userNameUniversidad=your_university_username
    passwordUniversidad=your_university_password
    ```

### Usage

1. Run the script:
    ```bash
    python delete_emails.py
    ```

2. Select the email service you want to use:
    ```
    Select a service:
        1. Outlook
        2. Google
        3. Google2
        4. University
    ```

3. Enter the email address of the sender whose emails you want to delete:
    ```
    Enter the sender's email address:
    ```

### Script Details

The script performs the following steps:

1. Loads email credentials from the `.env` file.
2. Prompts the user to choose an email service.
3. Connects to the selected email service using IMAP.
4. Prompts the user to enter the email address of the sender.
5. Searches for emails from the specified sender in the INBOX.
6. Deletes all found emails from the specified sender.
7. Logs out from the email account.

### Example

```python
import os
from dotenv import load_dotenv
import imaplib as im
from email.header import decode_header
import email

# Load environment variables from .env file
load_dotenv()

# Define global credentials
u_Google = os.getenv("userNameGoogle")
p_Google = os.getenv("passwordGoogle")
u_Google2 = os.getenv("userNameGoogle2")
p_Google2 = os.getenv("passwordGoogle2")
u_Outlook = os.getenv("userNameOutlook")
p_Outlook = os.getenv("passwordOutlook")
u_Universidad = os.getenv("userNameUniversidad")
p_Universidad = os.getenv("passwordUniversidad")

def ChooseService(case: int):
    try:
        if case == 1:
            outlook = im.IMAP4_SSL("imap-mail.outlook.com")
            outlook.login(u_Outlook, p_Outlook)
            return outlook
        elif case == 2:
            google = im.IMAP4_SSL("imap.gmail.com")
            google.login(u_Google, p_Google)
            return google
        elif case == 3:
            google2 = im.IMAP4_SSL("imap.gmail.com")
            google2.login(u_Google2, p_Google2)
            return google2
        elif case == 4:
            universidad = im.IMAP4_SSL("imap-mail.outlook.com")
            universidad.login(u_Universidad, p_Universidad)
            return universidad
        else:
            print("Invalid option.")
            return None
    except im.IMAP4.error as e:
        print(f"Authentication error: {e}")
        return None

if __name__ == "__main__":
    try:
        choose = int(input("Select a service:\n\t1. Outlook\n\t2. Google\n\t3. Google2\n\t4. University\n\t"))
        response = ChooseService(choose)
        if response:
            response.select("INBOX")
            try:
                email_address = str(input("Enter the sender's email address: "))
            except ValueError:
                print("Invalid input. Please enter a valid email address.")
                exit()
            
            status, messages = response.search(None, f'FROM "{email_address}"')
            if status != "OK":
                print("No emails found from that sender.")
                exit()

            messages = messages[0].split()
            for mail in messages:
                _, msg = response.fetch(mail, "(RFC822)")
                for response_part in msg:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        # decode the email subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()
                        print("Deleting:", subject)
                # mark the mail as deleted
                response.store(mail, "+FLAGS", "\\Deleted")
            response.expunge()
            # close the mailbox
            response.close()
            # logout from the account
            response.logout()
        else:
            print("Connection could not be established.")
    except ValueError:
        print("Invalid input. Please enter an integer.")
