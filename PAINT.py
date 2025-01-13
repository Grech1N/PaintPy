import tkinter as tk
from tkinter import colorchooser

# Класс для точки
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, color, thickness):
        canvas.create_oval(self.x - 2, self.y - 2, self.x + 2, self.y + 2, fill=color, outline=color, width=thickness)

# Класс для линии
class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas, color, thickness):
        canvas.create_line(
            self.start_point.x, self.start_point.y,
            self.end_point.x, self.end_point.y,
            fill=color, width=thickness
        )

# Основной класс приложения
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Список для хранения всех фигур
        self.shapes = []

        # Переменные для хранения точек начала и конца линии
        self.start_point = None
        self.end_point = None

        # Переменные для свободного рисования
        self.drawing = False
        self.last_x, self.last_y = None, None

        # Настройки по умолчанию
        self.current_color = "black"
        self.current_thickness = 2

        # Панель инструментов
        self.toolbar = tk.Frame(root, bg="lightgray")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки
        self.button_line_mode = tk.Button(self.toolbar, text="Режим: Линия", command=self.set_line_mode)
        self.button_line_mode.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_free_draw = tk.Button(self.toolbar, text="Режим: Рисование", command=self.set_free_draw_mode)
        self.button_free_draw.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_clear = tk.Button(self.toolbar, text="Очистить холст", command=self.clear_canvas)
        self.button_clear.pack(side=tk.LEFT, padx=5, pady=5)

        # Выбор цвета
        self.button_color = tk.Button(self.toolbar, text="Выбрать цвет", command=self.choose_color)
        self.button_color.pack(side=tk.LEFT, padx=5, pady=5)

        # Выбор толщины линии
        self.label_thickness = tk.Label(self.toolbar, text="Толщина линии:")
        self.label_thickness.pack(side=tk.LEFT, padx=5, pady=5)

        self.thickness_var = tk.IntVar(value=self.current_thickness)
        self.thickness_menu = tk.OptionMenu(self.toolbar, self.thickness_var, 1, 2, 3, 4, 5, 10, command=self.set_thickness)
        self.thickness_menu.pack(side=tk.LEFT, padx=5, pady=5)

        # Привязка событий мыши
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Режим по умолчанию
        self.mode = "line"  # Режим рисования линии

    # Установка режима рисования линии
    def set_line_mode(self):
        self.mode = "line"

    # Установка режима свободного рисования
    def set_free_draw_mode(self):
        self.mode = "free"

    # Выбор цвета
    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    # Установка толщины линии
    def set_thickness(self, value):
        self.current_thickness = int(value)

    # Обработчик клика мыши
    def on_mouse_click(self, event):
        if self.mode == "line":
            if self.start_point is None:
                self.start_point = Point(event.x, event.y)
                self.start_point.draw(self.canvas, self.current_color, self.current_thickness)
            else:
                self.end_point = Point(event.x, event.y)
                line = Line(self.start_point, self.end_point)
                line.draw(self.canvas, self.current_color, self.current_thickness)
                self.shapes.append(line)
                self.start_point = None
                self.end_point = None
        elif self.mode == "free":
            self.drawing = True
            self.last_x, self.last_y = event.x, event.y

    # Обработчик движения мыши с зажатой кнопкой
    def on_mouse_drag(self, event):
        if self.mode == "free" and self.drawing:
            if self.last_x and self.last_y:
                self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    fill=self.current_color, width=self.current_thickness
                )
            self.last_x, self.last_y = event.x, event.y

    # Обработчик отпускания кнопки мыши
    def on_mouse_release(self, event):
        if self.mode == "free":
            self.drawing = False
            self.last_x, self.last_y = None, None

    # Метод для очистки холста
    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()
        self.start_point = None
        self.end_point = None

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()