import socket


def basic_send(msg: str):
    """
    Given a message, simply generates checksum and sends message
    Does not check anything
    Returns true if message successfully sent
    Returns false if message not sent
    """
    tx_port = 5555
    udp_ip = "127.0.0.1"
    try:  # Message successfully sent
        msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
        return True
    except:
        return False