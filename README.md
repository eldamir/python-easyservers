python-easyservers
==================

The easy way to create servers and client for any task with python.

The server
----------

When making a server, simply define function that determines what to do when the server receives a message.

Let the function use these parameters

```python
def server_message_handler(message, address, send):
    pass
```

The `message` is the message received from a client. The `address` is the address that the message was received from. `send` is a method that can be used to send a message from the server. Use it like this:

```python
send("My message", address)
```

An address is simply a tuple of IP and port: `("123.456.798", 1234)`

A full example of a chat app is seen below. The `server_handle` method is the method that the server runs. At the bottom of the example, you can see how to strap the function into the server:

```python
from udpserver import UDPServer
from easy_threading import FunctionThread
import time

logged_in_users = []

def server_handle(msg, addr, send):
    """
    Defines what to do when receiving a message from the client
    """
    parts = msg.split()

    sender = None
    for user, user_address, ping_counter in logged_in_users:
        if user_address == addr:
            sender = user

    if parts[0] == "JOIN":
        print("[DEBUG] Interpreting JOIN request")
        username = msg[len(parts[0])+1:]

        name_taken = False
        for user, user_address, ping_counter in logged_in_users:
            if user == username:
                name_taken = True
                break

        if name_taken:
            send("JERR NAME TAKEN", addr)
        else:
            logged_in_users.append([username, addr, 0])
            send("JOK", addr)

    elif parts[0] == "MSGA":
        print("[DEBUG] Interpreting MSGA request")
        _msg = "(%s) "%sender + " ".join(parts[1:])
        for user, user_address, ping_counter in logged_in_users:
            send(_msg, user_address)

    elif parts[0] == "MSGP":
        print("[DEBUG] Interpreting MSGP request")
        send_to_name = msg[msg.find("(")+1:msg.find(")")]
        print("[DEBUG] Sending to %s"%send_to_name)
        _msg = "(%s) "%sender + msg[msg.find(")")+1:].strip()
        address = None
        for user, user_address, ping_counter in logged_in_users:
            if user == send_to_name:
                # Send to recipient
                send(_msg, user_address)
                # Echo back to sender aswell
                send(_msg, addr)
                break
        else:
            print("[WARN ] Unknown recipient. Ignoring MSGP request")

    elif parts[0] == "EXIT":
        print("[DEBUG] Interpreting EXIT request")
        for i in range(len(logged_in_users)):
            user, user_address, ping_counter = logged_in_users[i]
            if user_address == addr:
                # Remove logged in user
                del logged_in_users[i]
        else:
            print("[WARN ] EXIT came from unknown address. Ignoring")

    elif parts[0] == "PONG":
        print("[DEBUG] Interpreting PONG request")
        for i in range(len(logged_in_users)):
            user, user_address, ping_counter = logged_in_users[i]
            if user_address == addr:
                # Remove logged in user
                logged_in_users[i][2] = 0
                break
        else:
            print("[WARN ] PONG came from unknown address. Ignoring")

def ping_clients(server):
    while 1:
        for i in range(len(logged_in_users)):
            user, user_address, ping_counter = logged_in_users[i]
            print "[DEBUG] sending PING to %s"%str(user_address)
            server.send("PING", user_address)
            logged_in_users[i][2] += 1
            if logged_in_users[i][2] > 3:
                print "[DEBUG] Removing %s, since he didn't respond to PING"%str(user_address)
                del logged_in_users[i]
        time.sleep(10)

if __name__ == '__main__':
    # Create a server that uses server_handle on port 1234
    server = UDPServer(server_handle, port=1234)
    
    # Make the server run ping_clients in another thread
    server.create_thread(ping_clients, (server,))
    
    # Run the server
    server.run()
```

Simply create the server with the desired function and port. In this example, we want the server to do something other than respond to a request. To that end, we defined the function `ping_clients`, and strapped it into the server by using `create_thread`. What this does is to simply run the function in its own thread. If you do not want to run the thread instantly, pass the start option:

```python
thread = server.create_thread(ping_client, (server,), start=False)
# Thread is not yet started. Start it by doing
thread.start()
```

The run method will block the main thread and run an infinite loop, responding to requests as they come in.

the client
----------
