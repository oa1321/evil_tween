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
                        print("A vicitem connecting to suspisce network")

        x = Thread(target=self.change_channel, args=())
        x.start()
        sniff(iface = self.listen_iface,prn = print_packet)
        x.join()

        

#b4:b5:b6:f2:4d:17
#b6:4c:4a:86:33:24
a = Defance('wlxc4e9841c43b9','c4:e9:84:1c:43:b9')
a.sniff_attack()
#a.kill_wifi('b4:b5:b6:f2:4d:17','b6:4c:4a:86:33:24')
#a.reset_ap()
#a.beacon_packet("ofek - for real","enp3s0")
#sleep(60)
#a.reset_ap()