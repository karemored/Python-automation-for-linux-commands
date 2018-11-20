###################################################################
#   
#   PYTHON AUTOMATION FOR BASIC LINUX COMMANDS
#   AUTHOR : DIVYANSH
#
###################################################################

import paramiko as po
import subprocess as sp
import genscript as script
import pdb
import sys
import re
import os

FAIL = False
SUCCESS = True

###################################################################
# NAME         : estbProcess
# DESCRIPTION  : Executes the ssh command on the shell using
#                paramiko library
# INPUT PARAMS : 1. ip : IP of 2U host to be ssh'd
# RETURN       : paramiko object for one ssh session
###################################################################

def estbProcess(ip, user, passwd):
	hostname = ip
        string = ""

        print "\n...STARTING SSH SESSION TO " + hostname + "..."
        try:
		process = po.SSHClient()
		process.set_missing_host_key_policy(po.AutoAddPolicy())
		process.connect(hostname = ip,username = user ,password = passwd)
        except po.ssh_exception.AuthenticationException:
                print "ERROR : SSH TO "+ip+" FAILED"
		print "ERROR : AUTHENTICATION FAILED"
		print "ERROR : INCORRECT USERNAME OR PASSWORD SPECIFIED"
                return None
	except po.ssh_exception.NoValidConnectionsError:
		print "ERROR : UNABLE TO CONNECT TO "+ip
		print "ERROR : PLEASE CHECK IF "+ip+" IS REACHABLE"
		return None
        return process

###################################################################
# NAME         : validateIP
# DESCRIPTION  : checks the input IPs and fetches them in a list
# INPUT PARAMS : each line of a file
# RETURN       : list of IPs to be ssh'd
###################################################################

def validateIP(line):
	IP = []
	params = []
	if line != '\n':
		params = re.findall("\s*(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\suser\s*=\s*(.+)\s+passwd\s*=([^\s]+)",line)
	
		if params != []:
			IP.append(params[0][0])
			IP.append(params[0][1])
			IP.append(params[0][2])
		else:
			ipaddr = re.findall("(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})",line)
			if ipaddr == []:
				print "WARNING : COULD NOT FIND A VALID IP IN LINE"
			else:
				IP.append(ipaddr[0])
				IP.append('kodiak')
				IP.append('kodiak')
		return IP

###################################################################
# NAME         : fetchIP
# DESCRIPTION  : reads the input file "config_IP.txt", fetches all
#                the IPs and puts them in a list
# INPUT PARAMS : none
# RETURN       : list of IPs of the hosts to be telnetted
###################################################################

def fetchIP(IP_details):
	ip_file = open("config_IP.txt","r")
		
	for line in ip_file:
		if line != '\n':
			login_params = validateIP(line)
			if login_params != []:
				IP_details.append(login_params)

###################################################################
# NAME         : chkFiles
# DESCRIPTION  : Check if the input files are specified
# INPUT PARAMS : none
# RETURN       : SUCCESS/FAIL
###################################################################

def chkFiles():
	try:
		ip_conf_file = open("config_IP.txt","r")
	except FileNotFoundError:
		print "ERROR : FILE \'config_IP.txt\' NOT FOUND; ABORTING AUTOMATION"
		return FAIL

        try:
                ip_cmd_file = open("commands.txt","r")
        except FileNotFoundError:
                print "ERROR : FILE \'commands.txt\' NOT FOUND; ABORTING AUTOMATION"
                return FAIL

	if os.path.exists("output.txt"):
		os.remove("output.txt")

	return SUCCESS
		
###################################################################
# NAME         : main
# DESCRIPTION  : main function execution to start fro  this point
# INPUT PARAMS : none
# RETURN       : none
###################################################################

def main():
        sessionID = 1                                                    # defining session ID to each telnet session
        session_list = ['zero']                                          # list to maintain all ssh sessions
	ipaddr_list = ['zero']
	passwd_list = ['zero']
        ip_config = []
	
	if chkFiles() == FAIL:
		return 
                                                                
        fetchIP(ip_config)
        for ip in ip_config:
		session_obj = estbProcess(ip[0],ip[1],ip[2])
		
		if session_obj != None:		
			print "...SSH TO "+ip[0]+" SUCCESSFUL..."
                	session_list.append(session_obj)              # establish telnet session and store it in session list
			ipaddr_list.append(ip[0])
			passwd_list.append(ip[2])

	script.devScript(session_list,ipaddr_list,passwd_list)

if __name__ ==  "__main__" :
        main()

