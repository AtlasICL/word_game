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


class true_false_label:
    val = ""
    def __init__(self):
        val = "Attempt"
    def update_correct(self):
        self.val = "CORRECT"
    def update_false(self):
        self.val = "FALSE"

class score:
    correctlyGuessedWords = 0
    totalGuessedWords = 0
    def __init__(self):
        self.correctlyGuessedWords = 0
        self.totalGuessedWords = 0
    def addCorrectGuess(self):
        self.correctlyGuessedWords += 1
        self.totalGuessedWords += 1
    def addIncorrectGuess(self):
        self.totalGuessedWords += 1
    def getCorrectGuesses(self) -> int:
        return self.correctlyGuessedWords
    def getTotalGuesses(self) -> int:
        return self.totalGuessedWords


correctWord = cWord()
hiddenWord = hWord()
scoreCounter = score()

tflbl = true_false_label()

lbl = ctk.StringVar(master=root, value=hiddenWord.word)
true_false_lbl = ctk.StringVar(master=root, value=tflbl.val)
scoreLabelText = ctk.StringVar(master=root,
                               value=str(scoreCounter.getCorrectGuesses())+'/'+str(scoreCounter.getTotalGuesses()))

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, height=20, textvariable=lbl, font=ctk.CTkFont(size=20, weight="bold"))
label.pack(pady=20, padx=10)

entry_box = ctk.CTkEntry(master=frame, placeholder_text="")
entry_box.pack(pady=8, padx=10)

def check_guess_attempt(argu='in'):
    if lev.distance(entry_box.get(), correctWord.word) <= int(drop.get()):
        print("CORRECT")
        correctWord.update()
        hiddenWord.update()
        lbl.set(str(hiddenWord.word))
        true_false_lbl.set("CORRECT")
        entry_box.delete(0, len(entry_box.get()))
        scoreCounter.addCorrectGuess()
        scoreLabelText.set(str(scoreCounter.getCorrectGuesses())+'/'+str(scoreCounter.getTotalGuesses()))
    else:
        print("FALSE")
        true_false_lbl.set("FALSE")
        # scoreCounter.addIncorrectGuess()
        # scoreLabelText.set(str(scoreCounter.getCorrectGuesses())+'/'+str(scoreCounter.getTotalGuesses()))

def skip_word():
    print("SKIPPING WORD")
    correctWord.update()
    hiddenWord.update()
    lbl.set(str(hiddenWord.word))
    true_false_lbl.set("SKIPPED")
    scoreCounter.addIncorrectGuess()
    scoreLabelText.set(str(scoreCounter.getCorrectGuesses())+'/'+str(scoreCounter.getTotalGuesses()))
    entry_box.delete(0, len(entry_box.get()))


submitGuessButton = ctk.CTkButton(master=frame, text="Guess", command=check_guess_attempt, fg_color="green")
submitGuessButton.pack(pady=8, padx=10)

skipWordButton = ctk.CTkButton(master=frame, text="Skip", command=skip_word)
skipWordButton.pack(pady=8, padx=10)

feedback_label = ctk.CTkLabel(master=frame, height=20, width=100, textvariable=true_false_lbl)
feedback_label.pack(pady=8, padx=10)

DeviationAllowedMenuTitle = ctk.CTkLabel(master=frame, height=20, text="Deviation allowed:")
DeviationAllowedMenuTitle.pack(pady=8, padx=10)

drop = ctk.CTkOptionMenu(master=frame, values=["0", "1", "2"], fg_color="gray", button_color="gray") 
drop.pack()

root.bind('<Return>', submitGuessButton._command)

scoreLabel = ctk.CTkLabel(master=frame, height=14, textvariable=scoreLabelText, font=ctk.CTkFont(size=14, weight="bold"))
scoreLabel.pack(pady=20, padx=10)

def main():
    root.mainloop()

if __name__== "__main__":
    main()  