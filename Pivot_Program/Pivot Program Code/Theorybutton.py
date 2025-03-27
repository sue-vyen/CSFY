from tkinter import *
from PIL import Image, ImageTk


def theory_button(x):
    text_format = ("Times New Roman", 15)
    content1 = """
    Definition:
    Moment of force, also known as torque, refers to the tendency of an applied force to rotate a body about a point. This point 
    is known as a pivot point. A moment is generated when a force acts on an object at a distance from the pivot point, which 
    causes a rotational motion around the pivot point. 

    Equation:
    The moment of force can be calculated using the following equation:  

          M = F * d 

            Where:
            - M is the moment of force / torque 
            - F is the force acting upon the system 
            - d is the perpendicular distance between the pivot point and the applied force
  """

    content2 = """
    Definition:
    This principle states that a system is in equilibrium if the total moment in the clockwise direction is equal to the total 
    moment in the anti-clockwise direction about a pivot point.In this state, the body is balanced, and no turning effect occurs 
    in the system.  

    Opposite outcome:
    When there is a difference of moment between 2 opposing forces, a turning effect will occur in the system. For example, 
    when the moment of force at the anti-clockwise direction of the system is greater, the turning effect wil cause the 
    system to rotate towards the anti-clockwise direction. 

    Application:
    According to this principle, manipulation of a system’s 
    parameters (distance and force) could achieve many effects, 
    like a lever. 

  """

    content3 = """
    Lever structure:
    A lever is a system that manipulates the principle of moment.The structure consists of a beam-shaped platform on a fulcrum, 
    the fulcrum serves as the pivot point. The beam platform serves as a medium for the forces to be applied. 

    Application:
    Weights are placed on both edges of the beam, implicating that the forces are applied to the platform. 
    Perpendicular distance, d is the distance between the weight and the fulcrum. 

    Outcome:
    - When the moment of both sides is equal, the beam will remain static since no turning effect occurs. 

    - When the moment of both sides is different, the beam will rotate towards the point with the greater moment of force, 
      which is either clockwise or anti-clockwise. 

    - The extent of the rotation depends on the difference between the moments. The larger the difference, the larger the 
      rotation. By manipulating the structure of the system, namely the perpendicular distance, placement of the fulcrum, and the 
      length of the beam, it is possible to find the least force needed to lift an object.
  """

    # list to keep a reference for all the current opened pages
    pages_list = []

    # Enable button
    def enable_button(button, page):
        button['state'] = 'normal'
        page.destroy()

    def disable_button(button):
        button['state'] = 'disabled'

    def theory_content(activation_button, content, title):
        disable_button(activation_button)
        detail_page = Toplevel()
        detail_page.title(title)
        moment_theory = Text(detail_page, width=100, height=20)
        moment_theory.insert(END, content)
        moment_theory.place(x=20, y=20)
        moment_theory.configure(font=text_format, background='CadetBlue1', state='disabled')
        
        if content== content2:
        #the gif to explain theory
          theory_gif = Label(detail_page)
          theory_gif.place(x=550, y=230)
          animate_gif(theory_gif,'theorygif.gif', 100)
        
        moment_theory.pack()

        pages_list.append(detail_page)

        # function to remove this specific page, and update the list
        def close_page():
            enable_button(activation_button, detail_page)
            pages_list.remove(detail_page)
            detail_page.destroy()

        detail_page.protocol('WM_DELETE_WINDOW', lambda: close_page())

    # Disable the button
    disable_button(x)
    # window for theory's header
    global theory_page
    theory_page = Tk()
    theory_page.geometry('400x400')
    theory_page.configure(background="pale turquoise")
    
    theory_title = Label(theory_page, text='The Theory of Moment', font=('Bahnschrift SemiBold', 20), bg="pale turquoise"
                         ,highlightbackground='black',highlightthickness=2, padx=8, pady=8)
    theory_title.place(x=60, y=50)
    
    Moment = Button(theory_page, text='Moment', command=lambda: theory_content(Moment, content1, 'Moment'),
                    background='pink',font=('Bahnschrift SemiBold', 15),padx=55)
    Moment.place(x= 100, y=160)
    
    Principle = Button(theory_page, text='Principle of Moment',
                       command=lambda: theory_content(Principle, content2, 'Principle of Moment'),
                       background='PaleGreen2',font=('Bahnschrift SemiBold', 15))
    Principle.place(x=100, y=220)
    lever = Button(theory_page, text='Principle of Lever',font=('Bahnschrift SemiBold', 15),
                   
                   command=lambda: theory_content(lever, content3, 'Principle of Lever'), background='pink', padx=12)
    lever.place(x=100, y=280)

    # when the menu is closed, all the existing theory pages is deleted
    def close_theory_menu():
        for detail_page in pages_list:
            detail_page.destroy()
        enable_button(x, theory_page)

        # Enable the 'theory' button back upon closure

    theory_page.protocol('WM_DELETE_WINDOW', lambda: close_theory_menu())
    
    
def close_window():
  theory_page.destroy()
  
def animate_gif(label, path, delay, index=0):
    gif = Image.open(path)
    frames = []

  #insert frame until end of file error (gif has ended)
    try:
        while True:
            frame = gif.copy()
            frame = frame.resize((300, 200))
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    label.config(image=frames[index])
    label.image = frames[index]

    #delay for a moment and call the function back again, index cannot exceed the length 
    label.after(delay, animate_gif, label, path, delay, (index + 1) % len(frames))