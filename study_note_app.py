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

# =========================
# ノート機能の処理部分
# =========================

import os

# ノートの保存先ファイル
NOTE_FILE = "notes.txt"


def save_note():
    """ノートを保存（同名タイトルがあれば上書き）"""
    title = title_entry.get().strip()
    body = body_text.get("1.0", tk.END).strip()

    if not title or not body:
        print("タイトルと本文の両方を入力してください。")
        return

    notes = []
    if os.path.exists(NOTE_FILE):
        with open(NOTE_FILE, "r", encoding="utf-8") as f:
            notes = f.read().split("---\n")

    # 既存タイトルを探して上書き or 新規追加
    new_content = f"{title}\n{body}\n"
    updated = False
    for i in range(len(notes)):
        parts = notes[i].strip().split("\n", 1)
        if parts and parts[0] == title:
            notes[i] = new_content
            updated = True
            break

    if not updated:
        notes.append(new_content)

    # 保存（リストを---で結合）
    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        f.write("---\n".join([n.strip() for n in notes if n.strip()]) + "\n---\n")

    print(f"ノート「{title}」を保存しました。")
    load_notes()
    title_entry.delete(0, tk.END)
    body_text.delete("1.0", tk.END)


def delete_note():
    """選択したノートのみ削除"""
    selection = note_listbox.curselection()
    if not selection:
        print("削除するノートを選択してください。")
        return

    title_to_delete = note_listbox.get(selection[0])
    if not os.path.exists(NOTE_FILE):
        return

    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        notes = f.read().split("---\n")

    # 該当タイトル以外を残す
    remaining = []
    for note in notes:
        parts = note.strip().split("\n", 1)
        if parts and parts[0] != title_to_delete:
            remaining.append(note.strip())

    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        if remaining:
            f.write("---\n".join(remaining) + "\n---\n")
        else:
            f.truncate(0)  # 全削除

    print(f"ノート「{title_to_delete}」を削除しました。")

    load_notes()
    title_entry.delete(0, tk.END)
    body_text.delete("1.0", tk.END)


# ボタン設定の変更
save_button.config(command=save_note)
delete_button.config(command=delete_note)


def load_notes():
    """ファイルからノートのタイトルだけを一覧に表示"""
    note_listbox.delete(0, tk.END)
    if not os.path.exists(NOTE_FILE):
        return

    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        lines = f.read().split("---\n")
        for note in lines:
            parts = note.strip().split("\n", 1)
            if parts and parts[0]:
                note_listbox.insert(tk.END, parts[0])


def delete_notes():
    """ノートファイルを空にする（全削除）"""
    if os.path.exists(NOTE_FILE):
        open(NOTE_FILE, "w").close()
        print("すべてのノートを削除しました。")
    note_listbox.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    body_text.delete("1.0", tk.END)


# 各ボタンに機能を紐づけ
save_button.config(command=save_note)
delete_button.config(command=delete_note)

# 起動時に既存ノートを読み込み
load_notes()

# =========================
# ノートの選択・編集機能
# =========================


def on_select(event):
    """リストで選択されたノートを本文エリアに表示"""
    if not os.path.exists(NOTE_FILE):
        return

    # 選択されたインデックスを取得
    selection = note_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    title = note_listbox.get(index)

    # ファイルを読み込み、該当タイトルの本文を検索
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        notes = f.read().split("---\n")
        for note in notes:
            parts = note.strip().split("\n", 1)
            if len(parts) >= 2 and parts[0] == title:
                title_entry.delete(0, tk.END)
                title_entry.insert(0, parts[0])
                body_text.delete("1.0", tk.END)
                body_text.insert("1.0", parts[1])
                break


def new_note():
    """入力欄を空にして新しいノートを作成する準備"""
    title_entry.delete(0, tk.END)
    body_text.delete("1.0", tk.END)


# Listboxの選択イベントに関数を紐づけ
note_listbox.bind("<<ListboxSelect>>", on_select)

# 新規ボタンに機能を追加
new_button.config(command=new_note)

# メインループ開始
root.mainloop()
