import socket
import select
from subprocess import PIPE,Popen

def run_ping(host):
    # Runs the ping command and returns the average latency.
    p = Popen(['ping', '-c', '5', host], stdout=PIPE)
    for line in p.stdout:
        if line.startswith("rtt"):
            _, _, _, _, avg, _, _ = line.split("/")
            return avg
    return None

def run_traceroute(host):
    # Runs the traceroute command and returns the path and number of hops.
    p = Popen(['traceroute', '-w', '10', host], stdout=PIPE)
    path = []
    hops = 0
    for line in p.stdout:
        if line.startswith("traceroute"):
            continue
        ip = line.split('(', 1)[1].split(')')[0]
        path.append(ip)
        hops = len(path)
    return hops, path

def main():
    # create socket, bind it to a port and listen for new connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 2009))
    sock.listen(10)
    connections_list = [sock]
    # handle incoming connections
    while True:
        read, rite, error = select.select(connections_list, [], [])
        for s in read:
            if s is sock:
                connection, address = sock.accept()
                connections_list.append(connection)
            else:
                host = connection.recv(2048)
                print (host)
                if host:
                    avg_latency = run_ping(host)
                    hops, path = run_traceroute(host)
                    path_str = '-'.join(path)
                    connection.send(avg_latency + ' ' + str(hops) + ' ' + path_str)
                else:
                    connection.close()
                    connections_list.remove(connection)
                    
if __name__ == '__main__':
    main()