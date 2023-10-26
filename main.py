from  concurrent.futures import ThreadPoolExecutor
import socket
import argparse
import sys
TARGET = ""
WORKER = 100 
TIMEOUT = 0.5
openPorts = []
def checking_port(ip: str,port: int):
    try:
        with socket.create_connection((ip,port),timeout=TIMEOUT):
            openPorts.append(port)
    except:
        pass        
def valid_ip():
    global TARGET

    if not TARGET:
        return False
    if(len(TARGET.split(".")) != 4):
        TARGET = socket.gethostbyname(TARGET)
        
    try:
        socket.inet_aton(TARGET)
        return True
    except socket.error:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic port scanner for beginner programmer.")
    parser.add_argument("target",help=" IP is target server ip")
    parser.add_argument("-p",nargs=2,help="Begin/End port")
    parser.add_argument("-t",type=float,help="Timeout for each scan")
    parser.add_argument("-w",type=int,help="Maxiumum thread worker count ")

    args = parser.parse_args()

    TARGET = args.target
    PORT_INITIAL = -1
    PORT_END = -1

    if not args.t ==  None:
        args.t = TIMEOUT
    if not args.w == None:
        args.w = WORKER       
    if not args.p == None:
        if args.p[0] == "-":
            args.p = "0"
        if args.p[1] == "-":
            args.p = "65535"
        if not args.p[0].isdigit() or not  args.p[1].isdigit():
            print("Invalid port number")
            sys.exit()
        else:
            PORT_INITIAL = int(args.p[0])
            PORT_END = int(args.p[1])
    else:
        PORT_INITIAL = 0
        PORT_END = 65535

    if not valid_ip():
        print(f"Invalid ip: {TARGET}")
        sys.exit()

    print(f"\nScanning {TARGET} from port {PORT_INITIAL} to {PORT_END}...\n")
    
    pool = ThreadPoolExecutor(max_workers=WORKER)
    for port in range(PORT_INITIAL,PORT_END + 1):
        pool.submit(checking_port,TARGET,port)

    pool.shutdown(wait=True)
    for port in openPorts:
        print(f"Port {port} is open.")    










   





    
