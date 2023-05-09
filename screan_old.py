import os
import tkinter as tk
from tkinter import messagebox
# Sample data
networks = {"aa:bb:cc:dd:ee":"ofek","aa:bb:cc:dd:ff":"ofek2"}
users = {"a2:b2:c2:d2:e2":"aa:bb:cc:dd:ee","a1:b1:c1:d1:e1":"aa:bb:cc:dd:ee","a1:b1:c1:d1:f1":"aa:bb:cc:dd:ff"}
def main():
    global selected_network_var, selected_user_var, selected_network_name_var
    selected_network_var = None
    selected_user_var = None
    selected_network_name_var = None
    print("interfaces list:")
    os.system("iwconfig")
    print("Enter the network interface to use as the attacker")
    attack_card = input()
    print("Enter the network interface to use as an AP")
    ap_card = input()    
    print("Enter the network interface to forword the AP trafic to")
    connected_card = input()
    # TODO: scan the network for 1 minute 
main()


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
    network_listbox.insert(tk.END, network+","+names)
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
# Function to display the selected network and associated users
def show_users(event):
    if network_listbox.curselection() != ():
        # Get the selected network
        selected_network = network_listbox.get(network_listbox.curselection()[0])
        selected_network_name = selected_network.split(',')[1]
        network_key = selected_network.split(',')[0]
        # Find all users associated with the selected network
        associated_users = [k for k,v in users.items() if v == network_key]
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
