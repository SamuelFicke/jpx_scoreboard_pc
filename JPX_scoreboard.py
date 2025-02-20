from tkinter import *
from random import *
import time
import datetime
import pyttsx3 # text to speech
from playsound import playsound
import math
from PIL import Image, ImageTk

# score needed to win
winning_score = 11

tit_font      = "Harry P"
tit_font_size = round(120)

lab_font      = "Harry P"
lab_font_size = round(60)

sco_font      = "Seven Segment"
sco_font_size = round(130)

tim_font      = "Seven Segment"
tim_font_size = round(120)

title = "JPX"

# gloabal vars
score_checked = 0
timer_set     = 0
blinking      = 0
timing        = 0
first_server  = "away"

# load all the wave files
use_wav = True
use_explicit = True

wav_321go    = "audio/321go.wav"
wav_easports = "audio/EASports.wav"
wav_nice     = "audio/nice.wav"
if(use_explicit):
  wav_stop     = "audio/stop_drinking_explicit.wav"
else:
  wav_stop     = "audio/stop_drinking.wav"

#function to build the scoreboard in Tkinter
def make_scoreboard(root):
  main_frame    = Frame(root,bg="black")

  # scale factor for displaying on different sized screens
  pixel_width = root.winfo_screenwidth()
  scale = pixel_width/1100


  Label(main_frame,text=title,anchor="center",font=(tit_font,int(scale*tit_font_size)),fg='white',bg="black",width=9).grid(row=0,column=1,columnspan=2)

  Label(main_frame,text="AWAY",font=(lab_font,int(scale*lab_font_size)),fg='white',bg="black",width=8).grid(row=1,column=0)
  away = Label(main_frame,text="0",font=(sco_font,int(scale*sco_font_size)),fg='orange',bg="black",width=3)
  away.grid(row=2,column=0)

  Label(main_frame,text="HOME",font=(lab_font,int(lab_font_size*scale)),fg='white',bg="black",width=8).grid(row=1,column=4)
  home = Label(main_frame,text="0",font=(sco_font,int(scale*sco_font_size)),fg='green',bg="black",width=3)
  home.grid(row=2,column=4)
  
  timer = Label(main_frame,text="<-  ",font=(tim_font,int(tim_font_size*scale)),fg='red',bg="black",width=5)
  timer.grid(rowspan=2,columnspan=2,row=1,column=1)
  
  main_frame.pack(fill=X, padx=5, pady=5)

  return [home,away,timer]

#Adds 1 to label input
def add_lab(lab):
  score = lab["text"]
  lab["text"] = str(int(score)+1)
  
#Subtracts 1 from label input
def sub_lab(lab):
  score = lab["text"]
  lab["text"] = str(int(score)-1)

def set_timer(seconds):
  timer["text"] = f"{seconds:0.1f}"
  
def run_timer():
  global timer_set
  global timing
  timing = 1
  seconds = float(timer["text"])
  time_left = seconds
  if(use_wav):
    playsound(wav_321go)
  else:
    audio.say("3...2...1...GO")
    audio.runAndWait()
  end = time.time() + seconds
  while(time_left > 0):
      time_left = float(int(math.ceil((end - time.time())*10)))/10
      remaining = str(time_left)
      while(len(remaining) < 3):
        remaining += "0"
      timer["text"] = remaining
      root.update()
  if(use_wav):
    playsound(wav_stop)
  else:
    audio.say("Stop Drinking, Bitch!")
    audio.runAndWait()
  timer_set = 0
  timing = 0
  
def set_serve(team="away"):
  if(team == "home"):
    timer["text"] = "  ->"
  else:
    timer["text"] = "<-  "  
  
def get_serve():
  server = None
  if(timer["text"] == "  ->"):
    server = "home"
  else:
    server = "away"
  return server
  
  
def change_serve():
  if(timer["text"] == "<-  "):
    timer["text"] = "  ->"
  else:
    timer["text"] = "<-  "
  
#Blinks winner's score
def blink(team,num_blinks):
    global blinking
    
    blinking = 1
    
    if(team=="home"):
      temp = home["text"]
      for ii in range(num_blinks):
          home["text"] = ""
          root.update()
          time.sleep(0.25)
          home["text"] = temp
          root.update()
          time.sleep(0.25)
    else:
      temp = away["text"]
      for ii in range(num_blinks):
          away["text"] = ""
          root.update()
          time.sleep(0.25)
          away["text"] = temp
          root.update()
          time.sleep(0.25)
          
    blinking = 0
  
def score_update(event):

  global score_checked
  global timer_set
  global blinking
  global timing
  global first_server
  
  button = event.char
  
  if(button != "" and blinking == 0 and timing == 0):
    
    home_score = int(home["text"])
    away_score = int(away["text"])
    
    if(timer["text"] == "5.0" or timer["text"] == "2.0" or timer["text"] == "1.0" or timer["text"] == "1.5"):
      if(timer["text"] == "5.0"):
        home_score = 0
        away_score = 0
      run_timer()
      home["text"] = str(home_score)
      away["text"] = str(away_score)
      set_serve(first_server)
      
      
    else:
   
      # save state of server
      if(home_score == 0 and away_score == 0):
        first_server = get_serve()
   
      if(button == "7" and away_score < 99):
        score_checked = 0
        away_score += 1
        if((home_score+away_score) % 2 == 0 or (home_score+away_score) > 20 ):
          change_serve()
      elif(button == "1" and away_score > 0):
        score_checked = 0
        if((home_score+away_score) % 2 == 0 or (home_score+away_score) > 20 ):
          change_serve()
        away_score -= 1


      elif(button == "9" and home_score < 99):
        score_checked = 0
        home_score += 1
        if((home_score+away_score) % 2 == 0 or (home_score+away_score) > 20 ):
          change_serve()
      elif(button == "3" and home_score > 0):
        score_checked = 0
        if((home_score+away_score) % 2 == 0 or (home_score+away_score) > 20 ):
          change_serve()
        home_score -= 1
        
      # exit
      elif(button == "-"):
          root.destroy()
          exit()

      elif(button == "2"):
        set_timer(2)
        timer_set = 1
        
      elif(button == "="):
        set_timer(1)
        timer_set = 1
        
      elif(button == "+"):
        set_timer(1.5)
        timer_set = 1

      #change serve
      elif(button == "8"):
          change_serve()
      
      home["text"] = str(home_score)
      away["text"] = str(away_score)
      root.update()
      
      if(score_checked == 0 and ((home_score == 9 and away_score == 6) or (home_score == 6 and away_score == 9))):
        if(use_wav):
          playsound(wav_nice)
        else:
          audio.say("Nice!")
          audio.runAndWait()
        score_checked = 1

      if(home_score > winning_score-1 or away_score > winning_score-1):
        time.sleep(0.25)
        if(abs(home_score - away_score) > 1):
          if(home_score > away_score):
            set_timer(5)
            blink("home",5)
            timer_set = 1
          else:
            set_timer(5)
            blink("away",5)
            timer_set = 1




#Main function
if __name__ == "__main__":

  if(use_wav):
    # Create the ea sports window window
    window = Tk()
    window.attributes('-fullscreen', True)
    window.title("EA Sports")
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Load the image using Pillow
    image = Image.open("images/ea_sports.jpg")  # Replace with your image path
    image = image.resize((min(screen_width,screen_height), min(screen_width,screen_height)))
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = Label(window, image=photo)
    image_label.pack()

    # Keep a reference to the image object to prevent garbage collection
    image_label.image = photo

    # Run the Tkinter event loop
    window.after(250, lambda: playsound(wav_easports))
    window.after(4000, lambda: window.destroy())
    window.mainloop()
  else:
    audio = pyttsx3.init()
    voices = audio.getProperty('voices')
    audio.setProperty('voice', voices[1].id)


  # make real scoreboard 
  root = Tk()
  root.title("JPX Scoreboard")
  root.attributes('-fullscreen', True)
  root.configure(bg="black")  

  # put together scoreboard 
  [home, away, timer] = make_scoreboard(root)
  root.bind("<Key>",score_update)
  
  # make window capture key strokes
  root.focus_force()
  
  #Make countdown timer
  countdown = Label(root,text="",font =(lab_font,48),fg="white",bg="black",anchor="center")
  countdown.pack()
  root.mainloop()
