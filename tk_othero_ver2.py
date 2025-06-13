import tkinter as tk
from functools import partial
import tkinter.messagebox as messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.initialize_game()

    def initialize_game(self):
        "ゲームの状態を初期化する"
        self.player = 0  # 0: 黒, 1: 白
        self.white_count = 2
        self.black_count = 2
        self.game_over = False #ゲーム終了フラグ

        # create_widgetsが完了していることを確認してから盤面を操作
        if hasattr(self, 'buttons'):
            # 盤面をリセット
            for x in range(8):
                for y in range(8):
                    self.buttons[x][y]["text"] = ""
            
            # 初期配置
            self.buttons[3][3]["text"] = "●"
            self.buttons[3][4]["text"] = "○"
            self.buttons[4][3]["text"] = "○"
            self.buttons[4][4]["text"] = "●"

            self.update_turn_label()
            self.update_count_labels()
            self.highlight_valid_moves()

    def create_widgets(self):
        "ウィジェットを作成し、配置する"
        # 盤面作成
        self.buttons = []
        for x in range(8):
            yButtons = []
            for y in range(8):
                button = tk.Button(
                                   height=2,
                                   width=5,
                                   font=("", 14),
                                   bg="#008000", # 盤面を緑色に
                                   activebackground="#90EE90",
                                   compound="center")
                button["command"] = partial(self.click, x, y)
                button.place(x=20 + x * 60, y=20 + y * 60)
                yButtons.append(button)
            self.buttons.append(yButtons)
        
        # ラベルとボタンの配置用フレーム
        info_frame = tk.Frame(self.master)
        info_frame.place(x=520, y=100, width=260, height=400)

        # ターン表示ラベル
        self.turn_label = tk.Label(info_frame, text="黒のターンです。", font=("", 16))
        self.turn_label.pack(pady=20)

        # 石の数表示ラベル
        self.blacknum_label = tk.Label(info_frame, text="黒 2個", font=("", 14))
        self.blacknum_label.pack(pady=5)
        self.whitenum_label = tk.Label(info_frame, text="白 2個", font=("", 14))
        self.whitenum_label.pack(pady=5)

        # リセットボタン
        self.reset_button = tk.Button(info_frame, text="リセット", command=self.reset_game, font=("", 14))
        self.reset_button.pack(pady=40)


    def click(self, x, y):
        "盤面がクリックされたときの処理"
        #ゲーム終了後は操作を無効化
        if self.game_over:
            return

        valid_moves = self.get_valid_moves()
        if (x, y) not in valid_moves:
            return

        # 石を置く処理と裏返す処理
        self.place_and_flip(x, y)
        self.change_turn()


    def place_and_flip(self, x, y):
        "指定された位置に石を置き、対応する石を裏返す"
        if self.player == 0:
            myMark, othMark = ("●", "○")
        else:
            myMark, othMark = ("○", "●")
        
        self.buttons[x][y]["text"] = myMark

        # 8方向に対して石を裏返す
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            self.flip_stones_in_direction(x, y, dx, dy, myMark, othMark)

    def flip_stones_in_direction(self, x, y, dx, dy, myMark, othMark):
        "一方向に対して石を裏返す"
        stones_to_flip = []
        cx, cy = x + dx, y + dy

        while 0 <= cx < 8 and 0 <= cy < 8:
            if self.buttons[cx][cy]["text"] == othMark:
                stones_to_flip.append((cx, cy))
            elif self.buttons[cx][cy]["text"] == myMark:
                for fx, fy in stones_to_flip:
                    self.buttons[fx][fy]["text"] = myMark
                break
            else: # 空白の場合
                break
            cx, cy = cx + dx, cy + dy

    def change_turn(self):
        "ターンを交代し、ゲームの状態を更新する"
        self.clear_highlights()
        self.count_stones()

        # 盤面が埋まったらゲーム終了
        if self.white_count + self.black_count == 64:
            self.judge()
            return
        
        # 相手のターンへ
        self.player = 1 - self.player
        opponent_moves = self.get_valid_moves()

        if opponent_moves:
            # 相手が通常通り石を置ける場合
            self.update_turn_label()
            self.highlight_valid_moves()
        else:
            # 相手がパスする場合
            self.update_turn_label() # 「（相手）のターンです」と一度表示
            messagebox.showinfo("パス", f"{'白' if self.player == 0 else '黒'}は置ける場所がないため、パスします。")
            
            # 再び自分のターンへ
            self.player = 1 - self.player
            my_moves = self.get_valid_moves()

            if my_moves:
                # 自分は石を置ける場合
                self.update_turn_label()
                self.highlight_valid_moves()
            else:
                # 自分も相手も置けない場合（ゲーム終了）
                self.update_turn_label()
                messagebox.showinfo("ゲーム終了", "両者とも置ける場所がありません。")
                self.judge()


    def get_valid_moves(self):
        "現在のプレイヤーが石を置ける全てのマスを返す"
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def is_valid_move(self, x, y):
        "指定されたマスに石を置けるかどうかを判定する"
        if self.buttons[x][y]["text"] != "":
            return False

        if self.player == 0:
            myMark, othMark = ("●", "○")
        else:
            myMark, othMark = ("○", "●")
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            cx, cy = x + dx, y + dy
            if 0 <= cx < 8 and 0 <= cy < 8 and self.buttons[cx][cy]["text"] == othMark:
                cx, cy = cx + dx, cy + dy
                while 0 <= cx < 8 and 0 <= cy < 8:
                    if self.buttons[cx][cy]["text"] == myMark:
                        return True
                    if self.buttons[cx][cy]["text"] == "":
                        break
                    cx, cy = cx + dx, cy + dy
        return False
            
    def highlight_valid_moves(self):
        "置ける場所をハイライトする"
        valid_moves = self.get_valid_moves()
        for x, y in valid_moves:
            self.buttons[x][y].config(bg="#FFFF00")

    def clear_highlights(self):
        "ハイライトをすべて解除する"
        for x in range(8):
            for y in range(8):
                self.buttons[x][y].config(bg="#008000")
    
    def count_stones(self):
        "盤上の石の数を数える"
        self.white_count = 0
        self.black_count = 0
        for row in self.buttons:
            for button in row:
                if button["text"] == "○":
                    self.white_count += 1
                elif button["text"] == "●":
                    self.black_count += 1
        self.update_count_labels()
    
    def update_count_labels(self):
        "石の数の表示ラベルを更新"
        self.blacknum_label["text"] = f"黒 {self.black_count}個"
        self.whitenum_label["text"] = f"白 {self.white_count}個"

    def update_turn_label(self):
        "ターン表示ラベルを更新"
        if self.player == 0:
            turn_text = "黒のターンです。"
        else:
            turn_text = "白のターンです。"
        self.turn_label["text"] = turn_text
    
    def judge(self):
        "勝敗を判定し、結果を表示する"
        if self.game_over: 
            return # 既に判定済みの場合は何もしない

        #ゲーム終了フラグを立てる
        self.game_over = True
        self.clear_highlights()
        
        result_text = ""
        if self.white_count < self.black_count:
            result_text = f"黒の勝ちです"
        elif self.white_count > self.black_count:
            result_text = f"白の勝ちです"
        else:
            result_text = f"引き分けです"
        
        self.turn_label["text"] = "ゲーム終了"
        messagebox.showinfo("ゲーム終了", result_text)
        
    def reset_game(self):
        "ゲームをリセットして初期状態に戻す"
        self.clear_highlights()
        self.initialize_game()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("オセロ")
    root.geometry("800x550")
    app = Application(master=root)
    app.mainloop()