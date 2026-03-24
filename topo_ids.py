#!/usr/bin/env python3
"""
Topologie IDS realiste — OpenFlow 1.3 correct
"""
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

class OVS13Switch(OVSSwitch):
    """Switch OVS force en OpenFlow 1.3"""
    def __init__(self, name, **params):
        OVSSwitch.__init__(self, name, failMode='secure',
                          protocols='OpenFlow13', **params)

def run():
    setLogLevel('info')
    net = Mininet(switch=OVS13Switch,
                  controller=None,
                  link=TCLink,
                  autoSetMacs=False)

    # Controller ONOS
    onos = net.addController('onos',
                             controller=RemoteController,
                             ip='127.0.0.1',
                             port=6653)

    # Switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Hotes avec MACs et IPs realistes
    h1 = net.addHost('h1',
                     mac='a4:c3:f0:85:12:3e',
                     ip='192.168.1.10/24',
                     defaultRoute='via 192.168.1.1')

    h2 = net.addHost('h2',
                     mac='b8:27:eb:4f:a1:92',
                     ip='192.168.1.20/24',
                     defaultRoute='via 192.168.1.1')

    h3 = net.addHost('h3',
                     mac='dc:a6:32:11:87:5c',
                     ip='192.168.1.30/24',
                     defaultRoute='via 192.168.1.1')

    # Liens realistes
    net.addLink(h1, s1, bw=100, delay='2ms')
    net.addLink(h2, s3, bw=100, delay='2ms')
    net.addLink(h3, s3, bw=100, delay='2ms')
    net.addLink(s1, s2, bw=1000, delay='1ms')
    net.addLink(s2, s3, bw=1000, delay='1ms')

    net.build()
    onos.start()

    # Demarre les switches avec OpenFlow 1.3
    for sw in [s1, s2, s3]:
        sw.start([onos])

    print("\n=== Topologie IDS SOC Realiste ===")
    print("h1 (Attaquant) : 192.168.1.10 → s1")
    print("h2 (Victime)   : 192.168.1.20 → s3")
    print("h3 (Client)    : 192.168.1.30 → s3")
    print("Backbone       : s1 -- s2 -- s3")
    print("Controller     : ONOS 127.0.0.1:6653 OpenFlow13")
    print("=================================\n")

    # Attends que ONOS installe les flows
    import time
    print("Attente installation flows ONOS (10s)...")
    time.sleep(10)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
