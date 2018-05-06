'''

The Photon Project 
-------------------
File: cli.py

This file configures the Command line interface 

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import argparse

class CLI:
    """
    This Class defines the arguments to be calle to use SPARTAN
    For the help, you can use 'SPARTAN -h' or 'SPARTAN --help'
    """
    def __init__(self,):
        """
        Class constructor, defines the attributes of the class
        and run the argument section
        """
        self.args()

    def args(self,):
        """
        This function creates defines the 7 main arguments of SPARTAN using the argparse module
        """
        parser = argparse.ArgumentParser(description="Photon V1.0, R. Thomas, 2018, ESO, \
                This program comes with ABSOLUTELY NO WARRANTY; and is distributed under \
                the GPLv3.0 Licence terms.See the version of this Licence distributed along \
                this code for details.")

        parser.add_argument('file', help="Your catalog of data to visualize, \
                this is mandatory (positionnal argument)")

        parser.add_argument("-t", "--header", action="store_true", help=" To be used If a header is present in the catalog (#A B C D....), you just write '-t'. If you do not use it, each column will be renames colX where X is the number of the column (starting at 1).")

        parser.add_argument("-c", "--conf", type = str, help="Properties configuration file. If none is givenm the default configuration will be loaded")

        parser.add_argument("-w", "--width", type = int, help="Width of the GUI, default = 780")


        ##### GET the Arguments for SPARTAN startup
        self.arguments = parser.parse_args()


