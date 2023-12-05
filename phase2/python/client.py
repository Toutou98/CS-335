import socket
import sys

# parse configuration file
def read_config(filename):
    hosts = {}
    routers = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            name = parts[0]
            ips = parts[1:]
            if name.endswith('-host'):
                hosts[name] = ips[0]  # store first IP as host IP
            elif name.endswith('-router'):
                routers[name] = ips[0:]
    return hosts, routers

# function to convert ip values to their corresponding names
# type == 'host' to convert a host ip to name
# type == 'router' tp convert a router interface ip to name
def ip_to_name(ip, hosts_info, routers_info):
        for key, val in hosts_info.items():
            if ip in val:
                return key
        for key, val in routers_info.items():
            if ip in val:
                return key
        return ip



# print latency, number of hops, and path description
def print_results(data, hosts_info, routers_info):
    print
    print ('    Hosts                  Latency     Hops          Path')
    print
    for line in data:
        path_names = []
        host1, host2, latency, hops, path = line.split(' ')
        host1_str = ip_to_name(host1, hosts_info, routers_info)
        host2_str = ip_to_name(host2, hosts_info, routers_info)
        path_split = path.split('-')
        for ip in path_split:
            path_names.append(ip_to_name(ip, hosts_info, routers_info))
        final_path = ' -> '.join(path_names)
        if (len(latency) > 5):
            spaces = '      '
        else:
            spaces = '       '
        print ('    ' + host1_str + '-' + host2_str + '    ' + latency + spaces + hops + '             ' + final_path)
    print
    return



def main():
    # parse host names from command line
    host_names=sys.argv[1].strip('[').strip(']').split(',')
    # read configuration file
    hosts_info, routers_info = read_config('configuration.txt')
    data = []
    # keep only the host ips we need
    servers = []
    for name in host_names:
        if hosts_info.has_key(name):
            servers.append(hosts_info[name])

    # create sockets and send measurement requests to all server hosts
    for server in servers:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, 2009))
        for server2 in servers:
            if server != server2:
                sock.sendall(server2)
                results = sock.recv(1024)
                data.append(str(server) + ' ' + str(server2) + ' ' + results)

    print_results(data, hosts_info, routers_info)
    # close socket
    sock.close()

if __name__ == '__main__':
    main()


