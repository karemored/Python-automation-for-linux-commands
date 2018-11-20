import re
import common as cmn

SUCCESS = True
FAIL = False

###################################################################
# NAME         : fetchCmd
# DESCRIPTION  : Extracts all commands from the input file 
#                commands.txt#                
# INPUT PARAMS : None
# RETURN       : list of all commands
###################################################################

def fetchCmd():
	file_cmd = open("commands.txt","r")
	list_cmd = []
	
	list_cmd = file_cmd.read().splitlines()

	return list_cmd

###################################################################
# NAME         : chkSudo
# DESCRIPTION  : checks whether the command is to be executed being 
#                sudo user or not
# INPUT PARAMS : command
# RETURN       : sudo = (true/false) and command
###################################################################

def chkSudo(cmd):
	if re.search("\s*sudo\s\w+",cmd):                                   # checks for the word "sudo" in front of the command
		sudo_cmd = ''.join(re.findall("\s*sudo\s(.*)",cmd))             
		sudo = True
	else:
		sudo_cmd = cmd
		sudo = False
	
	return (sudo_cmd,sudo)

def devScript(session_list,ipaddr_list,passwd_list):

	list_cmd = fetchCmd()

	for cmd_itr in list_cmd:                                           # loop through a command  
		sudo_cmd , sudo = chkSudo(cmd_itr)                    
		for session_itr in range(1,len(session_list)):	               # loop though each ssh session
			cmn.execCmd(session_list[session_itr],ipaddr_list[session_itr],passwd_list[session_itr],sudo_cmd,sudo)	
