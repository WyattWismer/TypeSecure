import pickle
import pyHook
import pythoncom
import time

#Load identity
name = raw_input("Enter identity to be trained: ")

iden = {}
with open(name+'.pkl','rb') as pkl:
    iden = pickle.load(pkl)

#Constants
KEY_TIMEOUT = 5 #Seconds
OLD_BIAS = 0.9

#Maintain current word
word = ""
timing = []
last_time = time.time()


#Handle typing detection
def OnKeyboardEvent(event):
    global last_time, word, timing, name
    #check if letter
    if (event.Ascii >= 65 and event.Ascii <= 90) or (event.Ascii >= 97 and event.Ascii <= 122):
        if time.time() - last_time < KEY_TIMEOUT:
            word += chr(event.Ascii)
            if len(word) > 1:
                timing.append(time.time() - last_time)
            last_time = time.time()
            #print "IN", word, last_time
            return True

        #TIMEOUT - reset word
        word = chr(event.Ascii)
        timing = []
        last_time = time.time()
        #print "TIMEOUT", word, timing, last_time
        return True
        
    #submit word
    if len(word) > 0 and word in iden:
        if iden[word] == None:
            #set
            iden[word] = timing[:]
        else:
            #update
            print len(timing)
            iden[word] = [ OLD_BIAS * iden[word][i] + (1 - OLD_BIAS) * timing[i] for i in range(len(timing))]
        print word, iden[word]
    elif word == "savetraining":
        with open(name+'.pkl','wb') as output:
            pickle.dump(iden, output)
        print "Saved Training Data"
    #Clean
    word = ""
    timing = []
    
    

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()



