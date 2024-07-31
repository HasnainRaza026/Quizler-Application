import random
import customtkinter as ctk
import requests
from sys import exit
from Utility.CTkScrollableDropdown import *

API_URL = "https://opentdb.com/api.php"

FG_COLOR = "#242424"
HOVER_COLOR = "lightgray"

QUESTION_START = 1
QUESTION_END = 50

QUESTION_CATEGORY = {
    "Any Category": None,
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32,
}

QUESTION_TYPE = {
    "True / False": "boolean",
    "Multiple Choice": "multiple"
}

QUESTION_DIFFICULTY = {
    "Any Difficulty": None,
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
}

RESPONSE_CODE = {
    0: "Success: Returned results successfully",
    1: "No Results: Could not return results. The API doesn't have enough questions for your query",
    2: "Invalid Parameter: Contains an invalid parameter. Arguements passed in aren't valid",
    3: "Token Not Found: Session Token does not exist",
    4: "Token Empty: Session Token has returned all possible questions for the specified query. Resetting the Token is necessary",
    5: "Rate Limit: Too many requests have occurred. Each IP can only access the API once every 5 seconds"
}


class QuizGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quizler App")
        self.geometry("550x320")

        self.initialize()

    def initialize(self):
        self.option_buttons = []
        self.questions_answers_options = []
        self.question_index = 0
        self.score = 0

        self.frame = ctk.CTkFrame(self, fg_color=FG_COLOR)
        self.frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(
            row=5, column=0, columnspan=2, pady=5, sticky='ew')

        self.question_amount_selection()
        self.question_category_selection()
        self.question_type_selection()
        self.question_difficulty_selection()
        self.make_proceedbutton()

    def question_amount_selection(self):
        self.amount_label = ctk.CTkLabel(self.frame, text="Number of Questions:", font=("Arial", 14, "bold"),
                                         bg_color="transparent")
        self.amount_label.grid(row=0, column=0, padx=15, pady=0)

        self.selected_amount = ctk.IntVar(value=10)

        self.amount_entry = ctk.CTkEntry(
            self.frame, width=220, textvariable=self.selected_amount, justify="center")
        self.amount_entry.grid(row=0, column=1, padx=0, pady=5)

        self.increase_button = ctk.CTkButton(
            self.frame, text="▲", width=30, command=self.increase)
        self.increase_button.grid(row=0, column=1, padx=20, sticky="w")

        self.decrease_button = ctk.CTkButton(
            self.frame, text="▼", width=30, command=self.decrease)
        self.decrease_button.grid(row=0, column=1, padx=20, sticky="e")

    def increase(self):
        current_value = self.selected_amount.get()
        if current_value < QUESTION_END:
            self.selected_amount.set(current_value + 1)

    def decrease(self):
        current_value = self.selected_amount.get()
        if current_value > QUESTION_START:
            self.selected_amount.set(current_value - 1)

    def question_category_selection(self):
        self.category_label = ctk.CTkLabel(self.frame, text="Select Category:", font=("Arial", 14, "bold"),
                                           bg_color="transparent")
        self.category_label.grid(row=1, column=0, padx=15, pady=0)

        options = [keys for keys in QUESTION_CATEGORY]
        self.selected_category = ctk.StringVar(value=options[0])
        self.category_optionmenu = ctk.CTkOptionMenu(
            self.frame, variable=self.selected_category, width=300, anchor="center")
        self.category_optionmenu.grid(row=1, column=1, padx=20, pady=5)
        CTkScrollableDropdown(self.category_optionmenu, values=options)

    def question_type_selection(self):
        self.type_label = ctk.CTkLabel(self.frame, text="Select Type:", font=("Arial", 14, "bold"),
                                       bg_color="transparent")
        self.type_label.grid(row=2, column=0, padx=15, pady=0)

        options = [keys for keys in QUESTION_TYPE]
        self.selected_type = ctk.StringVar(value=options[0])
        self.type_optionmenu = ctk.CTkOptionMenu(
            self.frame, variable=self.selected_type, anchor="center", width=300)
        self.type_optionmenu.grid(row=2, column=1, padx=20, pady=5)
        CTkScrollableDropdown(self.type_optionmenu, values=options)

    def question_difficulty_selection(self):
        self.difficulty_label = ctk.CTkLabel(self.frame, text="Select Difficulty:", font=("Arial", 14, "bold"),
                                             bg_color="transparent")
        self.difficulty_label.grid(row=3, column=0, padx=15, pady=0)

        options = [keys for keys in QUESTION_DIFFICULTY]
        self.selected_difficulty = ctk.StringVar(value=options[0])
        self.difficulty_optionmenu = ctk.CTkOptionMenu(
            self.frame, variable=self.selected_difficulty, anchor="center", width=300)
        self.difficulty_optionmenu.grid(row=3, column=1, padx=20, pady=5)
        CTkScrollableDropdown(self.difficulty_optionmenu, values=options)

    def make_proceedbutton(self):
        self.proceed_button = ctk.CTkButton(self, text="PROCEED", width=300, height=40,
                                            fg_color="white", command=self.proceed_event,
                                            text_color="black", corner_radius=80,
                                            font=("Arial", 20, "bold"), hover_color=HOVER_COLOR)
        self.proceed_button.grid(row=1, column=0, padx=20, pady=20)

    def proceed_event(self):
        selected_difficulty = QUESTION_DIFFICULTY[self.selected_difficulty.get(
        )]
        selected_amount = self.selected_amount.get()
        selected_type = QUESTION_TYPE[self.selected_type.get()]
        selected_category = QUESTION_CATEGORY[self.selected_category.get()]

        self.parameter = {
            "amount": selected_amount,
            "type": selected_type,
            "category": selected_category,
            "difficulty": selected_difficulty
        }

        try:
            response = requests.get(url=API_URL, params=self.parameter)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            if data["response_code"] == 0:
                for item in data["results"]:
                    self.questions_answers_options.append(
                        (item["question"], item["correct_answer"], item["incorrect_answers"]))
                random.shuffle(self.questions_answers_options)
                self.frame.destroy()
                self.proceed_button.destroy()
                if selected_type == QUESTION_TYPE["True / False"]:
                    self.true_false_window()
                elif selected_type == QUESTION_TYPE["Multiple Choice"]:
                    self.multiple_choice_window()
            else:
                self.error_label.configure(
                    text=RESPONSE_CODE[data["response_code"]])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def true_false_window(self):
        self.set_window_helper(fg_c="gray", size=18, px=25, py=40)
        self.question_label.configure(
            text=self.questions_answers_options[self.question_index][0])

        true_button = ctk.CTkButton(self, text="True", height=40, width=160,
                                    fg_color="white", command=lambda: self.verify_answer("True"),
                                    text_color="black", corner_radius=80,
                                    font=("Arial", 15, "bold"), hover_color=HOVER_COLOR)
        true_button.grid(row=1, column=0, padx=60, pady=25, sticky="w")
        self.option_buttons.append(true_button)

        false_button = ctk.CTkButton(self, text="False", height=40, width=160,
                                     fg_color="white", command=lambda: self.verify_answer("False"),
                                     text_color="black", corner_radius=80,
                                     font=("Arial", 15, "bold"), hover_color=HOVER_COLOR)
        false_button.grid(row=1, column=0, padx=60, pady=25, sticky="e")
        self.option_buttons.append(false_button)

    def multiple_choice_window(self):
        self.set_window_helper(fg_c="gray", size=18, px=25, py=40)
        self.question_label.configure(
            text=self.questions_answers_options[self.question_index][0])

        options = [self.questions_answers_options[self.question_index][1], self.questions_answers_options[self.question_index][2][0],
                   self.questions_answers_options[self.question_index][2][1], self.questions_answers_options[self.question_index][2][2]]
        options_add = [options.pop(random.randint(0, len(options) - 1)),
                       options.pop(random.randint(0, len(options) - 1)),
                       options.pop(random.randint(0, len(options) - 1)),
                       options.pop(random.randint(0, len(options) - 1))]
        option1_button = ctk.CTkButton(self, text=options_add[0], height=40, width=200,
                                       fg_color="white", command=lambda: self.verify_answer(option1_button.cget("text")),
                                       text_color="black", corner_radius=80,
                                       font=("Arial", 15, "bold"), hover_color=HOVER_COLOR)
        option1_button.grid(row=1, column=0, padx=60, pady=10, sticky="w")
        self.option_buttons.append(option1_button)

        option2_button = ctk.CTkButton(self, text=options_add[1], height=40, width=200,
                                       fg_color="white", command=lambda: self.verify_answer(option2_button.cget("text")),
                                       text_color="black", corner_radius=80,
                                       font=("Arial", 15, "bold"), hover_color=HOVER_COLOR)
        option2_button.grid(row=1, column=0, padx=60, pady=10, sticky="e")
        self.option_buttons.append(option2_button)

        option3_button = ctk.CTkButton(self, text=options_add[2], height=40, width=200,
                                       fg_color="white", command=lambda: self.verify_answer(option3_button.cget("text")),
                                       text_color="black", corner_radius=80,
                                       font=("Arial", 15, "bold"), hover_color=HOVER_COLOR)
        option3_button.grid(row=2, column=0, padx=60, pady=10, sticky="w")
        self.option_buttons.append(option3_button)

        option4_button = ctk.CTkButton(self, text=options_add[3], height=40, width=200,
                                       fg_color="white", command=lambda: self.verify_answer(option4_button.cget("text")),
                                       text_color="black", corner_radius=80,
                                       font=("Arial", 15, "bold"), hover_color=HOVER_COLOR)
        option4_button.grid(row=2, column=0, padx=60, pady=10, sticky="e")
        self.option_buttons.append(option4_button)

    def verify_answer(self, answer):
        if self.question_index >= len(self.questions_answers_options)-1:
            self.final_score_window()
        if answer == self.questions_answers_options[self.question_index][1]:
            self.score += 1
            for button in self.option_buttons:
                if button.cget("text") == answer:
                    button.configure(fg_color="green", hover_color="green")
                    self.after(200, lambda: button.configure(
                        fg_color="white", hover_color="lightgray"))
                    break
        elif answer != self.questions_answers_options[self.question_index][1]:
            for button in self.option_buttons:
                if button.cget("text") == answer:
                    button.configure(fg_color="red", hover_color="red")
                    self.after(200, lambda: button.configure(
                        fg_color="white", hover_color="lightgray"))
                    break
        self.question_index += 1
        self.question_label.configure(
            text=self.questions_answers_options[self.question_index][0])
        if self.parameter["type"] == "multiple":
            random.shuffle(self.option_buttons)
            self.option_buttons[0].configure(
                text=self.questions_answers_options[self.question_index][1])
            self.option_buttons[1].configure(
                text=self.questions_answers_options[self.question_index][2][0])
            self.option_buttons[2].configure(
                text=self.questions_answers_options[self.question_index][2][1])
            self.option_buttons[3].configure(
                text=self.questions_answers_options[self.question_index][2][2])

    def set_window_helper(self, fg_c, size, px, py):
        self.question_frame = ctk.CTkFrame(
            self, fg_color=fg_c, width=500, height=150, border_width=2)
        # Prevents the frame from resizing to fit its contents
        self.question_frame.grid_propagate(False)
        self.question_frame.grid(row=0, column=0, padx=25, pady=20)

        self.question_label = ctk.CTkLabel(self.question_frame, text="", font=("Arial", size, "bold"),
                                           anchor="center", justify="center", wraplength=450)
        self.question_label.grid(
            row=0, column=0, padx=px, pady=py, sticky="nsew")

    def final_score_window(self):
        self.clear_widgets()
        self.set_window_helper(fg_c=FG_COLOR, size=30, px=180, py=50)
        self.question_label.configure(
            text=f"Final Score\n {self.score}/{len(self.questions_answers_options)}")

        self.quit_button = ctk.CTkButton(self, text="Exit", height=40, width=160,
                                         fg_color="red", command=lambda: exit(),
                                         text_color="white", corner_radius=80,
                                         font=("Arial", 15, "bold"), hover_color="#FF5B61")
        self.quit_button.grid(row=1, column=0, padx=65, pady=25, sticky="w")

        self.playagain_button = ctk.CTkButton(self, text="Play Again", height=40, width=160,
                                              fg_color="green", command=self.play_again,
                                              text_color="white", corner_radius=80,
                                              font=("Arial", 15, "bold"), hover_color="#32de84")
        self.playagain_button.grid(
            row=1, column=0, padx=65, pady=25, sticky="e")

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def play_again(self):
        self.clear_widgets()
        self.initialize()


if __name__ == "__main__":
    game = QuizGame()
    game.mainloop()
