import pickle


iden = {}

name = raw_input("Enter an identity: ")

with open('english.txt','r') as language:
    for line in language:
        word = line.strip()
        iden[word] = None

with open(name+'.pkl','wb') as output:
    pickle.dump(iden, output)
