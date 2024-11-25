import tkinter
import sqlite3
import secrets

conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()
screen = tkinter.Tk()
screen.geometry("500x500")
screen.title("Password Manager")

cursor.execute("""CREATE TABLE IF NOT EXISTS Passwords(
                      password_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      e_mail_username TEXT,
                      website TEXT,
                      password_text TEXT)""")
conn.commit()


def generate_password():
    password = secrets.token_hex(5)
    password_text.delete(0, tkinter.END)
    password_text.insert(tkinter.END, password)


def add_new_credentials():
    website = str(website_text.get())
    email = str(email_text.get())
    password = str(password_text.get())
    cursor.execute(f"""INSERT INTO Passwords(
                   e_mail_username,
                   website,
                   password_text)
                   VALUES (?, ?, ?)""", [email, website, password])
    conn.commit()
    email_text.delete(0, tkinter.END)
    website_text.delete(0, tkinter.END)
    password_text.delete(0, tkinter.END)


def find_password_email():
    website = str(website_text.get())
    answer_list = cursor.execute(f"""SELECT e_mail_username, password_text
                                    FROM Passwords
                                    WHERE website = ?""", [website])
    answer = answer_list.fetchone()
    website = website_text.get()
    pop_up = tkinter.Toplevel()
    pop_up.wm_title("Email and Password")
    pop_up.geometry("650x75")
    answer_label = tkinter.Label(pop_up, text=f"Email and Password for {website}: ", font=("Arial", 12, "bold"))
    answer_label.grid(row=5, column=0, pady=5, sticky="w")
    answer_text = tkinter.Label(pop_up, text="", font=("Arial", 12, "bold"), wraplength=1000, justify="left", anchor="w")
    answer_text.grid(row=5, column=1, pady=5, sticky="w")
    answer = f"Email/Username: {str(answer[0])}\nPassword: {str(answer[1])}"
    answer_text.config(text=answer)
    website_text.delete(0, tkinter.END)


image = tkinter.PhotoImage(file="image.png")
image_frame = tkinter.Frame(screen, pady=10, padx=10)
image_frame.pack(pady=10)
image_label = tkinter.Label(image_frame, image=image, anchor="center")
image_label.grid(row=0, column=0)

elements_frame = tkinter.Frame(screen, pady=10, padx=10)
elements_frame.pack(pady=10)

website_label = tkinter.Label(elements_frame, text="Website:", font=("Arial", 12), anchor="w")
website_label.grid(row=0, column=0, pady=5, sticky="w")
website_text = tkinter.Entry(elements_frame, width=30, font=("Arial", 12))
website_text.grid(row=0, column=1, pady=5)

email_label = tkinter.Label(elements_frame, text="E-mail/Username:", font=("Arial", 12), anchor="w")
email_label.grid(row=1, column=0, pady=5, sticky="w")
email_text = tkinter.Entry(elements_frame, width=30, font=("Arial", 12))
email_text.grid(row=1, column=1, pady=5)

password_label = tkinter.Label(elements_frame, text="Password:", font=("Arial", 12), anchor="w")
password_label.grid(row=2, column=0, pady=5, sticky="w")
password_text = tkinter.Entry(elements_frame, width=12, font=("Arial", 12))
password_text.grid(row=2, column=1, pady=5, sticky="w")
password_generate_button = tkinter.Button(elements_frame, text="Generate Password", font=("Arial", 12),
                                          command=generate_password)
password_generate_button.grid(row=2, column=1, pady=5, sticky="e")

save_credentials_button = tkinter.Button(elements_frame, text="Save Credentials", font=("Arial", 12),
                                         command=add_new_credentials)
save_credentials_button.grid(row=3, column=1, pady=5, sticky="we")

find_password_button = tkinter.Button(elements_frame, text="Find Password", font=("Arial", 12),
                                      command=find_password_email)
find_password_button.grid(row=4, column=1, pady=5, sticky="we")

screen.mainloop()
conn.close()
