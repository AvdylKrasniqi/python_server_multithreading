from random import randint
import socket, threading, datetime, math

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("Nje klient i ri u kyq: ", clientAddress)

    def countMessage(self, message):
        zanoret = {}
        bashktingelloret = {}

        for zanore in "aeiouy":
            count = message.count(zanore)
            zanoret[zanore] = count

        for bashktingellore in "bcdfghjklmnprqstvwxz":
            count = message.count(bashktingellore)
            bashktingelloret[bashktingellore] = count
        
        return "Gjithesej bashktingellore " + str(sum(bashktingelloret.values())) + " dhe zanore " + str(sum(zanoret.values()))

    def convertLength(self, method, number):
        if(method == "cmtofeet"):
            return str(0.0328084*number)
        elif(method == "feettocm"):
            return str(30.48*number)
        elif(method == "kmtomiles"):
            return str(0.621371*number)
        elif(method == "miletokm"):
            return str(1.60934*number)
        else:
            return "Opsioni eshte i gabuar. Opsionet valide jane: cmToFeet, feetToCm, kmToMiles, mileToKm"

    def help(self):
        return "\nipaddress\nport\ncount teksti\nreverse teksti\npalindrome teksti\ntime\ngame\ngcf nr1 nr2\nconvert options nr\nmax nr1 nr2\nexit"
        
    def max(self, nr1, nr2):
        if nr1 > nr2:
            return str(nr1)
        elif nr1 == nr2:
            return "Baraz"
        else:
            return str(nr2)

    def game(self):
        numrat = []
        while len(numrat) <= 5:
            nr = randint(1,35)
            if nr in numrat:
                continue
            else:
                numrat.append(nr)
        numrat.sort()
        return ' '.join(str(v) for v in numrat)

    def reverseText(self, message):
        return message[::-1].strip()

    def run(self):
        print ("Konektimi nga: ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            if len(data) > 128:
                self.csocket.send(bytes("Gjatesia e mesazhit me e madhe se 128 nuk eshte e lejuar",'UTF-8'))
            msg = data.decode()
            msg = msg.lower()
            print ("Nga klienti me IP ", clientAddress, " mesazhi: ", msg)
            if msg=='exit':
              break
            elif msg =='ipaddress':
                msg = clientAddress[0]
            elif msg =='port':
                msg = str(clientAddress[1])
            elif str(msg.split(' ', 1)[0]) =='count':
                try:
                    msg = self.countMessage(str(msg.split(' ', 1)[1]))
                except Exception as e:
                    print(e)
                    msg = "Argumenti 1 mungon"


            elif str(msg.split(' ', 1)[0]) =='reverse':
                try:
                    msg = self.reverseText(str(msg.split(' ', 1)[1]))
                except Exception as e:
                    print(e)
                    msg = "Argumenti 1 mungon"



            elif str(msg.split(' ', 1)[0]) =='palindrome':
                try:
                    if msg.split(' ', 1)[1] == self.reverseText(msg.split(' ', 1)[1]):
                        msg = "Teksti eshte palindrom"
                    else:
                        msg = "Teksti nuk eshte palindrom"
                except Exception as e:
                    print(e)
                    msg = "Argumenti 1 mungon"


            elif str(msg) =='time':
                msg = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S %p'))

            elif str(msg) =='game':
                msg = self.game()

            elif str(msg.split(' ', 2)[0]) =='gcf':
                try:
                    nripare = int(msg.split(' ', 2)[1])
                    nridyte = int(msg.split(' ', 2)[2])
                    msg = str(math.gcd(nripare, nridyte))
                except Exception as e:
                    print(e)
                    msg = "Argumenti 1 ose 2 mungon/Sigurohuni qe jeni duke shkruar numra"

            elif str(msg.split(' ', 2)[0]) =='convert':
                try:
                    opsioni = str(msg.split(' ', 2)[1])
                    numri = int(msg.split(' ', 2)[2])
                    msg = self.convertLength(opsioni, numri)
                except Exception as e:
                    print(e)
                    msg = "Argumentet mungojne."
            elif msg == 'connectiontest':
                msg = "Konektimi u be me sukses"

            elif str(msg.split(' ', 2)[0]) =='max':
                try:
                    nripare = int(msg.split(' ', 2)[1])
                    nridyte = int(msg.split(' ', 2)[2])
                    msg = self.max(nripare, nridyte)
                except Exception as e:
                    print(e)
                    msg = "Argumenti 1 ose 2 mungon/Sigurohuni qe jeni duke shkruar numra"

            elif msg == 'help':
                msg = self.help()
            else:
                msg = "Nuk ekziston kjo komande. Shkruani help per te kerkuar ndihme"
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Klienti ", clientAddress , " eshte diskonektuar...")
LOCALHOST = "127.0.0.1"
PORT = 13000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Serveri filloj te punoj\n Duke pritur per kliente")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()