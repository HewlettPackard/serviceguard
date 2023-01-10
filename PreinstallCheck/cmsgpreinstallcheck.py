#!/usr/bin/python
####################################################################
# (C) Copyright 2023 Hewlett Packard Enterprise Development LP.
###################################################################

# Preinstallation script which checks for
# standard configurations

from __future__ import print_function

import preinstallUtils as preutils

import json
import os
import subprocess
import re
import platform
import sys
import socket
import argparse
import logging
from subprocess import PIPE, Popen
log_file = "/tmp/cminstaller.log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers = []

file_handler = logging.FileHandler(log_file, mode='a')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--Detailed", help = "Show Detailed", action = "store_true")
parser.add_argument("-s", "--Summary", help = "Show Summary", action = "store_true")
parser.add_argument("-p","--parser", help = "Parse given data", action="store_true")

args = parser.parse_args()
if args.Detailed:
    preinstall_log_option = True
elif args.Summary:
    preinstall_log_option = False
else:
    preinstall_log_option = True

if args.parser:
    preutils.execute_parser_functions()

def main():
    try:
        preutils.cleanup()
        nodes = preutils.get_config_data("validation_nodes")
        
        local_node = preutils.get_hostName()

        for each_node in nodes:
            temp_list = []
            if each_node == local_node:
                remote_node_flag = False
            else:
                remote_node_flag = True
            print ("*****************************************************************************************************************************")
            print (" Preinstall check for node ",str(each_node))
            print ("*****************************************************************************************************************************")

            print()

            output = preutils.check_reachability(each_node,remote_node_flag)
            temp_list.append(output)
            logger.debug("Exiting check_reachability function on node " + each_node)
            os_list = preutils.serviceguard_os_list()
            output = preutils.check_distro_installed(os_list,each_node,remote_node_flag)
            temp_list.append(output)
            logger.debug("Exiting check_distro_installed function on node " + each_node)
            output = preutils.check_rpm_installed(each_node,remote_node_flag)
            temp_list.append(output)
            logger.debug("Exiting check_rpm_installed function on node " + each_node)
            output = preutils.check_port(each_node,remote_node_flag)
            temp_list.append(output)
            logger.debug("Exiting check_port function on node " + each_node)
            for i in range(len(temp_list)):
                preutils.print_detailed_summary(temp_list[i],preinstall_log_option)
            print()
    except Exception as ex:
        print("Exception in main function",str(ex))
main()
os.system("rm -rf tmp.txt")
