#PROGRAM BY SHRIVATHSA
import tkinter
from tkinter import *
from tkinter import messagebox


global player
player = 1

#1 2 3
#4 5 6
#7 8 9

def do_nothing():
    pass

def check_victory():
    count = 0
    victory_combination = [[button1['text'], button2['text'], button3['text']], 
                           [button4['text'], button5['text'], button6['text']],
                           [button7['text'], button8['text'], button9['text']],
                           [button1['text'], button4['text'], button7['text']],
                           [button2['text'], button5['text'], button8['text']],
                           [button3['text'], button6['text'], button9['text']], 
                           [button1['text'], button5['text'], button9['text']],
                           [button3['text'], button5['text'], button7['text']]]
    for i in victory_combination:
        if (i[0]=="X" and i[1]=="X" and i[2] == "X"):
            tkinter.messagebox.showinfo("Game Over", "Player X won the game")
            root.quit()
        elif (i[0]=="O" and i[1]=="O" and i[2] == "O"):
            tkinter.messagebox.showinfo("Game Over", "Player O won the game")
            root.quit()
        else:
            if (i[0] !=" " and i[1] != " " and i[2] != " "):
                count +=1
    if count==8:
        tkinter.messagebox.showinfo("Game Over", "It is a tie")
        root.quit()
                        
def move(button):
    global player
    if player==1:
        player = 0
        button.config(text = "X")
        button.config(command = do_nothing)
        check_victory()
    else:
        player = 1
        button.config(text = "O")
        button.config(command = do_nothing)
        check_victory()

root = Tk()

            
button = StringVar()

button1 = Button(root, text = " ", command = lambda : move(button1), height = 4, width = 8)
button2 = Button(root, text = " ", command = lambda : move(button2), height = 4, width = 8)
button3 = Button(root, text = " ", command = lambda : move(button3), height = 4, width = 8)
button4 = Button(root, text = " ", command = lambda : move(button4), height = 4, width = 8)
button5 = Button(root, text = " ", command = lambda : move(button5), height = 4, width = 8)
button6 = Button(root, text = " ", command = lambda : move(button6), height = 4, width = 8)
button7 = Button(root, text = " ", command = lambda : move(button7), height = 4, width = 8)
button8 = Button(root, text = " ", command = lambda : move(button8), height = 4, width = 8)
button9 = Button(root, text = " ", command = lambda : move(button9), height = 4, width = 8)


button1.grid(row = 0, column = 0, sticky = S+N+E+W)
button2.grid(row = 0, column = 1, sticky = S+N+E+W)
button3.grid(row = 0, column = 2, sticky = S+N+E+W)
button4.grid(row = 1, column = 0, sticky = S+N+E+W)
button5.grid(row = 1, column = 1, sticky = S+N+E+W)
button6.grid(row = 1, column = 2, sticky = S+N+E+W)
button7.grid(row = 2, column = 0, sticky = S+N+E+W)
button8.grid(row = 2, column = 1, sticky = S+N+E+W)
button9.grid(row = 2, column = 2, sticky = S+N+E+W)


root.mainloop()