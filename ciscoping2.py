import click
import ipaddress
import socket
from subprocess import Popen, PIPE

@click.command()
@click.argument('host')
@click.option('--repeat', '-r', default=5, show_default=True, help='specify repeat count')
@click.option('--size', '-s', default=100, show_default=True, help='specify datagram size')
@click.option('--timeout', '-t', default=2, show_default=True, help='specify timeout interval')
@click.option('--dfbit/--no-dfbit', default=False, help='enable do not fragment bit in IP header')
def ping(host, repeat, size, timeout, dfbit):
    """
    Cisco-like ping tool
    """
    rtt_min = rtt_max = rtt_avg = rtt_sum = 0
    failures = 0
    sent = 0
    if dfbit:
        opts = '-M do'
    else:
        opts = ''

    try:
        ipaddress.ip_address(host)
    except:
        print(f'Translating {host}... ', end='')
        try:
            host = socket.gethostbyaddr(host)[2][0]
            print('[OK]', end='\n\n')
        except:
            print('\n% Unrecognized host or address')
            exit()

    print('Type Ctrl-C to abort.')
    print(f'Sending {repeat}, {size}-byte ICMP Echos to {host}, timeout is {timeout} seconds:')

    try:
        for i in range(repeat):
            sent += 1
            p = Popen(f'ping -c 1 -W {timeout} -s {size-28} {opts} {host}', stdout=PIPE, stderr=PIPE, shell=True)
            out = p.communicate()
            if p.returncode == 0:
                rtt = float(out[0].decode('ascii').split('/')[4])
                if i == 0:
                    rtt_min = rtt
                else:
                    rtt_min = min(rtt_min, rtt)
                rtt_max = max(rtt_max, rtt)
                rtt_sum += rtt
                print('!', end='', flush=True)
            else:
                print('.', end='', flush=True)
                failures += 1
            if sent % 70 == 0:
                print('')
    except KeyboardInterrupt:
        pass

    rtt_avg = rtt_sum / repeat
    success_rate = int(100 - (failures / repeat) * 100)

    print('')
    print(f'Success rate is {success_rate} percent ({sent-failures}/{sent}), round-trip min/avg/max = {rtt_min:0.2f}/{rtt_avg:0.2f}/{rtt_max:0.2f} ms')

if __name__ == '__main__':
    ping()

