"""
Generate IP address plan for webcams (Elections 2018)
Network: 10.132.0.0/16

subnets must be /28, plan for each net:

net+0       Network
net+1       Gateway
net+2       Switch mgmt (if exists)
net+3       DSL modem mgmt (if exists)
net+4       Camera 1
net+5       Camera 2
net+6       UPS (if exists)
net+7-14    reserved
net+15      broadcast

"""
import ipaddress

main_net = '10.132.0.0'
main_prefix = 16
net_prefix = 28
number_of_nets = 183

prefix_diff = main_prefix-(32-net_prefix)    # we need /28 nets
all_nets = list(ipaddress.ip_network(f'{main_net}/{main_prefix}').subnets(prefixlen_diff=prefix_diff))

for i,net in enumerate(all_nets):
    n = ipaddress.ip_network(net)
    hosts = list(n.hosts())
    print(f'{hosts[3]};{hosts[4]};{n.network_address};{n.netmask};{hosts[0]}')
    if i == number_of_nets-1:
        break
print(f'Generated {i+1} subnets')
