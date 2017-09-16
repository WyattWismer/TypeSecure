import pickle
import pyHook
import pythoncom
import time


#Load identity
name = raw_input("User identity to be loaded: ")

iden = {}
with open(name+'.pkl','rb') as pkl:
    iden = pickle.load(pkl)

#Constants
KEY_TIMEOUT = 5 #Seconds
OLD_BIAS = 0.9
ERROR_THRESHOLD = 0.18


#Maintain current word
word = ""
timing = []
last_time = time.time()

#Detecting error
error_total = 0
error_skew_total = 0
words = 0


#Handle typing detection
def OnKeyboardEvent(event):
    global last_time, word, timing, name, words, error_total, error_skew_total
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
            pass
            #iden[word] = timing[:]
        else:
            #update
            print len(timing)
            #iden[word] = [ OLD_BIAS * iden[word][i] + (1 - OLD_BIAS) * timing[i] for i in range(len(timing))]
            words += 1
            word_time = sum(timing)
            error_total += sum([abs(timing[i]-iden[word][i]) for i in range(len(timing))])
            if len(timing) > 1:
                error_skew_total += abs( (max(timing)-min(timing)) - (max(iden[word])-min(iden[word])) )
            if words > 30 and error_total/float(words) > ERROR_THRESHOLD:
                print "You are a suspicious person"
                print "Regular Error", error_total/float(words)
                print "Skew", error_skew_total/float(words)
        #print word, iden[word]
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



