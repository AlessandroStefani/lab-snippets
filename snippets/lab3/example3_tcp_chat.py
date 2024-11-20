from snippets.lab3 import *
import sys

mode = sys.argv[1].lower().strip() #Non deve servire
# mode = 'server' # oppure always server e modifichiamo un po'
#remote_peer: Client | None = None

remote_peers = set() #TODO



def send_message(msg, sender):
    if remote_peers.__len__() == 0:
        print("No peer connected, message is lost")
    elif msg:
        for peer in remote_peers:
            peer.send(message(msg.strip(), sender))# TODO
    else:
        print("Empty message, not sent")


def on_message_received(event, payload, connection, error):
    match event:
        case 'message':
            print(payload)
        case 'close':
            print(f"Connection with peer {connection.remote_address} closed")
            global remote_peers; remote_peers.remove(connection) #TODO
        case 'error':
            print(error)


if mode == 'server':
    port = int(sys.argv[2])
    connect_to = 0     

    def on_new_connection(event, connection, address, error):
        match event:
            case 'listen':
                print(f"Server listening on port {address[1]} at {', '.join(local_ips())}")
            case 'connect':
                print(f"Open ingoing connection from: {address}")
                connection.callback = on_message_received
                global remote_peers; remote_peers.add(connection)                
                #SEND PEERS
                #content = remote_peers
                #send_message(content, 'peering')
                
            case 'stop':
                print(f"Stop listening for new connections")
            case 'error':
                print(error)

    this = Server(port, on_new_connection)
    
    if sys.argv.__len__() == 4:
        connect_to = sys.argv[3]  
        
        
elif mode == 'client':
    remote_endpoint = sys.argv[2]
    this = Client(address(remote_endpoint), on_message_received)
    remote_peers.add(this)
    print(f"Connected to {this.remote_address}")


username = input('Enter your username to start the chat:\n')
print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
while True:
    try:
        content = input()
        send_message(content, username)
    except (EOFError, KeyboardInterrupt):
        if this:
            this.close()
        break
if mode == 'server':
    this.close()
