import tkinter as tk
from tkinter import messagebox
from collections import Counter

# Частоты букв английского языка
english_letter_freq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
    'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'X': 0.15, 'J': 0.10, 'Q': 0.10, 'Z': 0.07
}

# Функция шифрования Цезаря
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

# Функция для оценки "правдоподобности" расшифрованного текста
def score_text(text):
    text = text.upper()
    letter_count = Counter(filter(str.isalpha, text))
    total_letters = sum(letter_count.values())

    if total_letters == 0:
        return float('inf')

    score = 0
    for letter, count in letter_count.items():
        letter_frequency = (count / total_letters) * 100
        if letter in english_letter_freq:
            score += abs(english_letter_freq[letter] - letter_frequency)

    return score

# Функция для взлома шифра Цезаря с частотным анализом
def caesar_break_smart(text):
    best_shift = 0
    best_score = float('inf')
    best_decryption = ""

    for shift in range(1, 26):
        decrypted_text = caesar_cipher(text, -shift)
        score = score_text(decrypted_text)
        if score < best_score:
            best_score = score
            best_shift = shift
            best_decryption = decrypted_text

    return best_decryption, best_shift

# Обработчики событий UI
def encrypt_text():
    text = input_text.get("1.0", tk.END).strip()
    shift = shift_value.get()
    if not text:
        messagebox.showwarning("Ошибка", "Введите текст для шифрования.")
        return
    encrypted = caesar_cipher(text, shift)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", encrypted)

def decrypt_text():
    text = input_text.get("1.0", tk.END).strip()
    shift = shift_value.get()
    if not text:
        messagebox.showwarning("Ошибка", "Введите текст для расшифровки.")
        return
    decrypted = caesar_cipher(text, -shift)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", decrypted)

def break_cipher():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Ошибка", "Введите зашифрованный текст для взлома.")
        return
    decrypted_text, shift = caesar_break_smart(text)
    messagebox.showinfo("Результат взлома", f"Предполагаемый сдвиг: {shift}\nРасшифрованный текст: {decrypted_text}")
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", decrypted_text)

# Копирование текста в буфер обмена
def copy_to_clipboard(widget):
    text = widget.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

# Создание UI
root = tk.Tk()
root.title("Шифр Цезаря")
root.geometry("500x400")

# Поля ввода
frame1 = tk.Frame(root)
frame1.pack()

label1 = tk.Label(frame1, text="Введите текст:")
label1.pack(side=tk.LEFT)
copy_button1 = tk.Button(frame1, text="Копировать", command=lambda: copy_to_clipboard(input_text))
copy_button1.pack(side=tk.RIGHT)

input_text = tk.Text(root, height=5)
input_text.pack()

shift_frame = tk.Frame(root)
shift_frame.pack()

shift_label = tk.Label(shift_frame, text="Сдвиг шифра:")
shift_label.pack(side=tk.LEFT)

shift_value = tk.IntVar(value=3)
shift_entry = tk.Spinbox(shift_frame, from_=0, to=25, textvariable=shift_value)
shift_entry.pack(side=tk.RIGHT)

# Кнопки управления
encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_text)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Расшифровать", command=decrypt_text)
decrypt_button.pack()

break_button = tk.Button(root, text="Умный взлом", command=break_cipher)
break_button.pack()

# Поле вывода
frame2 = tk.Frame(root)
frame2.pack()

label2 = tk.Label(frame2, text="Результат:")
label2.pack(side=tk.LEFT)
copy_button2 = tk.Button(frame2, text="Копировать", command=lambda: copy_to_clipboard(output_text))
copy_button2.pack(side=tk.RIGHT)

output_text = tk.Text(root, height=5)
output_text.pack()

root.mainloop()
