#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
'''
############################
#####
#####       Photon
#####      R. THOMAS
#####        2018
#####
###########################
@License: GPL - see LICENCE.txt
'''

###import libraries
import sys
import os

##third parties
from PyQt5.QtWidgets import QApplication

###Local modules
from . import cli
from . import GUI
from . import __info__ as info

def main():
    '''
    This is the main function of the code.
    if loads the command line interface and depending
    on the options specified by the user, start the 
    main window.
    '''
    ###load the command line interface
    args = cli.CLI().arguments

    if args.version == True:
        print('version %s'%info.__version__)
        sys.exit()

    ###terminal message
    print('\n\t\t\t\tPhoton V%s'%info.__version__)
    print('\t\t\t      R. Thomas -2018-')

    if args.docs == True:
        web = input('what is the command to open web browser?')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        index_doc = os.path.join(dir_path, 'docs/index.html')
        os.system('%s %s'%(web, index_doc))
        sys.exit()

    if args.plot == None and args.file == None:
        print('\n\t No file not plot configuration given...exiting photon...\n\
                Try photon --help to look at the options\n')
        sys.exit()

    if args.plot != None:
        print('\n\t Load plot: %s'%args.plot)

    if args.file != None:
        print('\n\t Load file: %s\n'%args.file)

    ###Construct a QAppp
    app = QApplication(sys.argv)

    if args.width != None:
        win = GUI.Main_window(args)    
        win.resize(args.width, 1030)

    if args.width == None:
        args.width = 780
        win = GUI.Main_window(args)    
        win.resize(args.width, 1030)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
