import tkinter as tk

BOARD_SIZE = 19
CELL_SIZE = 30
STONE_RADIUS = 12
OFFSET = 15


class RenjuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Рендзю")

        self.win_count = 5

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.canvas = tk.Canvas(self.main_frame, width=BOARD_SIZE * CELL_SIZE,
                                height=BOARD_SIZE * CELL_SIZE, bg="bisque")
        self.canvas.pack(side=tk.LEFT)

        self.right_panel = tk.Frame(self.main_frame, width=200)
        self.right_panel.pack(side=tk.RIGHT, padx=10)

        self.status_label = tk.Label(self.right_panel, text="Хід: Чорний", font=("Arial", 12), width=20,
                                     anchor="center", justify="center")
        self.status_label.pack(pady=10)

        self.result_label = tk.Label(self.right_panel, text="", font=("Arial", 12), fg="green", width=20, height=4,
                                     anchor="center", justify="center")
        self.result_label.pack(pady=10)

        self.win_count_label = tk.Label(self.right_panel, text="Кількість камінців для перемоги:", font=("Arial", 10))
        self.win_count_label.pack(pady=(20, 5))

        self.win_count_var = tk.IntVar(value=self.win_count)
        self.win_count_spinbox = tk.Spinbox(self.right_panel, from_=3, to=10, textvariable=self.win_count_var,
                                            width=5, font=("Arial", 10), justify="center")
        self.win_count_spinbox.pack()

        self.reset_button = tk.Button(self.right_panel, text="Очистити", command=self.reset_board, width=20)
        self.reset_button.pack(pady=20)

        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 1
        self.game_over = False
        self.game_started = False

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            x = CELL_SIZE + i * CELL_SIZE - OFFSET
            y = CELL_SIZE + i * CELL_SIZE - OFFSET
            self.canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                                    CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE)
            self.canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                                    CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE)
            self.canvas.create_text(CELL_SIZE // 2 - 8, y, text=str(i + 1), font=("Arial", 9))
            self.canvas.create_text(x, CELL_SIZE // 2 - 8, text=str(i + 1), font=("Arial", 9))

    def handle_click(self, event):
        if self.game_over:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.board[row][col] == 0:
                if not self.game_started:
                    self.game_started = True
                    self.hide_win_count_selection()

                self.board[row][col] = self.turn
                self.draw_stone(row, col, self.turn)
                self.win_count = self.win_count_var.get()
                win_pos = self.check_win(self.turn, self.win_count)
                if win_pos:
                    r, c, direction = win_pos
                    self.result_label.config(
                        text=f"Перемога: {'Чорний' if self.turn == 1 else 'Білий'}\n"
                             f"Коорд: {r + 1}, {c + 1}\n"
                             f"Напрям: {direction}")
                    self.status_label.config(text="Гру завершено")
                    self.game_over = True
                    self.canvas.unbind("<Button-1>")
                else:
                    self.turn = 3 - self.turn
                    self.status_label.config(text=f"Хід: {'Чорний' if self.turn == 1 else 'Білий'}")

    def hide_win_count_selection(self):
        self.win_count_label.pack_forget()
        self.win_count_spinbox.pack_forget()

    def draw_stone(self, row, col, color):
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        fill = "black" if color == 1 else "white"
        self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                x + STONE_RADIUS, y + STONE_RADIUS, fill=fill, outline="black")

    def check_win(self, color, win_count):
        directions = {
            (0, 1): "горизонталь",
            (1, 0): "вертикаль",
            (1, 1): "діагональ \\",
            (1, -1): "діагональ /"
        }
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == color:
                    for dx, dy in directions:
                        result = self.is_winning_sequence(row, col, dx, dy, color, win_count)
                        if result:
                            _, r, c = result[:3]
                            direction = directions[(dx, dy)]
                            return r, c, direction
        return None

    def is_valid(self, row, col, color):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == color

    def is_winning_sequence(self, row, col, dx, dy, color, win_count):
        positions = [(row, col)]

        def collect_stones(r, c, step_x, step_y):
            stones = []
            for _ in range(win_count - 1):
                r += step_x
                c += step_y
                if self.is_valid(r, c, color):
                    stones.append((r, c))
                else:
                    break
            return stones

        positions += collect_stones(row, col, dx, dy)
        positions += collect_stones(row, col, -dx, -dy)

        if len(positions) == win_count:
            before = (row - dx, col - dy)
            after = (row + dx * win_count, col + dy * win_count)
            if not self.is_valid(*before, color) and not self.is_valid(*after, color):
                if dx == 1 and dy == 0:
                    stone = min(positions, key=lambda x: x[0])
                else:
                    stone = min(positions, key=lambda x: x[1])
                return True, stone[0], stone[1]
        return False

    def reset_board(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.canvas.delete("all")
        self.draw_grid()
        self.turn = 1
        self.game_over = False
        self.canvas.bind("<Button-1>", self.handle_click)
        self.game_started = False
        self.status_label.config(text="Хід: Чорний")
        self.result_label.config(text="")
        self.win_count_label.pack(pady=(20, 5))
        self.win_count_spinbox.pack()
        self.win_count_var.set(5)


if __name__ == "__main__":
    root = tk.Tk()
    game = RenjuGUI(root)
    root.mainloop()
