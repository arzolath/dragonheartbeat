"""
DragonHeartbeat - Show your heartbeat in your chatbox!
(c) 2024 Arzolath - Arzolath.com
"""
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import time
import threading

def send_text_to_vrchat(text):
    # VRChat OSC server IP and port
    ip = "127.0.0.1"
    port = 9000

    text = text + " bps"

    # Initialize OSC client
    client = udp_client.SimpleUDPClient(ip, port)

    # The OSC address for displaying text in the chatbox
    osc_address = "/chatbox/input"

    # Send the text message
    client.send_message(osc_address, [text, True, False])
    print(f"Sent to VRChat chatbox: {text}")

def handle_incoming_message(unused_addr, args, *values):
    text = ' '.join(map(str, values))
    print(f"Received message: {text}")
    send_text_to_vrchat(text)

def start_osc_server(server):
    # Create and start the OSC server
    server.serve_forever()

def main():
    server_ip = "127.0.0.1"
    server_port = 9002
    disp = dispatcher.Dispatcher()
    disp.map("/avatar/parameters/HR", handle_incoming_message, "Message")
    server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), disp)

    server_thread = threading.Thread(target=start_osc_server, args=(server,))
    server_thread.start()
    
    print("Press CTRL+C to stop the server.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()  # This will stop the server loop
        server.server_close()  # Close the server socket
        server_thread.join()  # Wait for the server thread to finish
        print("Shutting down the server.")

if __name__ == "__main__":
    main()