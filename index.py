import os
from dotenv import load_dotenv
import imaplib as im
from email.header import decode_header
import email

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Definir las credenciales globales
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
            print("Opción inválida.")
            return None
    except im.IMAP4.error as e:
        print(f"Error de autenticación: {e}")
        return None

if __name__ == "__main__":
    try:
        choose = int(input("Seleccione un servicio:\n\t1. Outlook\n\t2. Google\n\t3. Google2\n\t4. Universidad\n\t"))
        response = ChooseService(choose)
        if response:
            response.select("INBOX")
            try:
                email_address = str(input("Digite el email de los correos: "))
            except ValueError:
                print("Entrada inválida. Por favor, introduzca un email válido.")
                exit()
            
            status, messages = response.search(None, f'FROM "{email_address}"')
            if status != "OK":
                print("No se encontraron correos de ese remitente.")
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
            print("No se pudo establecer la conexión.")
    except ValueError:
        print("Entrada inválida. Por favor, introduzca un número entero.")
