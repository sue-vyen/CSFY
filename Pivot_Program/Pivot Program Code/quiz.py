import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os

# Required to access the current directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pygame.mixer.init()

def play_sound(sound):
    sound.play()

click_sound = pygame.mixer.Sound("click_sound.wav")
confetti_sound = pygame.mixer.Sound("confetti_sound.wav")
hurray_sound = pygame.mixer.Sound("hooray_sound.wav")
womp_womp_sound = pygame.mixer.Sound("womp_womp_sound.wav")
circus_sound = pygame.mixer.Sound("circus_sound.wav")
victory_sound = pygame.mixer.Sound("victory_sound.wav")
background_music = pygame.mixer.Sound("background_music.wav")


class MomentQuiz(tk.Tk):
    correct_amount =0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Moment Quiz")
        self.geometry("400x300")


        self.questions = [
            {
                "question": "What is moment in physics?",
                "answers": ["Force x Distance", "Mass x Acceleration", "Speed x Time", "Energy / Distance"],
                "correct_answer": "Force x Distance"
            },
            {
                "question": "Which of the following has the greatest moment?",
                "answers": ["A heavy object at a short distance", "A light object at a long distance", "A heavy object at a long distance", "A light object at a short distance"],
                "correct_answer": "A heavy object at a long distance"
            },
            {
                "question": "What is the SI unit of moment?",
                "answers": ["Newton", "Joule", "Watt", "Newton meter"],
                "correct_answer": "Newton meter"
            },
            {
                "question": "In which of the following situations is moment NOT involved?",
                "answers": ["Opening a door", "Using a pair of scissors", "Pushing a car", "Lifting a box"],
                "correct_answer": "Pushing a car"
            },
            {
                "question": "Which formula represents the moment of a force?",
                "answers": ["m = F × a", "m = F ÷ A", "m = F × d", "m = F × v"],
                "correct_answer": "m = F × d"
            },
            {
                "question": "Which of the following is NOT a factor affecting moment?",
                "answers": ["Force applied", "Distance from the pivot point", "Speed of the object", "Angle of the force"],
                "correct_answer": "Speed of the object"
            },
            {
                "question": "What happens to the moment when the distance from the pivot point increases?",
                "answers": ["It decreases", "It stays the same", "It increases", "It becomes negative"],
                "correct_answer": "It increases"
            },
            {
                "question": "If two forces are applied in opposite directions along a straight line, what happens to the moments they produce?",
                "answers": ["They cancel each other out", "They add together", "They decrease", "They multiply"],
                "correct_answer": "They cancel each other out"
            },
            {
                "question": "What is the moment of a 10N force applied 2 meters from the pivot?",
                "answers": ["5 Nm", "10 Nm", "20 Nm", "100 Nm"],
                "correct_answer": "20 Nm"
            },
            {
                "question": "Which of the following objects has the greatest moment?",
                "answers": ["A 20N force applied at 1m from the pivot", "A 10N force applied at 5m from the pivot", "A 5N force applied at 10m from the pivot", "A 15N force applied at 2m from the pivot"],
                "correct_answer": "A 5N force applied at 10m from the pivot"
            },
            {
                "question": "What is the moment of a 30N force applied at an angle of 60 degrees from the horizontal, and 4m from the pivot?",
                "answers": ["60 Nm", "120 Nm", "240 Nm", "480 Nm"],
                "correct_answer": "240 Nm"
            },
            {
                "question": "Which of the following statements about moments is true?",
                "answers": ["The moment is independent of the pivot point", "Clockwise moments are positive", "The moment is measured in kilograms", "Moment arm is the same as force"],
                "correct_answer": "Clockwise moments are positive"
            },
            {
                "question": "What is the principle of moments?",
                "answers": ["sum of clockwise moments = sum of anticlockwise moments", "The sum of clockwise moments equals zero", "The sum of anticlockwise moments equals zero", "The sum of moments equals force"],
                "correct_answer": "sum of clockwise moments = sum of anticlockwise moments"
            },
            {
                "question": "What is the torque?",
                "answers": ["The same as moment", "The same as force", "The same as acceleration", "The same as energy"],
                "correct_answer": "The same as moment"
            },
            {
                "question": "Which of the following is an application of the principle of moments?",
                "answers": ["Archimedes' principle", "Bernoulli's principle", "Pascal's principle", "Lever balance"],
                "correct_answer": "Lever balance"
            },
        ]

        self.current_question_index = 0
        self.shuffle_questions()
        self.create_widgets()

    def shuffle_questions(self):
        random.shuffle(self.questions)

    def create_widgets(self):
        self.question_label = tk.Label(self, text="", wraplength=380, justify="center", font=("Arial", 12))
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(self, text="", width=46, command=lambda idx=i: self.select_answer(idx))
            button.pack(pady=5)
            self.answer_buttons.append(button)

        self.confirm_button = tk.Button(self, text="Confirm", width=10, command=self.confirm_answer)
        self.confirm_button.pack(pady=10)
        self.confirm_button.config(state="disabled")  # Initially disable the confirm button

        self.next_question()

    def next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question["question"])
            answers = question["answers"]
            random.shuffle(answers)
            for i in range(4):
                self.answer_buttons[i].config(text=answers[i], bg="SystemButtonFace", state="normal")  # Enable buttons
            self.current_question_index += 1
        else:
            global app
            messagebox.showinfo("Quiz Finished", "You have finished the quiz!")
            play_sound(circus_sound)
            messagebox.showinfo('Score', f'{self.correct_amount} out of 15')
            MomentQuiz.destroy(self)

    def select_answer(self, selected_index):
        for i in range(4):
            self.answer_buttons[i].config(state="disabled")  # Disable all buttons
        self.selected_index = selected_index  # Store the selected index
        self.confirm_button.config(state="normal")  # Enable the confirm button

    def confirm_answer(self):
        selected_answer = self.answer_buttons[self.selected_index]["text"]
        correct_answer = self.questions[self.current_question_index - 1]["correct_answer"]
        if selected_answer == correct_answer:
            self.answer_buttons[self.selected_index].config(bg="green")
            messagebox.showinfo("Correct", "Correct Answer!")
            self.correct_amount = self.correct_amount+1
            play_sound(hurray_sound)
            if self.current_question_index == len(self.questions):
                play_sound(victory_sound)
                

        else:
            self.answer_buttons[self.selected_index].config(bg="red")
            messagebox.showinfo("Incorrect", f"Correct Answer: {correct_answer}")
            play_sound(womp_womp_sound)
            for i in range(4):
                if self.answer_buttons[i]["text"] == correct_answer:
                    self.answer_buttons[i].config(bg="green")
                    break
        self.after(1000, self.next_question)  # Move to next question after 1 second
        self.confirm_button.config(state="disabled")  # Disable confirm button again

        self.lift()

if __name__ == "__main__":
    app = MomentQuiz()
    app.mainloop()

