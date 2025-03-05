import zmq
import numpy as np

def receive_data(zmq_address, data_type=np.complex64):
    """Receive data from a ZMQ PUB address with conflate and no block."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    # Set the conflate option to only receive the latest message
    socket.setsockopt(zmq.CONFLATE, 1)
    
    # Set subscription to all topics
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    
    # Connect to the specified address
    socket.connect(zmq_address)
    
    print(f"Connected to {zmq_address}...")
    
    while True:
        try:
            # Receive a message (non-blocking)
            data = socket.recv(flags=zmq.NOBLOCK)
            
            # Convert the received data to the specified type
            array = np.frombuffer(data, dtype=data_type)
            #array = np.frombuffer(data, dtype='<c8')  # '<c8' ensures little-endian complex64

            
            # Process the data (you can customize this)
            print(f"Received data: {array}")
        
        except zmq.Again:
            # No data available, continue non-blocking operation
            pass
        except KeyboardInterrupt:
            print("Interrupted. Exiting...")
            break
    
    socket.close()
    context.term()

if __name__ == "__main__":
    zmq_address = "tcp://127.0.0.1:5555"  # Replace with the desired ZMQ PUB address
    receive_data(zmq_address)
