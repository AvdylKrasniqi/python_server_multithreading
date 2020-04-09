from random import randint
import socketserver , threading, time, datetime, math

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
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
            return "Opsioni eshte i gabuar. Opsionet valide jane: cmtofeet, feettocm, kmtomiles, miletokm"

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

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))

        msg = data.decode("utf-8")
        if msg =='ipaddress':
            msg = self.client_address[0]
        elif msg =='port':
            msg = str(self.client_address[1])
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
        socket.sendto(bytes(msg, 'UTF-8'), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8888

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()