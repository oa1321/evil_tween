from scapy.all import *
from threading import Thread
import os 
from time import sleep
class Defance:


    listen_iface = ''
    listen_mac = ''

    chanel_number = 0
    users = dict()
    user_to_network = dict()

    def __init__(self,listen_iface, listen_mac) -> None:
        self.listen_iface = listen_iface
        self.listen_mac = listen_mac

    def change_channel(self):
        while 1:
            time.sleep(3)
            os.system(f"iwconfig {self.listen_iface} channel {self.chanel_number+1}")
            self.chanel_number = (self.chanel_number+1)%13

    def kill_wifi(self, target_mac, gateway_mac):
        dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac,type=0, subtype=12)
        # stack them up
        pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
        # send the packet
        sendp(pkt, count=70000, iface=self.listen_iface, verbose=3)

    def sniff_attack(self):
        def print_packet(pkt):
            if pkt.haslayer(Dot11Deauth):
                if self.users.get(pkt.addr1,False):
                    self.users[pkt.addr1] += 1
                else:
                    self.users[pkt.addr1] = 1
                    self.user_to_network[pkt.addr1] = pkt.addr2
                if self.users[pkt.addr1] % 1000 == 0:
                    print(pkt.addr1 + " is attacked now! "+ str(self.users[pkt.addr1]))

            if pkt.haslayer(Dot11Auth):
                print(pkt.addr1, pkt.addr2)
                if self.users.get(pkt.addr2,False):
                    if pkt.addr1 != self.user_to_network[pkt.addr2]: 
                        print("A vicitem connecting to suspisce network, dissconnect him!")
                        self.kill_wifi(pkt.addr2, pkt.addr1)
                       

        x = Thread(target=self.change_channel, args=())
        x.start()
        sniff(iface = self.listen_iface,prn = print_packet)
        x.join()

        

#b4:b5:b6:f2:4d:17
#b6:4c:4a:86:33:24
os.system("ip l")
print("enter the network interface and mac")
x = input()#interface
y = input()#mac

a = Defance(x,y)
a.sniff_attack()
#a.kill_wifi('b4:b5:b6:f2:4d:17','b6:4c:4a:86:33:24')
#a.reset_ap()
#a.beacon_packet("ofek - for real","enp3s0")
#sleep(60)
#a.reset_ap()