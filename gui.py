# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lbki_join import read_csv, join_data, write_csv

class LBKIJoinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LBKI_JOIN — SQL JOIN для CSV")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.left_data = []
        self.right_data = []
        self.left_headers = []
        self.right_headers = []

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Левые файлы
        tk.Label(frame, text="Левый CSV:").grid(row=0, column=0, sticky='w', pady=5)
        self.left_entry = tk.Entry(frame, width=50)
        self.left_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Обзор...", command=self.load_left).grid(row=0, column=2, padx=5)

        # Правые файлы
        tk.Label(frame, text="Правый CSV:").grid(row=1, column=0, sticky='w', pady=5)
        self.right_entry = tk.Entry(frame, width=50)
        self.right_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="Обзор...", command=self.load_right).grid(row=1, column=2, padx=5)

        # Разделители
        tk.Label(frame, text="Разделитель:").grid(row=2, column=0, sticky='w', pady=5)
        self.delimiter_var = tk.StringVar(value=',')
        delim_frame = tk.Frame(frame)
        delim_frame.grid(row=2, column=1, sticky='w', pady=5)
        for d, label in [(',', 'Запятая'), (';', 'Точка с запятой'), ('\t', 'Табуляция')]:
            tk.Radiobutton(delim_frame, text=label, variable=self.delimiter_var, value=d).pack(side=tk.LEFT)

        # Ключи
        tk.Label(frame, text="Ключ LEFT:").grid(row=3, column=0, sticky='w', pady=5)
        self.left_key_combo = ttk.Combobox(frame, state='readonly')
        self.left_key_combo.grid(row=3, column=1, sticky='w', pady=5)

        tk.Label(frame, text="Ключ RIGHT:").grid(row=4, column=0, sticky='w', pady=5)
        self.right_key_combo = ttk.Combobox(frame, state='readonly')
        self.right_key_combo.grid(row=4, column=1, sticky='w', pady=5)

        # Тип JOIN
        tk.Label(frame, text="Тип JOIN:").grid(row=5, column=0, sticky='w', pady=5)
        self.join_type_var = tk.StringVar(value='inner')
        join_frame = tk.Frame(frame)
        join_frame.grid(row=5, column=1, sticky='w', pady=5)
        for j in ['inner', 'left', 'right', 'outer']:
            tk.Radiobutton(join_frame, text=j.upper(), variable=self.join_type_var, value=j).pack(side=tk.LEFT)

        # Выходной файл
        tk.Label(frame, text="Сохранить как:").grid(row=6, column=0, sticky='w', pady=5)
        self.output_entry = tk.Entry(frame, width=50)
        self.output_entry.grid(row=6, column=1, padx=5, pady=5)
        tk.Button(frame, text="Выбрать...", command=self.save_file).grid(row=6, column=2, padx=5)

        # Кнопка выполнения
        tk.Button(frame, text="Выполнить JOIN", bg="lightgreen", font=("Arial", 10, "bold"),
                  command=self.perform_join).grid(row=7, column=0, columnspan=3, pady=20)

    def load_left(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.left_entry.delete(0, tk.END)
            self.left_entry.insert(0, path)
            self.load_headers(path, 'left')

    def load_right(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.right_entry.delete(0, tk.END)
            self.right_entry.insert(0, path)
            self.load_headers(path, 'right')

    def load_headers(self, path, side):
        try:
            delimiter = self.delimiter_var.get()
            if delimiter == '\t':
                delimiter = '\t'
            headers, data = read_csv(path, delimiter)
            if side == 'left':
                self.left_headers = headers
                self.left_data = data
                self.left_key_combo['values'] = headers
                if headers:
                    self.left_key_combo.current(0)
            else:
                self.right_headers = headers
                self.right_data = data
                self.right_key_combo['values'] = headers
                if headers:
                    self.right_key_combo.current(0)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def perform_join(self):
        try:
            left_file = self.left_entry.get()
            right_file = self.right_entry.get()
            output_file = self.output_entry.get()
            left_key = self.left_key_combo.get()
            right_key = self.right_key_combo.get()
            join_type = self.join_type_var.get()
            delimiter = self.delimiter_var.get()
            if delimiter == '\t':
                delimiter = '\t'

            if not all([left_file, right_file, output_file, left_key, right_key]):
                raise ValueError("Заполните все поля!")

            result = join_data(self.left_data, self.right_data, left_key, right_key, join_type)
            write_csv(result, output_file, delimiter)

            messagebox.showinfo("Успех", f"JOIN выполнен!\nСтрок: {len(result)}\nСохранено в:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


def run_gui():
    root = tk.Tk()
    app = LBKIJoinApp(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()