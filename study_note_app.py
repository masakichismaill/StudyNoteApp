import tkinter as tk

# メインウィンドウを作成
root = tk.Tk()
root.title("学習ノート")
root.geometry("800x500")  # 幅x高さ

# =========================
# 左側：ノート一覧エリア
# =========================
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.pack(side="left", fill="y")

# ノート一覧ラベル
list_label = tk.Label(left_frame, text="ノート一覧")
list_label.pack(anchor="w")

# Listbox（ノートタイトルを表示する予定）
note_listbox = tk.Listbox(left_frame, width=25, height=20)
note_listbox.pack(side="left", fill="y")

# スクロールバー
scrollbar = tk.Scrollbar(left_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Listbox と スクロールバーを連動
note_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=note_listbox.yview)

# =========================
# 右側：ノート編集エリア
# =========================
right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.pack(side="right", fill="both", expand=True)

# タイトルラベル
title_label = tk.Label(right_frame, text="タイトル")
title_label.pack(anchor="w")

# タイトル入力欄
title_entry = tk.Entry(right_frame)
title_entry.pack(fill="x")

# 本文ラベル
body_label = tk.Label(right_frame, text="本文")
body_label.pack(anchor="w", pady=(10, 0))

# 本文テキストエリア
body_text = tk.Text(right_frame, wrap="word")
body_text.pack(fill="both", expand=True)

# =========================
# ボタンエリア
# =========================
button_frame = tk.Frame(right_frame, pady=10)
button_frame.pack(fill="x")

new_button = tk.Button(button_frame, text="新規")
save_button = tk.Button(button_frame, text="保存")
delete_button = tk.Button(button_frame, text="削除")

new_button.pack(side="left", padx=5)
save_button.pack(side="left", padx=5)
delete_button.pack(side="left", padx=5)

# メインループ開始
root.mainloop()
