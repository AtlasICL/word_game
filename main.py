import customtkinter as ctk
import Levenshtein as lev

VOWELS = ['a', 'e', 'i', 'o', 'u']

def vowel_stripper(word: str, vowel_list: list[str]):
    out = ""
    for letter in word:
        if letter not in VOWELS:
            out = out + letter
    return out

def blank_vowels(word: str, vowel_list: list[str]):
    out = ""
    for letter in word:
        if letter in VOWELS:
            out += '_'
        else:
            out += letter
    return out

def open_and_read_file(filename: str) -> list[str]:
    List = open(filename).readlines()
    outlist = [word[:-1] for word in List]
    return outlist


folder_path = ctk.filedialog.askopenfilename()

correctWordList = open_and_read_file(folder_path)
hiddenWordList = [vowel_stripper(word, VOWELS) for word in correctWordList]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.geometry("500x400")



class cWord:
    word = ""
    round_no = -1
    def __init__(self):
        self.word = correctWordList[0]
        self.round_no = 0
    def update(self):
        self.round_no += 1
        self.word = correctWordList[self.round_no]

class hWord:
    word = ""
    round_no = 0
    def __init__(self):
        self.word = hiddenWordList[0]
        self.round_no = 0
    def update(self):
        self.round_no += 1
        self.word = hiddenWordList[self.round_no]

class bg_color_var:
    color = ""
    def __init__(self):
        self.color = "white"
    def update_correct(self):
        self.color = "green"
    def update_false(self):
        self.color = "red"

class true_false_label:
    val = ""
    def __init__(self):
        val = "Attempt"
    def update_correct(self):
        self.val = "CORRECT"
    def update_false(self):
        self.val = "FALSE"

cW = cWord()
hW = hWord()

tflbl = true_false_label()

lbl = ctk.StringVar(master=root, value=hW.word)
true_false_lbl = ctk.StringVar(master=root, value=tflbl.val)


frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, height=20, textvariable=lbl, font=ctk.CTkFont(size=20, weight="bold"))
label.pack(pady=20, padx=10)

entry_box = ctk.CTkEntry(master=frame, placeholder_text="")
entry_box.pack(pady=8, padx=10)

def check_guess_attempt(argu='in'):
    if lev.distance(entry_box.get(), cW.word) <= int(drop.get()):
        print("CORRECT")
        cW.update()
        hW.update()
        lbl.set(str(hW.word))
        true_false_lbl.set("CORRECT")
        entry_box.delete(0, len(entry_box.get()))
    else:
        print("FALSE")
        true_false_lbl.set("FALSE")

def skip_word():
    print("SKIPPING WORD")
    cW.update()
    hW.update()
    lbl.set(str(hW.word))
    true_false_lbl.set("SKIPPED")
    entry_box.delete(0, len(entry_box.get()))


submitGuessButton = ctk.CTkButton(master=frame, text="Guess", command=check_guess_attempt, fg_color="green")
submitGuessButton.pack(pady=8, padx=10)

skipWordButton = ctk.CTkButton(master=frame, text="Skip", command=skip_word)
skipWordButton.pack(pady=8, padx=10)

feedback_label = ctk.CTkLabel(master=frame, height=20, width=100, textvariable=true_false_lbl)
feedback_label.pack(pady=8, padx=10)

LDTitle = ctk.CTkLabel(master=frame, height=20, text="Deviation allowed:")
LDTitle.pack(pady=8, padx=10)

drop = ctk.CTkOptionMenu(master=frame, values=["0", "1", "2"], fg_color="gray", button_color="gray") 
drop.pack()

root.bind('<Return>', submitGuessButton._command)

def main():
    root.mainloop()

if __name__== "__main__":
    main()  