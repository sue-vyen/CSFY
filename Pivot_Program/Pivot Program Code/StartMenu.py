import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random
from Theorybutton import theory_button, close_window
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

def start_menu():
    global child_unlock, anvil_unlock, tree_unlock, car_unlock
    child_unlock= False
    anvil_unlock= False
    tree_unlock= False
    car_unlock= False
    # Add a list of image paths
    global image_paths
    image_paths = ["guide1.png", "guide2.png", "guide3.png", "guide4.png"]  # Update the paths accordingly


    def open_guide_window():
        play_sound(click_sound)
        def display_image(image_label, image_path):
            image = Image.open(image_path)
            image = image.resize((600, 400))
            photo = ImageTk.PhotoImage(image)
            image_label.configure(image=photo)
            image_label.image = photo  # Keep a reference to prevent garbage collection

        guide_window = tk.Toplevel(root)
        guide_window.title("Guide")

        # Create a label to display the image
        image_label = tk.Label(guide_window)
        image_label.pack(pady=10, padx=10)

        # Load the first image
        current_image = 0
        display_image(image_label, image_paths[current_image])

        # Create navigation buttons
        def navigate_images(direction):
            play_sound(click_sound)
            nonlocal current_image
            current_image = (current_image + direction) % len(image_paths)
            display_image(image_label, image_paths[current_image])

        prev_button = ttk.Button(guide_window, text="Previous", command=lambda: navigate_images(-1))
        prev_button.pack(side=tk.LEFT, padx=10)

        next_button = ttk.Button(guide_window, text="Next", command=lambda: navigate_images(1))
        next_button.pack(side=tk.LEFT, padx=10)

        # Create a close button
        close_button = ttk.Button(guide_window, text="Close", command=guide_window.destroy)
        close_button.pack(side=tk.BOTTOM, pady=10)


        

    def start_main_code():
        play_sound(click_sound)
        root.destroy()
        close_window()
        

    root = tk.Tk()
    root.title("The Moment")
    root.config(background='Pale Turquoise')
    root.protocol('WM_DELETE_WINDOW', lambda: exit())

    # Set window size and center it on the screen
    window_width = 650
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    #theory button
    theory_canvas = tk.Canvas(root, height=30, width=30, bg='pale turquoise', highlightbackground='pale turquoise')
    theory_canvas.place(x=15, y=15)
    circle = theory_canvas.create_oval(5, 5, 30, 30, width=2)

    circle_label = tk.Button(root, text='i', font=('Times new roman', 12, 'bold'),
                          relief=tk.FLAT, bg='pale turquoise', command=lambda: theory_button(circle_label))
    circle_label.place(x=26, y=24, height=17, width=15)

    theory_label = tk.Label(root, text='Theory', font=('Times new roman', 14, 'bold'), bg='pale turquoise')
    theory_label.place(x=52, y=18)


    # Create a title label
    top_level_label = ttk.Label(root, text="Welcome", font=("Arial", 30, "bold"), foreground='DodgerBlue4', background='Pale Turquoise')
    middle_level_label = ttk.Label(root, text="To", font=("Arial", 30, "bold"), foreground='DodgerBlue4', background='Pale Turquoise')
    title_label = ttk.Label(root, text="The Moment Program", font=("Arial", 40, "bold"), foreground='DodgerBlue2', background='Pale Turquoise')
    
    # Style
    style = ttk.Style(root)
    style.configure("TButton", background="#90ee90", font=("Arial", 14))

    # Create buttons inside the main frame
    start_button = ttk.Button(root, text="Start", command=start_main_code, style="TButton")
    guide_button = ttk.Button(root, text="Guide", command=open_guide_window)
    unlockables_button = ttk.Button(root, text="Unlockables", command= lambda: open_unlockables_window(root))

    # position on the window
    top_level_label.place(relx=0.5, rely=0.2, anchor="center")
    middle_level_label.place(relx=0.5, rely=0.3, anchor="center")
    title_label.place(relx=0.5, rely=0.417, anchor="center")
    start_button.place(relx=0.5, rely=0.55, anchor="center")
    guide_button.place(relx=0.5, rely=0.65, anchor="center")
    unlockables_button.place(relx=0.5, rely=0.75, anchor="center")


    root.mainloop()     

def open_unlockables_window(root):
    play_sound(click_sound)
    unlockables_window = tk.Toplevel(root)
    unlockables_window.title("Unlockable Objects")

    # Style
    style = ttk.Style(unlockables_window)
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0")
    style.configure("TButton", background="#90ee90", font=("Arial", 12))

    # Create a frame for the content
    content_frame = ttk.Frame(unlockables_window, padding=(20, 10))
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Create a title label
    title_label = ttk.Label(content_frame, text="UNLOCKABLE OBJECTS", font=("Arial", 20, "bold"))
    title_label.pack(pady=(20, 10))

    # Create a frame for the grid
    grid_frame = ttk.Frame(content_frame, padding=10)
    grid_frame.pack()

    # Add new image paths for unlockables
    unlockable_image_paths = ["unlockable1.png", "unlockable2.png", "unlockable3.png", "unlockable4.png"]

    # Define mini-games
    def play_tree_mini_game():
        play_sound(click_sound)
        def check_answer():
            user_input = guess_entry.get()
            if user_input.lower() == correct_word.lower():
                result_label.config(text="Congratulations! You unlocked the tree.", foreground="green")
                global tree_unlock
                tree_unlock = True
                play_sound(confetti_sound)
            else:
                result_label.config(text="Sorry, try again.", foreground="red")

        tree_game_window = tk.Toplevel(unlockables_window)
        tree_game_window.title("Tree Mini Game")

        correct_word = "tree"
        shuffled_word = ''.join(random.sample(correct_word, len(correct_word)))

        instruction_label = ttk.Label(tree_game_window, text=f"Unscramble the word: {shuffled_word}")
        instruction_label.pack()

        guess_entry = ttk.Entry(tree_game_window, width=20)
        guess_entry.pack(pady=10)

        submit_button = ttk.Button(tree_game_window, text="Submit", command=check_answer)
        submit_button.pack()

        result_label = ttk.Label(tree_game_window, text="", font=("Arial", 12))
        result_label.pack()

    def play_anvil_mini_game():
        play_sound(click_sound)
        def hit_anvil():
            nonlocal hits
            hits += 1
            if hits >= 10:
                result_label.config(text="Congratulations! You unlocked the anvil.", foreground="green")
                global anvil_unlock
                anvil_unlock = True
                play_sound(confetti_sound)
            else:
                result_label.config(text=f"Hit the anvil {10 - hits} more times.", foreground="blue")

        hits = 0

        anvil_game_window = tk.Toplevel(unlockables_window)
        anvil_game_window.title("Anvil Mini Game")

        anvil_label = ttk.Label(anvil_game_window, text="Hit the anvil 10 times!", font=("Arial", 14))
        anvil_label.pack()

        hit_button = ttk.Button(anvil_game_window, text="Hit", command=hit_anvil)
        hit_button.pack()

        result_label = ttk.Label(anvil_game_window, text="", font=("Arial", 12))
        result_label.pack()

    def play_car_mini_game():
        play_sound(click_sound)
        def drive_car():
            nonlocal distance
            distance += random.randint(1, 10)
            if distance >= 100:
                result_label.config(text="Congratulations! You unlocked the car.", foreground="green")
                global car_unlock
                car_unlock = True
                play_sound(confetti_sound)
            else:
                result_label.config(text=f"Drive {100 - distance} more units.", foreground="blue")

        distance = 0

        car_game_window = tk.Toplevel(unlockables_window)
        car_game_window.title("Car Mini Game")

        car_label = ttk.Label(car_game_window, text="Drive the car 100 units!", font=("Arial", 14))
        car_label.pack()

        drive_button = ttk.Button(car_game_window, text="Drive", command=drive_car)
        drive_button.pack()

        result_label = ttk.Label(car_game_window, text="", font=("Arial", 12))
        result_label.pack()

    def play_child_mini_game():
        play_sound(click_sound)
        def find_child():
            nonlocal found_child
            if not found_child:
                found_child = True
                result_label.config(text="Congratulations! You found the child.", foreground="green")
                global child_unlock
                child_unlock= True
                play_sound(confetti_sound)
            else:
                result_label.config(text="Keep searching.", foreground="blue")

        found_child = False

        child_game_window = tk.Toplevel(unlockables_window)
        child_game_window.title("Child Mini Game")

        instruction_label = ttk.Label(child_game_window, text="Find the hidden child.", font=("Arial", 14))
        instruction_label.pack()

        find_button = ttk.Button(child_game_window, text="Find", command=find_child)
        find_button.pack()

        result_label = ttk.Label(child_game_window, text="", font=("Arial", 12))
        result_label.pack()

    mini_games = [play_tree_mini_game, play_anvil_mini_game, play_car_mini_game, play_child_mini_game]

    # Loop through each image path and create labels and buttons
    for index, path in enumerate(unlockable_image_paths):
        # Create a frame for each image and button to group them
        item_frame = ttk.Frame(grid_frame, padding=10)
        item_frame.grid(row=index // 2, column=index % 2, padx=10, pady=10)

        # Create a label for the image
        image = Image.open(path)
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)
        image_label = ttk.Label(item_frame, image=photo)
        image_label.photo = photo  # Keep a reference to prevent garbage collection
        image_label.pack()

        # Create a button to unlock
        unlock_button = ttk.Button(item_frame, text="Unlock!", command=mini_games[index])
        unlock_button.pack(pady=(10, 0))

    # Create a close button
    close_button = ttk.Button(content_frame, text="Close", command=unlockables_window.destroy)
    close_button.pack(pady=10)
    
def check_unlockable():
    unlocked_list = []
    if child_unlock== True:
        unlocked_list.append('child')
    if car_unlock== True:
        unlocked_list.append('car')
    if anvil_unlock== True:
        unlocked_list.append('anvil')
    if tree_unlock== True:
        unlocked_list.append('tree')
    return unlocked_list
        
        

