from tkinter import *
from Theorybutton import theory_button, close_window
from quiz import MomentQuiz
from tkinter import messagebox
import math
from PIL import Image, ImageTk
import time
import os
from StartMenu import start_menu, open_unlockables_window, check_unlockable
import pygame

current_image1= 'Red_square.png'
current_image2= 'Red_square.png'

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

background_music.play(-1)


# Function to calculate moment and animation
def calculate_moment():
    global d1, d2
    try:
        f1 = float(force1_entry.get())
        d1 = float(distance1_entry.get())
        f2 = float(force2_entry.get())
        d2 = float(distance2_entry.get())

        if f1 >= 0 and f1 <= 100:
            force1_scale.set(f1)

        if f2 >= 0 and f2 <= 100:
            force2_scale.set(f2)

        input_list = [f1, d1, f2, d2]
        negative_check(input_list)

        moment1 = round((f1 * d1), 2)
        moment2 = round((f2 * d2), 2)
        global total_moment
        total_moment = moment1 - moment2

        output.config(state=NORMAL)
        output.delete('1.0', END)
        output.insert(END, str(total_moment))
        output.config(state=DISABLED)

        pivot_position()

        moment_sum = moment1 + moment2
        # animation and angle

        if total_moment == 0:
            moment_label.config(text="Equilibrium")
        elif total_moment > 0:
            moment_label.config(text="Clockwise Moment")
        else:
            moment_label.config(text="Anticlockwise Moment")

        # 90 is the maximum angle to be rotated for one direction
        global angle
        if moment_sum ==0:
           angle = 0 
        else: 
            angle = (-total_moment / moment_sum) * 20

        # obtain the new coords
        beam_movement(x_coordinate, 190, angle)

        # draw the animation result
        if total_moment != 0:
            animate()
        else:
            create_animation()

    except ValueError:
        messagebox.showinfo("Invalid Input", "Please enter valid numbers.")


# Function to check for negative input values
def negative_check(input_list):
    for i in input_list:
        if i < 0:
            messagebox.showinfo("Invalid Input", "Please enter positive numerical values.")
            return


def create_animation(pivot_xshift=0, pivot_yshift=0, x1=60, x2=540, y1=170, y2=170, angle=0,
                     weight_shiftx=0,
                     weight_shifty1=0, weight_shifty2=0):
    animation_canvas.delete('all')
    
    square1 = Image.open(current_image1)
    square1 = square1.resize((80, 80))
    square1 = square1.rotate(angle, expand=True)
    square1 = ImageTk.PhotoImage(square1)
    
    square2 = Image.open(current_image2)
    square2 = square2.resize((80, 80))
    square2 = square2.rotate(angle, expand=True)
    square2 = ImageTk.PhotoImage(square2)

    weight1 = animation_canvas.create_image(40 + x1 + weight_shiftx, y1 - 60 + weight_shifty1, image=square1)
    weight2 = animation_canvas.create_image(x2 - 40 + weight_shiftx, y2 - 60 + weight_shifty2, image=square2)
    
    animation_canvas.image = square1, square2

    # make the beam appear on top of the image
    beam = animation_canvas.create_line(x1, y1, x2, y2, width=40)
    animation_canvas.tag_raise(beam)

    animation_canvas.create_polygon(300 + pivot_xshift, 190 - pivot_yshift, 270 + pivot_xshift,
                                    250 - pivot_yshift, 330 + pivot_xshift, 250 - pivot_yshift, fill='blue')


# calculate the new beam coordinate
def beam_movement(centerx, centery, angle):
    global x1, x2, y1, y2
    global x1_shift
    global x2_shift
    global y1_shift
    global y2_shift
    # angle in radian
    angle = math.radians(angle)

    # new cords (rotation matrices equation)
    x1 = centerx + (60 - centerx) * math.cos(angle) - (150 - centery) * math.sin(angle)
    y1 = centery + (60 - centerx) * math.sin(angle) + (150 - centery) * math.cos(angle)
    x2 = centerx + (540 - centerx) * math.cos(angle) - (150 - centery) * math.sin(angle)
    y2 = centery + (540 - centerx) * math.sin(angle) + (150 - centery) * math.cos(angle)

    x1_shift = x1 - 60
    x2_shift = x2 - 540
    y1_shift = y1 - 170
    y2_shift = y2 - 170


# enable smooth animation
def animate():
    # total frame defined is 30, calculate the shift for each frame
    x1_increment = x1_shift / 30
    x2_increment = x2_shift / 30
    y1_increment = y1_shift / 30
    y2_increment = y2_shift / 30
    angle_increment = -angle / 30

    # these thing is used to force fix the animation error that occur due to the mathematical equation 
    pivot_yincrement = 20 / 30
    if total_moment < 0:
        weight_xshift = 0.47
        weight_yshift1 = 0.5
        weight_yshift2 = 0
    elif total_moment > 0:
        weight_xshift = -0.55
        weight_yshift1 = 0.0
        weight_yshift2 = 0.55

    for frame in range(30):
        create_animation(pivot_shift, pivot_yshift,
                         60 + x1_increment * frame,
                         540 + x2_increment * frame,
                         170 + ((y1_increment + pivot_yincrement) * frame),
                         170 + ((y2_increment + pivot_yincrement) * frame),
                         angle_increment * frame,
                         weight_xshift * frame,
                         weight_yshift1 * frame, weight_yshift2 * frame)
        animation_canvas.update()
        time.sleep(0.1)


def themoment():
    global window
    window = Tk()
    window.geometry('1000x670')
    window.protocol("WM_DELETE_WINDOW", exit)
    window.configure(bg='pale turquoise')
    window.title('The Moment')

    # The theory button
    theory_canvas = Canvas(window, height=30, width=30, bg='pale turquoise', highlightbackground='pale turquoise')
    theory_canvas.place(x=15, y=15)
    circle = theory_canvas.create_oval(5, 5, 30, 30, width=2)

    circle_label = Button(window, text='i', font=('Times new roman', 12, 'bold'),
                          relief=FLAT, bg='pale turquoise', command=lambda: theory_button(circle_label))
    circle_label.place(x=26, y=24, height=17, width=15)

    theory_label = Label(window, text='Theory', font=('Times new roman', 14, 'bold'), bg='pale turquoise')
    theory_label.place(x=52, y=18)

    # The middle frame
    global middle_frame
    middle_frame = Frame(window, height=500, width=620, bg='pale turquoise')
    middle_frame.place(x=188, y=30)

    # animation frame
    global animation_canvas
    animation_canvas = Canvas(middle_frame, height=345, width=600, highlightbackground='black', highlightthickness=2)
    animation_canvas.place(x=10, y=150)

    pivot_scale = Scale(middle_frame, from_=0, to=100, orient=HORIZONTAL, width=13, length=535,
                        command=lambda event: distance_entry_update(pivot_scale, distance1_entry, distance2_entry))
    pivot_scale.set(50)
    pivot_scale.place(x=40, y=445)

    pivot_label = Label(middle_frame, text='Pivot position', font=('Bahnschrift SemiBold', 10))
    pivot_label.place(x=40, y=445)

    create_animation()

    # weight selection frame
    global selection_frame
    selection_frame = Frame(middle_frame, height=110, width=620, highlightbackground='black', highlightthickness=2)
    selection_frame.place(x=0, y=10)
    

    square_red = import_image("Red_square.png")
    square = Button(selection_frame, image=square_red, relief=FLAT,command=lambda:swap_weight('Red_square.png'))
    square.photo = square_red  
    square.place(x=20, y=10)
    square.origX, square.origY = 20, 10

    weight_selection(middle_frame)  

    # the output frame
    output_frame = Frame(window, height=130, width=620, bg='pale turquoise')
    formula = Label(output_frame, text='General formula: M = F*d', font=('Bahnschrift SemiBold', 18, 'bold'),
                    bg='pale turquoise')
    formula.place(x=170, y=10)

    output_label = Label(output_frame, text='Moment (Nm): ', font=('Bahnschrift SemiBold', 18, 'bold'),
                         bg='pale turquoise')
    output_label.place(x=130, y=60)

    global output
    output = Text(output_frame, font=('Bahnschrift SemiBold', 18, 'bold'), width=12, height=1)
    output.config(state=DISABLED)

    output.place(x=310, y=62)
    output_frame.place(x=188, y=540)

    # input frame left
    left_frame = Frame(window, height=360, width=160, bg='pale turquoise')

    global force1_scale
    force1_scale = Scale(left_frame, from_=0, to=100, orient=VERTICAL, width=20, length=100,
                         bg='pale turquoise', highlightbackground='pale turquoise',
                         command=lambda event: force_entry_update(force1_scale, force1_entry))
    force1_scale.place(x=110, y=90)

    weight1_label = Label(left_frame, font=('Bahnschrift SemiBold', 20, 'bold'), text='Weight 1', bg='pale turquoise')
    weight1_label.place(x=17, y=15)

    force1_label = Label(left_frame, font=('Bahnschrift SemiBold', 18, 'bold'), text='Force 1 (N):',
                         bg='pale turquoise')
    force1_label.place(x=0, y=80)

    global force1_entry
    force1_entry = Entry(left_frame, font=('Bahnschrift SemiBold', 15), width=8)
    force1_entry.place(x=15, y=125)             
    force1_entry.insert(0,0)

    distance1_label = Label(left_frame, font=('Bahnschrift SemiBold', 18, 'bold'), text='Distance 1 \n (m):',
                            bg='pale turquoise')
    distance1_label.place(x=0, y=195)

    global distance1_entry
    distance1_entry = Entry(left_frame, font=('Bahnschrift SemiBold', 15), width=8)
    distance1_entry.place(x=15, y=270)
    distance1_entry.config(state="disabled")

    left_frame.place(x=15, y=180)

    # input frame right
    right_frame = Frame(window, height=360, width=160, bg='pale turquoise')
    right_frame.place(x=822, y=180)

    weight1_label = Label(right_frame, font=('Bahnschrift SemiBold', 20, 'bold'), text='Weight 2', bg='pale turquoise')
    weight1_label.place(x=17, y=15)

    global force2_scale
    force2_scale = Scale(right_frame, from_=0, to=100, orient=VERTICAL, width=20, length=100,
                         bg='pale turquoise', highlightbackground='pale turquoise',
                         command=lambda event: force_entry_update(force2_scale, force2_entry))
    force2_scale.place(x=115, y=90)

    force2_label = Label(right_frame, font=('Bahnschrift SemiBold', 18, 'bold'), text='Force 2 (N):',
                         bg='pale turquoise')
    force2_label.place(x=0, y=80)

    global force2_entry
    force2_entry = Entry(right_frame, font=('Bahnschrift SemiBold', 15), width=8)
    force2_entry.place(x=15, y=125)
    force2_entry.insert(0, 0)

    distance2_label = Label(right_frame, font=('Bahnschrift SemiBold', 18, 'bold'), text='Distance 2 \n (m):',
                            bg='pale turquoise')
    distance2_label.place(x=0, y=195)

    global distance2_entry
    distance2_entry = Entry(right_frame, font=('Bahnschrift SemiBold', 15), width=8)
    distance2_entry.place(x=15, y=270)
    distance2_entry.config(state="disabled")

    # Moment label
    global moment_label
    moment_label = Label(window, text="")
    moment_label.place(x=40, y=640)

    # Start button
    start_button = Button(window, text='Start', font=('Bahnschrift SemiBold', 20), bg='SpringGreen2',
                          command=calculate_moment)
    start_button.place(x=40, y=580)

    # End button
    end_button = Button(window, text='End', font=('Bahnschrift SemiBold', 20), bg='red2', command=exit)
    end_button.place(x=890, y=580)

    # enter quiz
    quiz_button = Button(window, text='Quiz', font=('Bahnschrift SemiBold', 14), command=quiz)
    quiz_button.place(x=920, y=70)
    
    #return button
    return_button = Button(window, text='Return', font=('Bahnschrift SemiBold', 14),command= lambda: return_menu(window))
    return_button.place(x=900, y=20)
        
    #unlockable button
    unlockable = Button(window, text='Unlocklable', font=('Bahnschrift SemiBold', 14), command = lambda: open_unlockables_window(window))
    unlockable.place(x=857, y=120)

    #refresh button
    refresh = Button(window, text='↻', font=('Bahnschrift SemiBold', 12), command =refresh_selection)
    refresh.place(x=820, y= 40)
    
    #mute button
    mute = Button(window, text='🔇', font=('Bahnschrift SemiBold', 12), command= lambda: mute_music())
    mute.place(x=875,y=73)
    

    window.mainloop()
    
#mute the background music
background_playing = True
def mute_music():
    global background_playing
    if background_playing == True:
        background_music.set_volume(0)
        background_playing = False
    elif background_playing == False:
        background_music.set_volume(1)
        background_playing = True

#return to menu
def return_menu(root):
    root.destroy()
    try:
        close_window()
    except:
        pass
    start_menu()
    themoment()


# Scale widget update the force entry widget
def force_entry_update(scale_widget, entry_widget):
    value = scale_widget.get()
    entry_widget.delete(0, END)
    entry_widget.insert(0, value)


# Scale widget update the distance entry widget
def distance_entry_update(scale_widget, widget_distance1, widget_distance2):
    widget_distance1.config(state="normal")
    widget_distance2.config(state='normal')
    value = scale_widget.get()
    distance2 = 100 - value
    distance1 = 100 - distance2
    widget_distance1.delete(0, END)
    widget_distance1.insert(0, distance1)
    widget_distance2.delete(0, END)
    widget_distance2.insert(0, distance2)
    widget_distance1.config(state="disabled")
    widget_distance2.config(state='disabled')
    pivot_position()
    create_animation(pivot_xshift=pivot_shift)


def quiz():
    quiz_window = MomentQuiz()
    quiz_window.mainloop()
 
def import_image(filename):
    image = Image.open(filename)
    image = image.resize((80, 80))  
    photo = ImageTk.PhotoImage(image)
    return photo


#add the unlocked weight selection  
def weight_selection(frame):
    unlocked_list = check_unlockable()
    if 'car' in unlocked_list:
        image3 = import_image("unlockable3.png")
        car = Button(selection_frame, image=image3, relief=FLAT,command=lambda:swap_weight("unlockable3.png"))
        car.photo = image3
        car.place(x=130, y=10)
        car.origX, car.origY = 130, 10
        
    if 'anvil' in unlocked_list:
        image2 = import_image("unlockable2.png")
        anvil = Button(selection_frame, image=image2,relief=FLAT, command=lambda:swap_weight("unlockable2.png"))
        anvil.photo = image2
        anvil.place(x=240, y=10)
        anvil.origX, anvil.origY = 240, 10
        
    if 'tree' in unlocked_list:
        image1 = import_image("unlockable1.png")
        tree = Button(selection_frame, image=image1, relief=FLAT,command=lambda:swap_weight("unlockable1.png"))
        tree.photo = image1
        tree.place(x=350, y=10)
        tree.origX, tree.origY = 350, 10
        
    if 'child' in unlocked_list:
        image4 = import_image("unlockable4.png")
        child = Button(selection_frame, image=image4, relief=FLAT,command=lambda:swap_weight("unlockable4.png"))
        child.photo = image4
        child.place(x=460, y=10)
        child.origX, child.origY = 460, 10
   
#refresh the widget selection
def refresh_selection():
    weight_selection(middle_frame)
    
def swap_weight(image):
    weight_select = Toplevel()
    weight_select.config(bg='pale turquoise')
    weight_select.geometry('215x100')
    text_label = Label(weight_select, text='Do you want this object as:', font=('Bahnschrift SemiBold', 12),bg='pale turquoise')
    text_label.place(x=10, y=10)
    weight1_option = Button(weight_select, text='weight1',font=('Bahnschrift SemiBold', 12), command=lambda: weight1_change(image))
    weight2_option = Button(weight_select, text='weight2',font=('Bahnschrift SemiBold', 12),  command=lambda: weight2_change(image))
    weight1_option.place(x=30, y=50)
    weight2_option.place(x=120, y=50)

    
    
def weight_update_force(image,forceentry):
    if image=='unlockable1.png':
        forceentry.config(state='normal')
        forceentry.delete(0,END)
        forceentry.insert(0,100)
        forceentry.config(state='disabled')
    if image=='unlockable2.png':
        forceentry.config(state='normal')
        forceentry.delete(0,END)
        forceentry.insert(0,80)
        forceentry.config(state='disabled')
    if image=='unlockable3.png':
        forceentry.config(state='normal')
        forceentry.delete(0,END)
        forceentry.insert(0,100)
        forceentry.config(state='disabled')
    if image=='unlockable4.png':
        forceentry.config(state='normal')
        forceentry.delete(0,END)
        forceentry.insert(0,30)
        forceentry.config(state='disabled')
    if image=='Red_square.png':
        forceentry.config(state='normal')
        if forceentry == force1_entry:
            forceentry.delete(0,END)
            forceentry.insert(0,force1_scale.get())
        elif forceentry == force2_entry:
            forceentry.delete(0,END)
            forceentry.insert(0,force2_scale.get())
      
    
def weight1_change(image):
    global current_image1
    current_image1=  image
    weight_update_force(image, force1_entry)
    create_animation()

    
def weight2_change(image):
    global current_image2
    current_image2= image
    weight_update_force(image, force2_entry)
    create_animation()

#determine the pivot shift value in the animation
def pivot_position():
        d1 = float(distance1_entry.get())
        d2 = float(distance2_entry.get())
        # calculate the ratio of distance
        distance_sum = d1 + d2
        global d1_percentage
        d1_percentage = d1 / distance_sum
        global pivot_shift
        global pivot_yshift
        # calculate the x shift for the pivot
        global x_coordinate
        x_coordinate = (480 * d1_percentage) + 60
        pivot_shift = int(x_coordinate) - 300
        # this is fixed amount to match up with the beam movement
        pivot_yshift = 0

start_menu()
themoment()