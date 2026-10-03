from socket import *
import time


# Server settings
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 12000

# Ping settings
PING_COUNT = 10
TIMEOUT = 1

# Create UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

rtt_values = []
lost_packets = 0


print("=" * 45)
print("             UDP PINGER CLIENT")
print("=" * 45)
print(f"Server: {SERVER_NAME}:{SERVER_PORT}")
print(f"Sending {PING_COUNT} ping requests...")
print("-" * 45)


for sequence_number in range(1, PING_COUNT + 1):
    send_time = time.time()

    # Send ping request
    message = f"Ping {sequence_number} {send_time}"
    client_socket.sendto(message.encode(), (SERVER_NAME, SERVER_PORT))

    try:
        # Wait for server response
        message, server_address = client_socket.recvfrom(1024)

        receive_time = time.time()
        rtt = receive_time - send_time

        print(f"Ping {sequence_number}: {message.decode()}")
        print(f"  RTT: {rtt:.6f} seconds")

        rtt_values.append(rtt)

    except timeout:
        print(f"Ping {sequence_number}: Request timed out")
        lost_packets += 1


# Display ping statistics
print("\n" + "=" * 45)
print("              PING STATISTICS")
print("=" * 45)

if rtt_values:
    min_rtt = min(rtt_values)
    max_rtt = max(rtt_values)
    avg_rtt = sum(rtt_values) / len(rtt_values)
    packet_loss = (lost_packets / PING_COUNT) * 100

    print(f"Minimum RTT : {min_rtt:.6f} seconds")
    print(f"Maximum RTT : {max_rtt:.6f} seconds")
    print(f"Average RTT : {avg_rtt:.6f} seconds")
    print(f"Packet Loss : {packet_loss:.1f}%")
else:
    print("No responses received.")
    print("Packet Loss : 100.0%")

print("=" * 45)

# Close the socket
client_socket.close()