import tkinter
import pygame
from tkinter import filedialog
from tkinter import GROOVE
import time
from mutagen.mp3 import MP3
import sys
import os
import shutil

def on_closing(): # to make sure the program is closed
    print("Music Player window closed.")
    music_player.destroy()

def start_music_player(email):
    global music_player
    music_player = tkinter.Tk()
    music_player.title("Music Player")
    music_player.geometry("450x300")
    music_player.protocol("WM_DELETE_WINDOW", on_closing)
    pygame.mixer.init()

    label = tkinter.Label(music_player, text=f"Welcome to the Music Player, {email[:-10]}!")
    label.pack()

    # 2nd frame for playlist_set and volume slider
    playlist_set_n_volume_frame = tkinter.Frame(music_player)
    playlist_set_n_volume_frame.pack(fill=tkinter.BOTH, expand=True)

    # 3rd frame for control buttons
    controls_frame = tkinter.Frame(music_player)
    controls_frame.pack()

    # The playlist set
    playlist_set = tkinter.Listbox(playlist_set_n_volume_frame, bg="silver", width=60, selectbackground="PaleGreen2", selectforeground="DarkOrchid4")
    playlist_set.pack(side=tkinter.LEFT, padx=(10,5), pady=10)

    # Load the user's saved songs from the folder
    user_folder = f'C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\{email[:-10]}\\'
    if os.path.exists(user_folder):
        saved_songs = os.listdir(user_folder)
        for song in saved_songs:
            if song.endswith(".mp3"):
                song_name = song.replace(".mp3", "")
                playlist_set.insert(tkinter.END, song_name)

    # Song Length Time displayed at the bottom-right
    def song_length():
        current_time = pygame.mixer.music.get_pos() / 1000
        current_time = int(current_time)
        new_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

        song = playlist_set.get(tkinter.ACTIVE)
        song = f'C:/Users/kloke/OneDrive/Desktop/UoSM/SEM2/33/python2/Labwork2/songs_db/{song}.mp3'
        song1 = MP3(song)
        song1_length = song1.info.length
        new_song_length = time.strftime('%H:%M:%S', time.gmtime(song1_length))

        status_bar.configure(text=f"{new_current_time}/{new_song_length}")
        status_bar.after(1000, song_length)
    
    # Status Bar
    status_bar = tkinter.Label(music_player, text="", bd=1, relief=GROOVE, anchor=tkinter.E)
    status_bar.pack(fill=tkinter.X, side=tkinter.BOTTOM, ipady=2)

    # Play Button
    def play():
        song = playlist_set.get(tkinter.ACTIVE)
        song = f'C:/Users/kloke/OneDrive/Desktop/UoSM/SEM2/33/python2/Labwork2/songs_db/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        
        song_length()
    play_img = tkinter.PhotoImage(file=r'C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\resources\play.png')
    play_btn = tkinter.Button(controls_frame, image=play_img, borderwidth=0, command=play)

    # Pause Button
    global paused
    paused = False

    def pause(is_paused):
        global paused
        paused = is_paused

        if paused:
            pygame.mixer.music.unpause()
            paused = False

        else:
            pygame.mixer.music.pause()
            paused = True
    pause_img = tkinter.PhotoImage(file=r'C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\resources\pause.png')
    pause_btn = tkinter.Button(controls_frame, image=pause_img, borderwidth=0, command=lambda:pause(paused))
    

    # Stop Button
    def stop():
        pygame.mixer.music.stop()
        playlist_set.selection_clear(tkinter.ACTIVE)
    stop_img = tkinter.PhotoImage(file=r'C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\resources\stop.png')
    stop_btn = tkinter.Button(controls_frame, image=stop_img, borderwidth=0, command=stop)


    # Next Song Button
    def forward():
        current_song = playlist_set.curselection()
        next_song = current_song[0]+1
        song = playlist_set.get(next_song)

        song = f'C:/Users/kloke/OneDrive/Desktop/UoSM/SEM2/33/python2/Labwork2/songs_db/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        # make the selection bar to move and highlight the new song
        playlist_set.selection_clear(0, tkinter.END)
        playlist_set.selection_set(next_song, last=None)
        playlist_set.activate(next_song)
    forward_img = tkinter.PhotoImage(file=r'C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\resources\forward.png')
    forward_btn = tkinter.Button(controls_frame, image=forward_img, borderwidth=0, command=forward)


    # Previous Song Button
    def backward():
        current_song = playlist_set.curselection()
        next_song = current_song[0]-1
        song = playlist_set.get(next_song)

        song = f'C:/Users/kloke/OneDrive/Desktop/UoSM/SEM2/33/python2/Labwork2/songs_db/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        # make the selection bar to move and highlight the new song
        playlist_set.selection_clear(0, tkinter.END)
        playlist_set.selection_set(next_song, last=None)
        playlist_set.activate(next_song)
    backward_img = tkinter.PhotoImage(file=r'C:\Users\kloke\OneDrive\Desktop\UoSM\SEM2\33\python2\Labwork2\resources\backward.png')
    backward_btn = tkinter.Button(controls_frame, image=backward_img, borderwidth=0, command=backward)


    # Position of the buttons
    backward_btn.pack(side=tkinter.LEFT)
    stop_btn.pack(side=tkinter.LEFT)
    play_btn.pack(side=tkinter.LEFT)
    pause_btn.pack(side=tkinter.LEFT)
    forward_btn.pack(side=tkinter.LEFT)
    
    controls_frame.pack(pady=5) 
    #to put the buttons that are in the controls_frame frame in the frame with the playlist_set

    # Menu Bar
    menu_bar = tkinter.Menu(music_player)
    music_player.config(menu=menu_bar)

    # add songs
    add_song_menu = tkinter.Menu(menu_bar)
    def add_songs():
        songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose Songs",  filetypes=(("mp3 Files", "*.mp3"), ))

        for song in songs:
            song = song.replace("C:/Users/kloke/OneDrive/Desktop/UoSM/SEM2/33/python2/Labwork2/songs_db/", "")
            song = song.replace(".mp3", "")
            playlist_set.insert(tkinter.END, song)

            user_filepath = f'C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\songs_db\\{song}.mp3'
            test = f'C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\{email[:-10]}\\'
            shutil.copy2(user_filepath,test)


    menu_bar.add_cascade(label="Add Songs", menu=add_song_menu, command=add_songs)
    add_song_menu.add_command(label="Add Songs To Playlist", command=add_songs)


    # Delete the song
    delete_song_menu = tkinter.Menu(menu_bar)
    menu_bar.add_cascade(label="Delete Songs", menu=delete_song_menu)

    # Delete a song
    def delete_songs():
        # deletes the song selected
        song = playlist_set.get(tkinter.ANCHOR)
        playlist_set.delete(tkinter.ANCHOR)
        pygame.mixer.music.stop()

        song_path = f'C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\{email[:-10]}\\{song}.mp3'
        if os.path.exists(song_path):
            os.remove(song_path)

    # Delete all songs in the playlist_set
    def delete_all_songs():
        # deletes all the songs in the playlist
        pygame.mixer.music.stop()
        songs = playlist_set.get(0, tkinter.END)

        for song in songs:
            song_path = f'C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM2\\33\\python2\\Labwork2\\{email[:-10]}\\{song}.mp3'
            os.remove(song_path)

        playlist_set.delete(0, tkinter.END)

    delete_song_menu.add_command(label="Delete Songs", command=delete_songs)
    delete_song_menu.add_command(label="Delete All Songs", command=delete_all_songs)

    # Volume
    def volume(x):
        pygame.mixer.music.set_volume(volume_slider.get())

    def update_volume(event):
        volume_level = volume_slider.get()
        pygame.mixer.music.set_volume(volume_level / 100)

    volume_slider = tkinter.Scale(playlist_set_n_volume_frame, from_=100, to=0, orient=tkinter.VERTICAL, command=volume)
    volume_slider.pack(side=tkinter.LEFT, padx=5, pady=10)
    volume_slider.bind('<Motion>', update_volume)

    music_player.mainloop()


# blocking in case the email dosen't get in
if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
        start_music_player(email)
    else:
        print("No email provided.")