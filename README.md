# Quizler Application

Quizler is a Python-based quiz application built using the `customtkinter` library. The application fetches quiz questions from the Open Trivia Database API and allows users to select various quiz settings like the number of questions, category, type, and difficulty. The quiz presents questions in either multiple-choice or true/false format and displays the final score at the end with an option to play again or exit.

## Features

- **Customizable Quiz Settings:**
  - Choose the number of questions (1-50).
  - Select from various categories (e.g., General Knowledge, Science, Entertainment).
  - Pick the quiz type: Multiple Choice or True/False.
  - Set the difficulty level: Easy, Medium, or Hard.

- **Randomized Questions:**
  - The quiz questions and options are shuffled to provide a unique experience every time.

- **User-Friendly Interface:**
  - Built with `customtkinter` for a modern and responsive UI.
  - Visual feedback when selecting answers, with color indications for correct and incorrect answers.

- **Final Score Display:**
  - The user's score is shown at the end of the quiz, along with an option to play again or exit the application.

## Installation

### Prerequisites

- Python 3.x installed on your machine.
- The required Python packages can be installed using `pip`.

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/quizler.git
   ```

2. Navigate to the project directory:
    ```bash
    cd quizler
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application::
    ```bash
    python main.py
    ```

## Usage
1. Launch the application by running main.py.
2. Customize your quiz settings:
    - Choose the number of questions.
    - Select a category.
    - Choose the type of quiz (Multiple Choice or True/False).
    - Set the difficulty level.
3. Click "PROCEED" to start the quiz.
4. Answer the questions by selecting the correct option.
5. View your final score at the end of the quiz.
6. Choose to play again or exit the application.

## Code Structure
- `main.py`: The main script that initializes the quiz application and handles user interactions.
- `Utility/CTkScrollableDropdown.py`: A custom utility for adding scrollable dropdown menus in `customtkinter`.
- `README.md`: This documentation file.

## Acknowledgements

- The quiz questions are sourced from the [Open Trivia Database API](https://opentdb.com/).
- The application UI is built using the `customtkinter` library, with the help of open source utility [CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown)