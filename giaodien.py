import tkinter as tk
from tkinter import scrolledtext, messagebox
from modules import classify_test

class SpamFilterGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Phân loại thư rác")
        self.master.geometry("1050x900")
        self.master.resizable(False, False)

        tk.Label(master, text="Nhập nội dung thư:", font=("Arial", 12)).pack(anchor='w', padx=10, pady=(10, 0))
        self.email_input = scrolledtext.ScrolledText(master, height=20, font=("Arial", 11))
        self.email_input.pack(fill="x", padx=10, pady=5)

        tk.Button(
            master,
            text="Lọc thư",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            height=2,
            width=15,
            command=self.run_filter
        ).pack(pady=15)

        tk.Label(master, text="Spam:", font=("Arial", 11)).pack(anchor='w', padx=10)
        self.spam_words_output = scrolledtext.ScrolledText(master, height=10, font=("Arial", 11), state='normal')
        self.spam_words_output.pack(fill="x", padx=10, pady=5)

        tk.Label(master, text="Ham:", font=("Arial", 11)).pack(anchor='w', padx=10)
        self.result_output = scrolledtext.ScrolledText(master, height=10, font=("Arial", 11), state='normal')
        self.result_output.pack(fill="x", padx=10, pady=(5, 10))

    def run_filter(self):
        message = self.email_input.get("1.0", tk.END).strip()
        
        if not message:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung thư!")
            return

        result = classify_test(message)

        self.spam_words_output.config(state='normal')
        self.result_output.config(state='normal')
        self.spam_words_output.delete("1.0", tk.END)
        self.result_output.delete("1.0", tk.END)

        if result == "spam":
            self.spam_words_output.insert(tk.END, message)
        elif result == "ham":
            self.result_output.insert(tk.END, message)
        else:
            messagebox.showinfo("Thông báo", "Không thể phân loại. Cần phân loại thủ công.")

        self.spam_words_output.config(state='disabled')
        self.result_output.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = SpamFilterGUI(root)
    root.mainloop()
