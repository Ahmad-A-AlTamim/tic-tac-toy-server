import socket
import  os
from threading import Thread
from threading import RLock
import pickle
from time import sleep
playersList=[]
listIsChanged=False
id=100
class clientThread(Thread):
    def __init__(self,clientSocket,addr):
        global id
        Thread.__init__(self)
        self.cSock=clientSocket
        self.addr=addr
        self.isBusy=False
        self.isReady=False
        self.secondPlayer=None
        self.name=self.cSock.recv(2048).decode().replace("New:","")
        self.cSock.send("name received".encode())
        self.id=int(self.cSock.recv(2048).decode())
        print(self.id)
        self.board=[[" "," "," "],[" "," "," "],[" "," "," "]]
        if self.id==0:
            self.id=id+1
            id+=1
        self.cSock.send("connected...".encode())
        self.cSock.send(str(self.id).encode())
        playersList.append([self.id,self.name,self])
        self.printPlayers()

    def sendPlayersList(self):
        counterReady=0
        for i in playersList:
            if i[2].isReady:
                counterReady+=1
        self.cSock.send(str(counterReady).encode())
        for i in playersList:
            if i[2].isReady:
                self.cSock.send((f"id: {i[0]} name: {i[1]}\n").encode())

    def printPlayers(self):
        os.system('cls')
        print("Number of online Players is:",len(playersList))
        print("Players:")
        for i in playersList:
            print("id:",i[0]," name:",i[1]," address:",i[2].addr," is ready")

    # def printBoard(self):
    #     print("===============")
    #     for i in self.board:
    #         print(i)
    #     print("===============")
        

    
    def gameEngine(self):
        msg=""
        
        if self.secondPlayer!=None:
            self.secondPlayer[2].cSock.send("O".encode())
        while msg!="end":


            

            self.board=pickle.loads(self.cSock.recv(2048))  
            

            data=pickle.dumps(self.board)
            self.secondPlayer[2].cSock.send(data)
            if msg =="end":
                self.cSock.send(msg.encode())
        self.isBusy=False
        self.isReady=False
        
        pass   
    def run(self):
        while self.cSock.getsockopt(socket.SOL_SOCKET,socket.SO_ERROR)==0:  
            try:
                msg=self.cSock.recv(2048).decode()
                if len(msg)>0:#to avoid  ctrl+c interrupt
                    pass
                if msg=="waiting for player":
                    self.isReady=True
                    self.isBusy=False
                    self.gameEngine()
                    continue
                if msg =="exit":
                    self.cSock.send("disconnect".encode())
                    break
                if msg=="Send$xx$Online$xx$Players$Token":
                    self.sendPlayersList()
                    continue
                if int(msg) in [i[0] for i in playersList]:
                    self.secondPlayer=[i for i in playersList if i[0]==int(msg)][0]
                    if self.secondPlayer[2].isBusy:
                        self.cSock.send("Player is busy".encode())
                    else:
                        if self.secondPlayer[2].isReady:

                            self.isBusy=True
                            self.secondPlayer[2].isBusy=True
                            self.secondPlayer[2].isReady=False
                            self.secondPlayer[2].secondPlayer=[self.id,self.name,self]
                            self.cSock.send("Ready$xx$To$xx$Start$xx$Chat$Token".encode())
                            self.gameEngine()
                            continue
                        else:
                            self.cSock.send("Player not ready".encode())
                else:
                    self.cSock.send("Player not found".encode())

            except Exception as e:
                print("error:",e)
                break
        self.cSock.close()
        playersList.remove([self.id,self.name,self])
        self.printPlayers()




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',100))
print("server run ...")
while True:
    s.listen(50)
    clientSocket,addr=s.accept()
    print("connected to:",addr)
    newThread=clientThread(clientSocket,addr)
    newThread.start()

