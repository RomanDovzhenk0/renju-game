import tkinter as tk

BOARD_SIZE = 19
CELL_SIZE = 30
STONE_RADIUS = 12


class RenjuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Renju")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.canvas = tk.Canvas(self.main_frame, width=BOARD_SIZE * CELL_SIZE,
                                height=BOARD_SIZE * CELL_SIZE, bg="bisque")
        self.canvas.pack(side=tk.LEFT)

        self.right_panel = tk.Frame(self.main_frame, width=150)
        self.right_panel.pack(side=tk.RIGHT, padx=10)

        self.status_label = tk.Label(self.right_panel, text="Хід: Чорний", font=("Arial", 12), width=20,
                                     anchor="center", justify="center")
        self.status_label.pack(pady=10)

        self.result_label = tk.Label(self.right_panel, text="", font=("Arial", 12), fg="green", width=20, height=4,
                                     anchor="center", justify="center")
        self.result_label.pack(pady=10)

        self.reset_button = tk.Button(self.right_panel, text="Очистити", command=self.reset_board, width=20)
        self.reset_button.pack(pady=20)

        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 1
        self.game_over = False

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            x = CELL_SIZE + i * CELL_SIZE - 15
            y = CELL_SIZE + i * CELL_SIZE - 15
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
                self.board[row][col] = self.turn
                self.draw_stone(row, col, self.turn)
                win_pos = self.check_win(self.turn)
                if win_pos:
                    self.result_label.config(
                        text=f"Перемога: {'Чорний' if self.turn == 1 else 'Білий'}\nКоорд: {win_pos[0] + 1}, {win_pos[1] + 1}")
                    self.status_label.config(text="Гру завершено")
                    self.game_over = True
                else:
                    self.turn = 3 - self.turn
                    self.status_label.config(text=f"Хід: {'Чорний' if self.turn == 1 else 'Білий'}")

    def draw_stone(self, row, col, color):
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        fill = "black" if color == 1 else "white"
        self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                x + STONE_RADIUS, y + STONE_RADIUS, fill=fill, outline="black")

    def check_win(self, color):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == color:
                    for dx, dy in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if self.is_five(row, col, dx, dy, color):
                            return row, col
        return None

    def is_five(self, row, col, dx, dy, color):
        count = 1
        r, c = row, col
        for _ in range(4):
            r += dx
            c += dy
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == color:
                count += 1
            else:
                break
        r, c = row - dx, col - dy
        for _ in range(4):
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == color:
                count += 1
                r -= dx
                c -= dy
            else:
                break
        if count == 5:
            before_r = row - dx
            before_c = col - dy
            after_r = row + dx * 5
            after_c = col + dy * 5
            return not (
                    (0 <= before_r < BOARD_SIZE and 0 <= before_c < BOARD_SIZE and self.board[before_r][
                        before_c] == color)
                    or
                    (0 <= after_r < BOARD_SIZE and 0 <= after_c < BOARD_SIZE and self.board[after_r][after_c] == color)
            )
        return False

    def reset_board(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.canvas.delete("all")
        self.draw_grid()
        self.turn = 1
        self.game_over = False
        self.status_label.config(text="Хід: Чорний")
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    game = RenjuGUI(root)
    root.mainloop()
