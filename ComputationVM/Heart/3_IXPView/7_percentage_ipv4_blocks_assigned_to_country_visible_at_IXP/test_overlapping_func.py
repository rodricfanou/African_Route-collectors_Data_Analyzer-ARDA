import random
import sys

from netaddr import *
from netaddr import IPNetwork

ip = IPNetwork('41.32.0.0/12')
ip_list = list(ip)
print(len(ip_list))
n = random.randint(0, len(ip_list))

for address in list(ip[0:n]):
    # print address
    if address in IPNetwork("41.32.4.0/24"):
        print(address, ' is in ', IPNetwork("41.32.4.0/24"))
    else:
        print(address, ' is not in ', IPNetwork("41.32.4.0/24"))

sys.exit()
