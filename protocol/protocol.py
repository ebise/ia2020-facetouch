import time
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class App(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        #Declare protocol
        self.protocol = ["Chin", "Forehead", "LeftCheek", "RightCheek"]
        self.dictate = self.prepare(self.protocol, 1)
        self.index = 0
        self.relativeTime = 0
        #File name to be written
        self.f = ""
        #Building the user interface
        self.lblProtocol = tk.Label(self, text = "", width = 10)
        self.lblProtocol.pack()
        self.lblCountdown = tk.Label(self, text = "", width = 10)
        self.lblCountdown.pack()
        self.remaining = 10
        self.btnStart = tk.Button(self, text="Start", command = self.toggle)
        self.btnStart.pack()
        self.btnRestart = tk.Button(self, text="Restart", command = self.restart)
        self.btnRestart.pack()
        self.paused = True
    
    #This method is invoked by Start button.
    #If it's at the beginning of the protocol, it'd create a new log file, if not, it'd just pause the timer
    def toggle(self):
        if self.paused:
            self.paused = False
            self.btnStart.config(text = "Pause")
            self.lblProtocol.config(text = self.dictate[self.index])
            if self.index == 0:
                now = datetime.now()
                date_time = now.strftime("%d_%m_%Y_%H_%M_%S")
                self.f = "Log_" + date_time + ".txt"
            self.writeFile()
            self.cd()
        else:
            self.paused = True
            self.btnStart.config(text = "Start")
    
    #This method is invoked by Restart button, it can only be used when the timer is paused.
    #This method reset all the configuration and reshuffle the protocol
    def restart(self):
        if self.paused:
            self.relativeTime = 0
            self.remaining = 10
            self.index = 0
            self.dictate = self.prepare(self.protocol)
            self.lblProtocol.config(text = "")
            self.lblCountdown.config(text = "")
    
    #This method start the timer on self.remaining variable
    #remaining: if not empty replace self.remaining with this value, if empty, use self.remaining
    def cd(self, remaining = None):
        if self.paused:
            return
        
        if remaining is not None:
            self.remaining = remaining
        
        if self.remaining >= 0:
            self.lblCountdown.configure(text = "%d" % self.remaining)
            self.remaining -= 1
            self.after(1000, self.cd)
        else:
            if self.index < (len(self.dictate)-1):
                self.index = self.index + 1
                self.writeFile()
                self.lblProtocol.config(text = self.dictate[self.index])
                self.remaining = 10
                self.cd()
    
    #This method repeat our protocol n times, randomize it and add opening and ending
    #protocol: list of our base protocol
    #n: how many our protocol repeated
    def prepare(self, protocol, n):
        l = []
        for i in range(n):
            l = l + protocol
        random.shuffle(l)
        l = ["Start", "Nose3times"] + l + ["Nose3times", "End"]
        return l
        
    #This method write the protocol and timestamp to the log file with format
    #"protocol,timestamp,relativeTime"
    def writeFile(self):
        with open(self.f, "a") as file:
             now = datetime.now()
             time = now.strftime("%H:%M:%S")
             file.write(self.dictate[self.index] + "," + time + "," + str(self.relativeTime) + "\n")
             self.relativeTime += 10
 
if __name__ == "__main__":
    app = App()
    app.title("FaceTouch - Protocol")
    app.geometry("500x400")
    app.mainloop()