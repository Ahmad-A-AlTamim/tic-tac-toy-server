import socket
import os
from threading import Thread
from  time import sleep
import pickle

os.system('cls')
print("Enter your name")
name=input()
msg=""
id=0
while msg!="exit":
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    os.system("cls")
    s.connect(('127.0.0.1',100))
    s.send((f"New:{name}").encode())
    x=s.recv(2048).decode()
    s.send(str(id).encode())
    board=[[" "," "," "],[" "," "," "],[" "," "," "]]
    x=s.recv(2048).decode()
    print(x)

    yourCharacter=""
    id=s.recv(2048).decode()
    off=0

    def receiveUsers():
        os.system("cls")
        s.send("Send$xx$Online$xx$Players$Token".encode())
        playersCount=s.recv(2048).decode()
        print("your id is:",id)
        print("Number of online Players is:",playersCount,'\n')
        print("===============Players===============\n")
        if int(playersCount)==0:
            print("No players online")
        else:    
            for i in range(int(playersCount)-(int(playersCount)-1)):

                ss=str(s.recv(2048).decode())
                print(ss)
        print("=====================================")
        print("\n")

    def checkWinner():
        global board
        for row in board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]
        
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != " ":
                return board[0][col]
        
        if board[0][0] == board[1][1] == board[2][2] != " ":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != " ":
            return board[0][2]
        
        if all(cell != " " for row in board for cell in row):
            return "Tie"
        
        return None


    def printBoard():
        os.system('cls')
        print("===============")
        for i in board:
            print(i)
        print("===============")
        
    def playing():
        global board
        global off
        x="waiting for player"
        s.send(x.encode())
        i=0
        while True:

            if i==0:
                os.system('cls')
                print(x)
                yourCharacter=s.recv(2048).decode()
                print("Game started")         
                printBoard()
                print("You are playing with",yourCharacter)
                print("x turn")
            i+=1

            board=pickle.loads(s.recv(2048))
            printBoard()
            if checkWinner()!=None:
                if checkWinner()!="Tie":
                    print(checkWinner(),"is winner")
                else:
                    print("Tie")
                sleep(5)
                break  
            while True:
                print("Enter the position you want to play x,y 1 to 3")
                text=input()
                if text=="end" or (len(text)>2 and text[0]>='1' and text[0]<='3' and text[2]>='1' and text[2]<='3' and board[int(text[0])-1][int(text[2])-1]==" "):
                    text+=yourCharacter
                    print(board[int(text[0])-1][int(text[2])-1])
                    board[int(text[0])-1][int(text[2])-1]=text[3]
                    data=pickle.dumps(board)
                    s.send(data)
                    printBoard()
                    break
                else:
                    print("Enter a valid position")
            if checkWinner()!=None:
                if checkWinner()!="Tie":
                    print(checkWinner(),"is winner")
                else:
                    print("Tie")
                sleep(5)
                break                
        # print("exit")
        off=1
        s.close()

        
    def playing2():
        x=""
        yourCharacter="X"
        printBoard()
        print("You are playing with",yourCharacter)
        print("x turn")
        global board
        global off
        while True:


            while True:
                print("Enter the position you want to play x,y 1 to 3")
                text=input()
                if text=="end" or (len(text)>2 and text[0]>='1' and text[0]<='3' and text[2]>='1' and text[2]<='3' and board[int(text[0])-1][int(text[2])-1]==" "):
                    text+=yourCharacter
                    board[int(text[0])-1][int(text[2])-1]=text[3]
                    data=pickle.dumps(board)
                    s.send(data)
                    printBoard()
                    break
                else:
                    print("Enter a valid position")
            if checkWinner()!=None:
                if checkWinner()!="Tie":
                    print(checkWinner(),"is winner")
                else:
                    print("Tie")
                sleep(5)
                break 
            
            board=pickle.loads(s.recv(2048))
            printBoard()
            if checkWinner()!=None:
                if checkWinner()!="Tie":
                    print(checkWinner(),"is winner")
                else:
                    print("Tie")
                sleep(5)
                break 
        off=1
        s.close()




    while True and off==0:
        try:
            receiveUsers()
            print("Enter a player id to play \nplay to enter play list \nor type exit to exit \nor type refresh to refresh the list of online players  \n" ) 
            msg=input()
            print("\n")

            if msg=='exit':
                s.send(msg.encode())
                x=s.recv(2048).decode()
                print(x)
                break
            if msg=='refresh':
                continue
            if msg==str(id):
                print("You can't search for yourself")
                sleep(2)
                continue
            if msg=='play':
                playing()
                break
            if not msg.isdigit():
                print("Enter a valid id")
                sleep(2)
                continue
            s.send(msg.encode())
            x=s.recv(2048).decode()
            if x=="Ready$xx$To$xx$Start$xx$Chat$Token":
                os.system('cls')
                print("Game started")
                playing2()
                break
        except:
            #ctrl c or disconnect from client side
            s.send("exit".encode())
            # x=s.recv(2048).decode()
            print(x)
            # sleep(15)
            break

    s.close()