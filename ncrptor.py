import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2

class PasswordManager:
    def __init__(self):
        self._password = None
        self.remember_password = False

    def set_password(self, password, remember=False):
        self._password = password
        self.remember_password = remember

    def get_password(self):
        return self._password

    def clear_password(self):
        self._password = None
        self.remember_password = False

class NcrYptor:
    def __init__(self, master):
        self.master = master
        self.master.title("NcrYptor")
        self.master.configure(bg="#2E2E2E")

        self.file_name = None
        self.left_frame_visible = True
        self.password_manager = PasswordManager()

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')

        bg_color = "#000000"
        fg_color = "#FF6B6B"
        accent_color = "#000000"
        entry_bg = "#3E3E3E"

        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color)
        style.configure('TButton', background=accent_color, foreground=fg_color)
        style.map('TButton', background=[('active', '#333333')])
        style.configure('TRadiobutton', background=bg_color, foreground=fg_color)
        style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
        style.map('TRadiobutton', background=[('active', bg_color)])
        style.map('TCheckbutton', background=[('active', bg_color)])

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(expand=True, fill='both')

        self.left_frame = ttk.Frame(main_frame, width=300)
        self.left_frame.pack(side='left', fill='y', padx=(0, 10))
        self.left_frame.pack_propagate(False)

        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side='right', expand=True, fill='both')

        self.create_file_frame()
        self.create_password_frame()
        self.create_operation_frame()
        self.create_notebook()
        self.create_toggle_button()

    def create_file_frame(self):
        file_frame = ttk.Frame(self.left_frame)
        file_frame.pack(fill='x', pady=(0, 20))

        self.file_entry = ttk.Entry(file_frame, width=40)
        self.file_entry.pack(side='left', expand=True, fill='x', padx=(0, 10))

        open_file_btn = ttk.Button(file_frame, text="OPEN", command=self.open_file)
        open_file_btn.pack(side='right')

    def create_password_frame(self):
        password_frame = ttk.Frame(self.left_frame)
        password_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(password_frame, text="Password:").pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(fill='x', pady=(0, 10))

        ttk.Label(password_frame, text="Confirm Password:").pack(anchor='w', pady=(0, 5))
        self.confirm_password_entry = ttk.Entry(password_frame, show="*")
        self.confirm_password_entry.pack(fill='x', pady=(0, 10))

        self.remember_password_var = tk.BooleanVar(value=True)
        remember_password_check = ttk.Checkbutton(password_frame, text="Remember the Password", variable=self.remember_password_var)
        remember_password_check.pack(anchor='w', pady=(0, 10))

    def create_operation_frame(self):
        operation_frame = ttk.Frame(self.left_frame)
        operation_frame.pack(fill='x', pady=(0, 20))

        self.operation_var = tk.StringVar()
        encrypt_radio = ttk.Radiobutton(operation_frame, text="Encrypt", variable=self.operation_var, value="Encrypt")
        decrypt_radio = ttk.Radiobutton(operation_frame, text="Decrypt", variable=self.operation_var, value="Decrypt")
        encrypt_radio.pack(side='left', padx=(0, 20))
        decrypt_radio.pack(side='left')

        start_button = ttk.Button(self.left_frame, text="Start Operation", command=self.check_password)
        start_button.pack(fill='x')

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(expand=True, fill='both')

    def create_toggle_button(self):
        self.toggle_button = ttk.Button(self.master, text="Hide Encrypt/Decrypt", command=self.toggle_left_frame)
        self.toggle_button.pack(pady=(10, 10))

    def open_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if self.file_name:
            self.display_values(self.file_name)

    def display_values(self, file_path):
        filename = os.path.basename(file_path)
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def check_password(self):
        password1 = self.password_entry.get()
        password2 = self.confirm_password_entry.get()
        if password1 == password2 and password1:
            remember = self.remember_password_var.get()
            self.password_manager.set_password(password1, remember)
            self.start_program()
        else:
            messagebox.showinfo("Error", "Passwords do not match or are empty")

    def start_program(self):
        operation = self.operation_var.get()
        if operation == "Encrypt":
            self.encryption()
        elif operation == "Decrypt":
            self.decryption()
        else:
            messagebox.showinfo("Error", "Please select an operation")

        if not self.password_manager.remember_password:
            self.password_manager.clear_password()
            self.clear_password_fields()

    def encryption(self):
        try:
            password = self.password_manager.get_password()
            if password:
                encrypt_file(self.file_name, password)
                messagebox.showinfo("Success", "File encrypted successfully")
            else:
                messagebox.showinfo("Error", "Please enter and confirm the password")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decryption(self):
        try:
            password = self.password_manager.get_password()
            if password:
                decrypted_content = decrypt_file(self.file_name, password, save_to_file=False)
                self.open_tab(self.file_name, decrypted_content)
            else:
                messagebox.showinfo("Error", "Please enter and confirm the password")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_password_fields(self):
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    def open_tab(self, file_name, content):
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=os.path.basename(file_name))

        text_area = scrolledtext.ScrolledText(tab_frame, wrap=tk.WORD, bg="#3E3E3E", fg="#FF6B6B", undo=True,
                                              font=("TkDefaultFont", 12), insertbackground='red')
        text_area.pack(expand=True, fill='both', padx=10, pady=10)

        text_area.insert(tk.END, content)
        text_area.edit_reset()

        text_area.bind("<Control-z>", lambda event: text_area.edit_undo())
        text_area.bind("<Control-y>", lambda event: text_area.edit_redo())

        button_frame = ttk.Frame(tab_frame)
        button_frame.pack(fill='x', padx=10, pady=10)

        save_button = ttk.Button(button_frame, text="Save Decrypted File",
                                 command=lambda: self.save_changes(text_area.get('1.0', tk.END), file_name))
        save_button.pack(side='left', padx=(0, 10))

        encrypt_button = ttk.Button(button_frame, text="Encrypt and Save",
                                    command=lambda: self.encrypt_and_save(text_area.get('1.0', tk.END), file_name))
        encrypt_button.pack(side='left')

        close_button = ttk.Button(button_frame, text="Close Tab", command=lambda: self.close_tab(tab_frame))
        close_button.pack(side='right')

    def close_tab(self, tab):
        self.notebook.forget(tab)

    def save_changes(self, content, file_name):
        try:
            with open(file_name[:-4], 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", "Changes saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")

    def encrypt_and_save(self, content, file_name):
        try:
            password = self.password_manager.get_password()
            if not password:
                messagebox.showinfo("Error", "No password available. Please enter a password in the main window.")
                return

            # Create a temporary file with the current content
            temp_file = file_name[:-4] + "_temp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)

            # Encrypt the temporary file
            encrypt_file(temp_file, password)

            # Remove the temporary file and rename the encrypted file
            os.remove(temp_file)
            encrypted_file = temp_file + ".enc"

            # If the original file was already encrypted, replace it
            # Otherwise, create a new .enc file
            if file_name.endswith('.enc'):
                os.replace(encrypted_file, file_name)
            else:
                os.rename(encrypted_file, file_name + ".enc")

            messagebox.showinfo("Success", "Content encrypted and saved successfully")

            # Close the current tab as the file has been encrypted
            current_tab = self.notebook.select()
            self.notebook.forget(current_tab)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt and save: {str(e)}")

    def toggle_left_frame(self):
        if self.left_frame_visible:
            self.left_frame.pack_forget()
            self.right_frame.pack(side='left', expand=True, fill='both')
            self.toggle_button.config(text="Show Encrypt/Decrypt")
        else:
            self.left_frame.pack(side='left', fill='y', padx=(0, 10))
            self.right_frame.pack(side='right', expand=True, fill='both')
            self.toggle_button.config(text="Hide Encrypt/Decrypt")
        self.left_frame_visible = not self.left_frame_visible

# Keep the encryption and decryption functions as they are
def derive_key(password, salt=b'salt', key_length=32):
    return PBKDF2(password, salt, key_length)

def encrypt_file(file_path, password):
    key = derive_key(password.encode())
    with open(file_path, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(cipher.iv + ct_bytes)

def decrypt_file(file_path, password, save_to_file=True):
    key = derive_key(password.encode())
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ct_bytes = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_bytes = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    if save_to_file:
        decrypted_file_path = file_path[:-4]  # Remove the '.enc' extension
        with open(decrypted_file_path, 'wb') as f:
            f.write(pt_bytes)
        return None
    else:
        return pt_bytes.decode('utf-8', errors='replace')

if __name__ == "__main__":
    root = tk.Tk()
    app = NcrYptor(root)
    root.mainloop()