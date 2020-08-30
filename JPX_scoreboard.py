from tkinter import *
from random import *
import time
import datetime
import pyttsx3
import math
from PIL import Image, ImageTk

# score needed to win
winning_score = 11

# scale factor for displaying on different sized screens
scale = 1.5

tit_font      = "Harry P"
tit_font_size = round(120*scale)

lab_font      = "Harry P"
lab_font_size = round(60*scale)

sco_font      = "Seven Segment"
sco_font_size = round(140*scale)

tim_font      = "Seven Segment"
tim_font_size = round(120*scale)

# gloabal vars
score_checked = 0
timer_set     = 0
blinking      = 0
timing        = 0

#function to build the scoreboard in Tkinter
def make_scoreboard(root):
  print('making scoreboard')
  main_frame    = Frame(root,bg="black")

  Label(main_frame,text="JPX",anchor="center",font=(tit_font,tit_font_size),fg='white',bg="black",width=8).grid(row=0,column=1,columnspan=2)

  Label(main_frame,text="AWAY",font=(lab_font,lab_font_size),fg='white',bg="black",width=8).grid(row=1,column=0)
  away = Label(main_frame,text="0",font=(sco_font,sco_font_size),fg='orange',bg="black",width=3)
  away.grid(row=2,column=0)

  Label(main_frame,text="HOME",font=(lab_font,lab_font_size),fg='white',bg="black",width=8).grid(row=1,column=4)
  home = Label(main_frame,text="0",font=(sco_font,sco_font_size),fg='green',bg="black",width=3)
  home.grid(row=2,column=4)
  
  timer = Label(main_frame,text="<-  ",font=(tim_font,tim_font_size),fg='red',bg="black",width=5)
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
  if(seconds == 5):
    timer["text"] = "5.0"
  else:
    timer["text"] = "2.0"
  
def run_timer():
  global timer_set
  global timing
  timing = 1
  seconds = float(timer["text"])
  time_left = seconds
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
  audio.say("Stop Drinking, Bitch!")
  audio.runAndWait()
  timer_set = 0
  timing = 0
  
  
  
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
  
  button = event.char
  
  if(button != "" and blinking == 0 and timing == 0):
    
    home_score = int(home["text"])
    away_score = int(away["text"])
    
    if(timer["text"] == "5.0" or timer["text"] == "2.0"):
      if(timer["text"] == "5.0"):
        home_score = 0
        away_score = 0     
      run_timer()
      home["text"] = str(home_score)
      away["text"] = str(away_score)
      change_serve()
      
      
    else:
   
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
          


      elif(button == "2"):
        set_timer(2)
        timer_set = 1

      #change serve
      elif(button == "8"):
          change_serve()
          
      
      home["text"] = str(home_score)
      away["text"] = str(away_score)
      root.update()
      
      if(score_checked == 0 and ((home_score == 9 and away_score == 6) or (home_score == 6 and away_score == 9))):
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
  root = Tk()
  root.title("JPX Scoreboard")
  root.configure(bg="black")
  audio = pyttsx3.init()
  voices = audio.getProperty('voices')
  audio.setProperty('voice', voices[1].id)

  [home, away, timer] = make_scoreboard(root)


  root.bind("<Key>",score_update)
  
  #Make countdown timer
  countdown = Label(root,text="",font =(lab_font,48),fg="white",bg="black",anchor="center")
  countdown.pack()
  root.mainloop()
