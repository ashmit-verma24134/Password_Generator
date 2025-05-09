from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import os



def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

def save():
    website = website_entry.get()                 #SAVE option
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)
                messagebox.showinfo(title="Success", message="Your password has been saved successfully!")


def search_password():        
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo(title="Error", message="Please enter a website to search for.")
    else:
        try:
            with open("data.txt", "r") as data_file:
                data = data_file.readlines()
                found = False
                updated_data = []

                for line in data:
                    line_parts = line.strip().split(" | ")
                    
                    if len(line_parts) == 3 and website.lower() in line_parts[0].lower():
                        email, old_password = line_parts[1], line_parts[2]
                       
                        new_password = simpledialog.askstring(
                            "Update Password", f"Current password: {old_password}\nEnter the new password:"
                        )
                        if new_password:
                       
                            updated_line = f"{line_parts[0]} | {email} | {new_password}\n"
                            updated_data.append(updated_line)
                            found = True
                        else:
                            updated_data.append(line)  
                    else:
                        updated_data.append(line)

                if found:
                    # Overwrite the file with updated data
                    with open("data.txt", "w") as data_file:
                        data_file.writelines(updated_data)
                    messagebox.showinfo(title="Success", message="Password updated successfully!")
                else:
                    messagebox.showinfo(title="Error", message="No details found for the entered website.")

        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No saved data found.")


#app
window = Tk()
window.title("Key Keeper")
window.config(padx=20, pady=20)

canvas = Canvas(height=300, width=350)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(220, 220, image=logo_img)
canvas.grid(row=0, column=1)


website_label = Label(text="Website:")
website_label.grid(row=3, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=4, column=0)
password_label = Label(text="Password:")
password_label.grid(row=5, column=0)


website_entry = Entry(width=35)
website_entry.grid(row=3, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=4, column=1, columnspan=2)
email_entry.insert(0, "")
password_entry = Entry(width=25)
password_entry.grid(row=5, column=1)


generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=7, column=1, columnspan=2)
search_button = Button(text="Search", width=36, command=search_password)
search_button.grid(row=8, column=1, columnspan=2)

window.mainloop()
