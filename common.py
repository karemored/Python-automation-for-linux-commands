import paramiko
import sys

SUCCESS = True
FAIL = False

###################################################################
# NAME         : execCmd
# DESCRIPTION  : Executes the command given by the end user
# INPUT PARAMS : 1 session : ssh session
#                2. ipaddr : ip address associated with the session
#                3. cmd : command to be executed
#                4. sudo : true/false
# RETURN       : calls PrintOP function
###################################################################

def execCmd(session,ipaddr,passwd,cmd,sudo = False):

	if sudo:
		sudo_cmd = "sudo -k " + cmd
		
		try:
                	stdin,stdout,stderr = session.exec_command(sudo_cmd, get_pty = True)
			if stdout.channel.recv_exit_status() != 0:
				print "\nERROR : COMMAND->\"sudo "+cmd+"\" FAILED; PROBABLE INCORRECT COMMAND GIVEN"
			
		except:
			print "ERROR : SUDO COMMAND COULD NOT BE EXECUTED"

		stdin.write(passwd+"\n")
		stdin.flush()
	else:
		sudo_cmd = cmd
		
		try:
			stdin,stdout,stderr = session.exec_command(sudo_cmd, get_pty = True)
			if stdout.channel.recv_exit_status() != 0:
                                print "ERROR : COMMAND-\""+cmd+"\" FAILED"
		except:
			print "ERROR : COMMAND COULD NOT BE EXECUTED"
			
	return printOP(ipaddr,sudo_cmd,stdin,stdout,stderr)

###################################################################
# NAME         : printOP
# DESCRIPTION  : Prints the output of each command
# INPUT PARAMS : 1. session : ssh session
#                2. ipaddr : ip address associated with the session
#                3. cmd : command to be executed
#                4. sudo : true/false
#                5. stdin : standard input buffer to the pseudo terminal
#                6. stdout : standard output buffer to the pseudo terminal
# RETURN       : SUCCESS/FAILURE
###################################################################

def printOP(ipaddr,sudo_cmd,stdin,stdout,stderr):
	op_file = open("output.txt","a")                                         # opens a output file to print the output of commands
	op_file.write("\n")
	op_file.write("\n\tIP ADDRESS OF THE HOST:"+ipaddr)                      # IP address of the host
	op_file.write("\n\tCOMMAND EXECUTED :"+"\""+sudo_cmd+"\"")               # command that is executed
	op_file.write("\n")   
	buffertrack = ""	
	while True:
		opparser = stdout.read(1)                                            # every charachter is read one by one from the output buffer 
		                                                                     # and fed to the output file
		if opparser == '':
			break

		if opparser != '':
			buffertrack = buffertrack + str(opparser)
			op_file.write(opparser)

	return SUCCESS	
