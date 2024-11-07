import tkinter as tk
import random
from hashlib import md5
import tkinter.messagebox as messagebox

class BingoCard:
    def __init__(self, root):
        self.root = root
        self.root.title("BingoCard")
        self.grid_size = 5
        self.card_hashes = set()
        self.card_numbers = []
        self.card_history = []
        self.selected = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.card_label = tk.Frame(self.root, padx=10, pady=10, bg="lightgray")
        self.card_label.grid(row=0, column=0, sticky="ew")
        self.card = tk.Frame(self.root, padx=10, pady=10, bg="lightgray")
        self.card.grid(row=1, column=0)
        self.card_buttons = tk.Frame(self.root, bg="lightgray")
        self.card_buttons.grid(row=2, column=0, sticky="ew")
        self.empty_card()
        self.create_buttons()
    
    #画面上部を作成するメソッド
    def create_card_label(self):
        self.card_number_label = tk.Label(self.card_label, text="カード番号", font=("Arial", 14, "bold"), bg="lightgray")
        self.card_number_label.pack()
    
    #空のビンゴカードを作成するメソッド
    def empty_card(self):
        #ウィジェットをすべて削除
        for widget in self.card.winfo_children():
            widget.destroy()
        #カードの上部を作成
        self.create_card_label()

        #グリッドに合わせてBINGOと表示
        for i, text in enumerate("BINGO"):
            bingo_label = tk.Label(self.card, text=text, font=("Arial", 20, "bold"), bg="lightgray")
            bingo_label.grid(row=0, column=i, padx=5, pady=5)

        self.buttons = []

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                #中央のボタンはFREEにする
                if(i == 2 and j == 2):
                    button = tk.Button(self.card, text="FREE", width=5, height=2, state="disabled", highlightbackground="lightblue", highlightthickness=2)
                else:
                    button = tk.Button(self.card, text="", width=5, height=2, state="disabled", command=lambda x=i, y=j: self.select_number(x, y))
                button.grid(row=i+1, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)
    #カードを生成
    def create_card(self):
        columns = [range(1, 16), range(16, 31), range(31, 46), range(46, 61), range(61, 76)]
        while True:
            card = []
            for i in range(self.grid_size):
                column_number = random.sample(columns[i], self.grid_size)
                card.append(column_number)
            card[2][2] = "FREE"
            self.card_hash = md5(str(card).encode()).hexdigest()
            if self.card_hash not in self.card_hashes:
                self.card_hashes.add(self.card_hash)
                print("ハッシュ値", self.card_hash)
                return card
    
    def display_card(self):
        self.card_number_label.config(text=f"カード番号:{len(self.card_history)}")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                num = self.card_numbers[i][j]
                btn_text = str(num) if num != "FREE" else "FREE"
                self.buttons[i][j].config(text=btn_text, state="normal")
        self.buttons[2][2].config(state="disabled")

    #カードの操作をするボタンを作成
    def create_buttons(self):
        #前のカードに戻るボタンを作成
        back_button = tk.Button(self.card_buttons, text="←", command=self.back_card)
        back_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        #カードを生成するボタンを作成
        generate_button = tk.Button(self.card_buttons, text="⚪︎", command=self.generate_card)
        generate_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        #次のカードを生成するボタンを作成
        next_button = tk.Button(self.card_buttons, text="→", command=self.next_card)
        next_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    #generate_buttonが押されたときのメソッド
    def generate_card(self):
        self.card_numbers = self.create_card()
        self.card_history.append(self.card_numbers)
        self.reset_buttons()
        self.display_card()
    
    #next_buttonが押された時に呼ばれるメソッド
    def next_card(self):
        self.card_numbers = self.create_card()
        self.card_history.append(self.card_numbers)
        self.reset_buttons()
        self.display_card()

    #back_buttonが押された時に呼ばれるメソッド
    def back_card(self):
        if len(self.card_history) > 1:
            self.card_history.pop()
            self.card_numbers = self.card_history[-1]
            self.display_card()
        else:
            print("前のカードはありません。")
    

    #番号が選択されたときに呼ばれるメソッド
    def select_number(self, x, y):
        if not self.selected[x][y]:
            self.selected[x][y] = True
            self.buttons[x][y].config(highlightbackground="#ffff00", highlightthickness=2)
            self.check_bingo()
        else:
            self.selected[x][y] = False
            self.buttons[x][y].config(highlightbackground="SystemButtonFace", highlightthickness=1)
    
    #ビンゴを判定するメソッド
    def check_bingo(self):
        # ビンゴ判定
        for i in range(self.grid_size):
            if all(self.selected[i]):  
                messagebox.showinfo("結果", "ビンゴ！")  
                return
            if all(self.selected[j][i] for j in range(self.grid_size)): 
                messagebox.showinfo("結果", "ビンゴ！")  
                return
        
        if all(self.selected[i][i] for i in range(self.grid_size)): 
            messagebox.showinfo("結果", "ビンゴ！") 
            return
        if all(self.selected[i][self.grid_size - 1 - i] for i in range(self.grid_size)):  # 右上から左下の対角線
            messagebox.showinfo("結果", "ビンゴ！")  
            return
    
    #カードの選択状況をリセットするメソッド
    def reset_buttons(self):
        self.selected = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.selected[2][2] = True
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i == 2 and j == 2):
                    continue
                self.buttons[i][j].config(highlightbackground="SystemButtonFace", highlightthickness=1, state="disabled")

    


if __name__ == "__main__":
    root = tk.Tk()
    BingoCard(root)
    root.mainloop()