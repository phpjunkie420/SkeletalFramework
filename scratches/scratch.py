from multiprocessing.connection import Listener, Client
import sys
import time

# The "Address" is actually a Windows Named Pipe in memory
# Syntax: r'\\.\pipe\<name_of_pipe>'
PIPE_ADDRESS = r'\\.\pipe\MyPythonControlPipe'
SECRET_PASSWORD = b'my_secret_password'  # Optional security


def run_client(arguments):
    """
    I run if the program is ALREADY open.
    I just pass the message and die.
    """
    try:
        print(f"[Client] Attempting to talk to main program...")

        # 1. Connect to the existing pipe
        conn = Client(PIPE_ADDRESS, authkey = SECRET_PASSWORD)

        # 2. Send the arguments (Python pickles them automatically)
        conn.send(arguments)

        print("[Client] Instructions sent. Exiting.")
        conn.close()
        return True  # Success

    except FileNotFoundError:
        # This error means the pipe doesn't exist yet.
        # Therefore, WE must be the main program.
        return False


def run_server():
    """
    I run if I am the FIRST instance.
    I listen for commands forever.
    """
    print(f"[Server] Starting up. Listening on {PIPE_ADDRESS}...")

    # 1. Create the Named Pipe (Windows API happens here under the hood)
    listener = Listener(PIPE_ADDRESS, authkey = SECRET_PASSWORD)

    while True:
        try:
            # 2. Block and wait for a connection (Sleeps until data arrives)
            print("[Server] Waiting for instructions...")
            conn = listener.accept()

            # 3. Read the data
            msg = conn.recv()
            print(f"[Server] RECEIVED INSTRUCTION: {msg}")

            # DO STUFF HERE BASED ON 'msg'
            if msg == ['shutdown']:
                break

            conn.close()

        except Exception as e:
            print(f"[Server] Error: {e}")

    print("[Server] Shutting down.")
    listener.close()


if __name__ == "__main__":
    # Get arguments from command line (excluding the script name itself)
    user_args = sys.argv[1:]

    # Step 1: Try to be a client
    connected = run_client(user_args)

    # Step 2: If we couldn't connect, we become the server
    if not connected:
        run_server()
