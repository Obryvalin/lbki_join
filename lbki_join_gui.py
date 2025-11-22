# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lbki_join import read_csv, join_data, write_csv

class LBKIJoinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LBKI_JOIN — SQL JOIN для CSV")
        self.root.geometry("585x500")
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
        self.left_entry = tk.Entry(frame, width=40)
        self.left_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Обзор...", command=self.load_left).grid(row=0, column=2, padx=5)

        # Разделитель левого файла
        tk.Label(frame, text="Разделитель LEFT:").grid(row=1, column=0, sticky='w', pady=5)
        self.left_delimiter_var = tk.StringVar(value=',')
        left_delim_frame = tk.Frame(frame)
        left_delim_frame.grid(row=1, column=1, sticky='w', pady=5)
        for d, label in [(',', 'Запятая'), (';', 'Точка с запятой'), ('\t', 'Табуляция')]:
            tk.Radiobutton(left_delim_frame, text=label, variable=self.left_delimiter_var, value=d).pack(side=tk.LEFT)

        # Правые файлы
        tk.Label(frame, text="Правый CSV:").grid(row=2, column=0, sticky='w', pady=5)
        self.right_entry = tk.Entry(frame, width=40)
        self.right_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(frame, text="Обзор...", command=self.load_right).grid(row=2, column=2, padx=5)

        # Разделитель правого файла
        tk.Label(frame, text="Разделитель RIGHT:").grid(row=3, column=0, sticky='w', pady=5)
        self.right_delimiter_var = tk.StringVar(value=',')
        right_delim_frame = tk.Frame(frame)
        right_delim_frame.grid(row=3, column=1, sticky='w', pady=5)
        for d, label in [(',', 'Запятая'), (';', 'Точка с запятой'), ('\t', 'Табуляция')]:
            tk.Radiobutton(right_delim_frame, text=label, variable=self.right_delimiter_var, value=d).pack(side=tk.LEFT)

        # Ключи
        tk.Label(frame, text="Ключ LEFT:").grid(row=4, column=0, sticky='w', pady=5)
        self.left_key_combo = ttk.Combobox(frame, state='readonly')
        self.left_key_combo.grid(row=4, column=1, sticky='w', pady=5)

        tk.Label(frame, text="Ключ RIGHT:").grid(row=5, column=0, sticky='w', pady=5)
        self.right_key_combo = ttk.Combobox(frame, state='readonly')
        self.right_key_combo.grid(row=5, column=1, sticky='w', pady=5)

        # Тип JOIN
        tk.Label(frame, text="Тип JOIN:").grid(row=6, column=0, sticky='w', pady=5)
        self.join_type_var = tk.StringVar(value='inner')
        join_frame = tk.Frame(frame)
        join_frame.grid(row=6, column=1, sticky='w', pady=5)
        for j in ['inner', 'left', 'right', 'outer']:
            tk.Radiobutton(join_frame, text=j.upper(), variable=self.join_type_var, value=j).pack(side=tk.LEFT)

        # Выходной файл
        tk.Label(frame, text="Сохранить как:").grid(row=7, column=0, sticky='w', pady=5)
        self.output_entry = tk.Entry(frame, width=40)
        self.output_entry.grid(row=7, column=1, padx=5, pady=5)
        tk.Button(frame, text="Выбрать...", command=self.save_file).grid(row=7, column=2, padx=5)

        # Разделитель результирующего файла
        tk.Label(frame, text="Разделитель OUTPUT:").grid(row=8, column=0, sticky='w', pady=5)
        self.output_delimiter_var = tk.StringVar(value=',')
        output_delim_frame = tk.Frame(frame)
        output_delim_frame.grid(row=8, column=1, sticky='w', pady=5)
        for d, label in [(',', 'Запятая'), (';', 'Точка с запятой'), ('\t', 'Табуляция')]:
            tk.Radiobutton(output_delim_frame, text=label, variable=self.output_delimiter_var, value=d).pack(side=tk.LEFT)

        # Кнопка выполнения
        tk.Button(frame, text="Выполнить JOIN", bg="lightgreen", font=("Arial", 10, "bold"),
                  command=self.perform_join).grid(row=9, column=0, columnspan=3, pady=15)

        # Статистика
        tk.Label(frame, text="Статистика:", font=("Arial", 10, "bold")).grid(row=10, column=0, sticky='w', pady=(10, 5))
        self.stats_text = tk.Text(frame, height=5, width=70, state='disabled', bg='#f0f0f0')
        self.stats_text.grid(row=11, column=0, columnspan=3, sticky='nsew', pady=5)

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
            if side == 'left':
                delimiter = self.left_delimiter_var.get()
            else:
                delimiter = self.right_delimiter_var.get()
            
            if delimiter == '\t':
                delimiter = '\t'
            
            headers, data = read_csv(path, delimiter)
            if side == 'left':
                self.left_headers = headers
                self.left_data = data
                self.left_key_combo['values'] = headers
                if headers:
                    self.left_key_combo.current(0)
                self.update_stats()
            else:
                self.right_headers = headers
                self.right_data = data
                self.right_key_combo['values'] = headers
                if headers:
                    self.right_key_combo.current(0)
                self.update_stats()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

    def update_stats(self):
        """Обновляет статистику в текстовом поле."""
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', tk.END)
        
        stats = "Статистика файлов:\n"
        stats += "─" * 50 + "\n"
        
        if self.left_data:
            stats += f"Левый файл (LEFT):     {len(self.left_data)} строк\n"
        else:
            stats += "Левый файл (LEFT):     не загружен\n"
        
        if self.right_data:
            stats += f"Правый файл (RIGHT):   {len(self.right_data)} строк\n"
        else:
            stats += "Правый файл (RIGHT):   не загружен\n"
        
        self.stats_text.insert('1.0', stats)
        self.stats_text.config(state='disabled')

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
            output_delimiter = self.output_delimiter_var.get()
            if output_delimiter == '\t':
                output_delimiter = '\t'

            if not all([left_file, right_file, output_file, left_key, right_key]):
                raise ValueError("Заполните все поля!")

            result = join_data(self.left_data, self.right_data, left_key, right_key, join_type)
            write_csv(result, output_file, output_delimiter)

            # Обновляем статистику с результатом
            self.stats_text.config(state='normal')
            self.stats_text.delete('1.0', tk.END)
            
            stats = "Статистика файлов:\n"
            stats += "─" * 50 + "\n"
            stats += f"Левый файл (LEFT):     {len(self.left_data)} строк\n"
            stats += f"Правый файл (RIGHT):   {len(self.right_data)} строк\n"
            stats += "─" * 50 + "\n"
            stats += f"Результат ({join_type.upper()}):      {len(result)} строк\n"
            
            self.stats_text.insert('1.0', stats)
            self.stats_text.config(state='disabled')

            messagebox.showinfo("Успех", f"JOIN выполнен!\n\nЛевый файл: {len(self.left_data)} строк\nПравый файл: {len(self.right_data)} строк\nРезультат: {len(result)} строк\n\nСохранено в:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


def run_gui():
    root = tk.Tk()
    app = LBKIJoinApp(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()