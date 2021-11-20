"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )
        s7 = self.addSwitch( 's7' )
        s8 = self.addSwitch( 's8' )


        h1 = self.addHost('h1', ip='172.16.10.10/24', defaultRoute='via 172.16.10.1')
        h2 = self.addHost('h2', ip='172.16.20.10/24', defaultRoute='via 172.16.20.1')

#        leftHost = self.addHost( 'h1' )
#        rightHost = self.addHost( 'h2' )
#        leftSwitch = self.addSwitch( 's3' )
#        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( s1, s2 )
        self.addLink( s1, s3 )
        self.addLink( s1, s5 )
        self.addLink( s2, s3 )
        self.addLink( s2, s5 )
        self.addLink( s2, s4 )
        self.addLink( s3, s4 )
        self.addLink( s3, s6 )
        self.addLink( s3, s5 )
        self.addLink( s3, s7 )
        self.addLink( s4, s5 )
        self.addLink( s4, s6 )
        self.addLink( s4, s7 )
        self.addLink( s4, s8 )
        self.addLink( s5, s6 )
        self.addLink( s5, s7 )
        self.addLink( s6, s7 )
        self.addLink( s6, s8 )
        self.addLink( s7, s8 )
        self.addLink( h1, s1 )
        self.addLink( h2, s8 )


topos = { 'mytopo': ( lambda: MyTopo() ) }

# H x A

locations = {'c0':(50,50), 's1':(200,300), 's2':(400,150), 's3':(400,450), 's4':(600,100), 's5':(600,400), 's6':(800,150), 's7':(800,450), 's8':(1000,300), 'h1':(100,300), 'h2':(1100,300)}
