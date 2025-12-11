import tkinter as tk
from tkinter import ttk, messagebox
import random
from server import db_manager


class SortingApp:
    #инит автоматически вызывается при создании нового объекта класса
    def __init__(self, root):
        #селф параметр ссылка на сам объект, через него устанавливаем атрибуты объекта
        self.status_var = tk.StringVar(value="Готов к работе")
        self.root = root
        self.root.title("Сортировка массивов")
        self.root.geometry("700x600")

        #переменные приложения
        self.original_array = []
        self.sorted_array = []
        self.current_user = None

        self.create_login_screen()

    #создание экрана авторизации
    def create_login_screen(self):
        self.clear_screen()

        #создание фрейма и расширение
        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.pack(expand=True)

        #создание метки и размещение с вертик отступами
        ttk.Label(login_frame, text="Авторизация", font=('Arial', 16)).pack(pady=10)

        #поле имени пользователя
        ttk.Label(login_frame, text="Имя пользователя:").pack(pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)

        #поле пароля
        ttk.Label(login_frame, text="Пароль:").pack(pady=5)
        self.password_entry = ttk.Entry(login_frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        #кнопки авторизации и регистрации
        btn_frame = ttk.Frame(login_frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Войти", command=self.login).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Зарегистрироваться", command=self.register).pack(side="left", padx=5)

    #создание основного интерфейса
    def create_main_interface(self):
        self.clear_screen()

        #верхняя панель с инфой о пользователе
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x") #заполнение по горизонтали

        ttk.Label(top_frame, text=f"Пользователь: {self.current_user['username']}",
                  font=('Arial', 12)).pack(side="left")
        ttk.Button(top_frame, text="Выйти", command=self.logout).pack(side="right")
        ttk.Button(top_frame, text="Мои массивы", command=self.show_saved_arrays).pack(side="right", padx=5)
        ttk.Button(top_frame, text="Справка", command=self.show_help).pack(side="right", padx=5)

        #фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Ввод массива", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        #поле для ввода массива
        ttk.Label(input_frame, text="Массив (через запятую):").pack(anchor="w", pady=(10, 0)) #выравнивание по левому краю и отступы сверху 10 снизу0
        self.array_entry = ttk.Entry(input_frame, width=50)
        self.array_entry.pack(fill="x", pady=5)

        #кнопка генерации случайного массива
        self.generate_btn = ttk.Button(input_frame, text="Сгенерировать массив",
                                       command=self.generate_random_array)
        self.generate_btn.pack(pady=5)

        #кнопка сортировки
        self.sort_btn = ttk.Button(input_frame, text="Отсортировать массив",
                                   command=self.sort_array)
        self.sort_btn.pack(pady=5)

        #фрейм для отображения результатов
        result_frame = ttk.LabelFrame(self.root, text="Результаты", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        #исходный массив
        ttk.Label(result_frame, text="Исходный массив:").pack(anchor="w")
        self.original_text = tk.Text(result_frame, height=3, width=70)
        self.original_text.pack(fill="x", pady=5)

        #отсортированный массив
        ttk.Label(result_frame, text="Отсортированный массив:").pack(anchor="w")
        self.sorted_text = tk.Text(result_frame, height=3, width=70)
        self.sorted_text.pack(fill="x", pady=5)

        #кнопки сохранения
        save_frame = ttk.Frame(result_frame)
        save_frame.pack(fill="x", pady=10)

        ttk.Button(save_frame, text="Сохранить массивы",
                   command=self.save_array).pack(side="left", padx=5)

        #статус
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken") #создание рамки
        status_bar.pack(fill="x", side="bottom", padx=10, pady=5)

    #очистка экрана
    def clear_screen(self):
        #проход по всем дочерним виджетам окна
        for widget in self.root.winfo_children():
            widget.destroy()

    #авторизация пользователя
    def login(self):
        username = self.username_entry.get().strip()  #гет берет текст из поля
        password = self.password_entry.get().strip() #стрип удаление пробелов в начале и в конце

        if not username or not password:
            messagebox.showwarning("Предупреждение", "Введите имя пользователя и пароль")
            return

        success, result = db_manager.authenticate_user(username, password)

        if success:
            self.current_user = result
            self.create_main_interface()
            self.status_var.set(f"Добро пожаловать, {username}!")
        else:
            messagebox.showerror("Ошибка", result)

    #регистрация
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Предупреждение", "Введите имя пользователя и пароль")
            return

        if len(username) < 3:
            messagebox.showwarning("Предупреждение", "Имя пользователя должно содержать минимум 3 символа")
            return

        success, message = db_manager.register_user(username, password)

        if success:
            messagebox.showinfo("Результат", message)
        else:
            messagebox.showerror("Ошибка", message)

    #выход из системы
    def logout(self):
        self.current_user = None
        self.create_login_screen()

    #генерация случайного массива
    def generate_random_array(self):
        try:
            size = random.randint(5, 20)
            self.original_array = [random.randint(-100, 100) for _ in range(size)]
            self.sorted_array = []  # Сбрасываем отсортированный массив при генерации нового
            self.array_entry.delete(0, tk.END)
            self.array_entry.insert(0, ", ".join(map(str, self.original_array)))
            self.update_display()
            self.status_var.set(f"Сгенерирован массив из {size} элементов")
        except Exception:
            messagebox.showerror("Ошибка", f"Ошибка генерации: {str(Exception)}")


    #сортировка
    def sort_array(self):
        try:
            input_str = self.array_entry.get().strip()
            if not input_str:
                messagebox.showwarning("Предупреждение", "Введите массив для сортировки")
                return

            try:
                self.original_array = [int(x.strip()) for x in input_str.split(",")]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат массива")
                return

            if not self.original_array:
                messagebox.showwarning("Предупреждение", "Сначала введите или сгенерируйте массив")
                return

            self.sorted_array = self.quick_sort(self.original_array.copy())
            self.update_display()
            self.status_var.set("Массив успешно отсортирован")

        except Exception:
            messagebox.showerror("Ошибка", f"Ошибка сортировки: {str(Exception)}")

    #быстрая сортировка
    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        #рекурсивно сортируем левую и правую часть
        return self.quick_sort(left) + middle + self.quick_sort(right)

    #справка
    def show_help(self):
        help_text = """
        Инструкция по использованию:

        1. ВХОД/РЕГИСТРАЦИЯ:
           - Введите имя пользователя и пароль
           - Минимум 3 символа в имени пользователя

        2. РАБОТА С МАССИВАМИ:
           - Введите числа через запятую
           - Или сгенерируйте случайный массив
           - Нажмите "Отсортировать" для сортировки

        3. СОХРАНЕНИЕ:
           - Сохраняйте исходные или отсортированные массивы
           - Просматривайте историю в "Мои массивы"

        4. СОРТИРОВКА:
           - Используется алгоритм быстрой сортировки
           - Работает с целыми числами
        """
        messagebox.showinfo("Справка", help_text)

    #обновление отображения массивов
    def update_display(self):
        self.original_text.delete(1.0, tk.END)
        self.sorted_text.delete(1.0, tk.END)

        if self.original_array:
            self.original_text.insert(1.0, str(self.original_array))

        if self.sorted_array:
            self.sorted_text.insert(1.0, str(self.sorted_array))


    # сохранение массива в бд
    def save_array(self):
            if not self.current_user:
                messagebox.showwarning("Предупреждение", "Сначала авторизуйтесь")
                return

            if not self.original_array:
                messagebox.showwarning("Предупреждение", "Нет исходного массива для сохранения")
                return

            success, message = db_manager.save_array(
                self.current_user['id'],
                self.original_array,
                self.sorted_array
            )

            if success:
                if self.sorted_array:
                    messagebox.showinfo("Результат", "Оба массива сохранены")
                    self.status_var.set("Оба массива сохранены")
                else:
                    messagebox.showinfo("Результат", "Исходный массив сохранен")
                    self.status_var.set("Исходный массив сохранен")
            else:
                messagebox.showerror("Ошибка", message)


    #показ сохраненные массивы
    def show_saved_arrays(self):
        if not self.current_user:
            return

        success, result = db_manager.get_user_arrays(self.current_user['id'])

        if not success:
            messagebox.showerror("Ошибка", result)
            return

        arrays = result

        # создаем новое окно для отображения массивов
        arrays_window = tk.Toplevel(self.root)
        arrays_window.title("Мои сохраненные массивы")
        arrays_window.geometry("800x400")

        # создаем таблицу
        tree = ttk.Treeview(arrays_window, columns=('id', 'original', 'sorted'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('original', text='Исходный массив')
        tree.heading('sorted', text='Отсортированный массив')

        tree.column('id', width=50)
        tree.column('original', width=350)
        tree.column('sorted', width=350)

        # заполняем таблицу данными
        for arr in arrays:
            tree.insert('', 'end', values=(
                arr['id'],
                str(arr['original_array']),
                str(arr['sorted_array'])
            ))

        tree.pack(fill='both', expand=True, padx=10, pady=10)

def main():
    root = tk.Tk()
    SortingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()