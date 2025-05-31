from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES

# Translator object
translator = Translator()

# Initialize main window
root = Tk()
root.title("Language Translator - AI Internship")
root.geometry("600x400")
root.config(bg="#f0f0f0")

# Language options
language_list = list(LANGUAGES.values())

# Function to perform translation
def translate_text():
    try:
        src_lang = src_lang_combo.get()
        dest_lang = dest_lang_combo.get()
        src_lang_key = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(src_lang.lower())]
        dest_lang_key = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest_lang.lower())]

        translated = translator.translate(text_input.get("1.0", END), src=src_lang_key, dest=dest_lang_key)
        text_output.delete("1.0", END)
        text_output.insert(END, translated.text)
    except Exception as e:
        text_output.delete("1.0", END)
        text_output.insert(END, "Error: " + str(e))

# Labels
Label(root, text="Enter Text", font=("Arial", 12, "bold"), bg="#f0f0f0").place(x=30, y=20)
Label(root, text="From Language", font=("Arial", 10), bg="#f0f0f0").place(x=30, y=230)
Label(root, text="To Language", font=("Arial", 10), bg="#f0f0f0").place(x=300, y=230)
Label(root, text="Translated Text", font=("Arial", 12, "bold"), bg="#f0f0f0").place(x=30, y=270)

# Text boxes
text_input = Text(root, height=5, width=65)
text_input.place(x=30, y=50)

text_output = Text(root, height=4, width=65)
text_output.place(x=30, y=300)

# Language dropdowns
src_lang_combo = ttk.Combobox(root, values=language_list, state='readonly')
src_lang_combo.place(x=140, y=230)
src_lang_combo.set("english")

dest_lang_combo = ttk.Combobox(root, values=language_list, state='readonly')
dest_lang_combo.place(x=400, y=230)
dest_lang_combo.set("hindi")

# Translate button
translate_btn = Button(root, text="Translate", command=translate_text, bg="#007acc", fg="white", font=("Arial", 11, "bold"))
translate_btn.place(x=250, y=260)

root.mainloop()
