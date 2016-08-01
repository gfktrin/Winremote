#Winremote by Gabriel Trindade
import requests
from bs4 import BeautifulSoup
import time
import os
import winshell
import os.path
import webbrowser
import ImageGrab
import threading
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler

def check_id():#checks if exists an id file on pc, it creates an id file if there isn't one
	global app_data, id
	if os.path.isfile(app_data + '\id.paradox'): 
		file = open(app_data + '\id.paradox', 'r')
		id = file.readline()
		file.close()
	else:
		file = open(app_data + '\id.paradox', 'w')
		file.write('1')
		id = '1'
		file.close()

def screenshot():#takes screenshots, they are stored in my documents folder
	global PRINT_start, PRINT_limiter
	box = ()
	im = ImageGrab.grab()
	im.save(documents + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
	PRINT_start = time.time()
	PRINT_limiter = 1
		
def start_server():# for starting the http server
	thread.start()
	print('starting server on port {}'.format(server.server_port))#port 2928

def close_server():# for closing the server
	server.shutdown()
	print('stopping server on port {}'.format(server.server_port))
  
def http_server(comamnd):# checks if it's a start or a stop comamnd for http server
	global documents, HTTP_limiter, HTTP_control
	if (comamnd[7:len(comamnd)] == 'start') and (HTTP_limiter == 0):
		os.chdir(documents)
		start_server()
		HTTP_limiter = 1
		HTTP_control = ''
	elif (comamnd[7:len(comamnd)] == 'stop') and (comamnd != HTTP_control):
		close_server()
		HTTP_control = comamnd
		HTTP_limiter = 0

def open_website(comamnd): #opens a website in the default browser
	global WEB_start, WEB_limiter
	webbrowser.open(comamnd[4:len(comamnd)], new=0, autoraise=True)
	WEB_start = time.time()
	WEB_limiter = 1
		
def close_process(comamnd): #closes a process
	global EXE_start, EXE_limiter
	os.system("taskkill /im "+comamnd[6:len(comamnd)]+".exe")
	EXE_start = time.time()
	EXE_limiter = 1

def change_id(comamnd):# changes the id
	global id_control, app_data
	file = open(app_data + '\id.paradox', 'w')
	id = comamnd[9:len(comamnd)]
	file.write(id)
	file.close()
	id_control = comamnd

def msg(comamnd): #shows a message on the screen with notepad
	global msg_control, app_data
	file = open(app_data + '\msg.txt', 'w')
	file.write(comamnd[4:len(comamnd)])
	file.close()
	os.startfile(app_data + '\msg.txt')
	msg_control = comamnd

def check_comamnd(comamnd): #checks the command and executes the functions
	global off_limiter, app_data,id,startup, msg_control, id_control, x, WEB_limiter, documents
				
	if (comamnd == id+'shutdown') and (off_limiter == 0):
		os.system("shutdown -s")
		off_limiter = 1
		
	elif (comamnd[0:4] == id+'msg') and (comamnd != msg_control):
		msg(comamnd)
		
	elif (comamnd[0:9] == id+'changeid') and (comamnd != id_control) :
		change_id(comamnd)
		
	elif comamnd == id+'deletemsg' :
		os.remove(app_data + '\msg.txt')
	
	elif comamnd == id+'stop' :
		x = 0
	
	elif (comamnd[0:6] == id+'close') and(len(comamnd) > 6) and (EXE_limiter == 0):
		close_process(comamnd)
		
	elif (comamnd[0:4] == id+'web') and (WEB_limiter == 0):
		open_website(comamnd)
	
	elif (comamnd[0:7] == id+'server'):
		http_server(comamnd)
		
	elif (comamnd == id+'print') and (PRINT_limiter == 0):
		screenshot()
			
def get_title():#gets the title of the webpage used to send commands
	try:
		
		html = requests.get('http://webpage.com') #put the site here 
		html = html.text		
		html = html.replace("</scr' + 'ipt>","")		
		soup = BeautifulSoup(html, 'html.parser')		
		comamnd = soup.title.string						
		check_comamnd(comamnd)

	except:
		time.sleep(1)#you can put an error message here if you want
			
def time_control():#controls the time for using some functions
	global x, EXE_limiter, WEB_limiter, PRINT_limiter
	while x == 1:
		end_time = time.time()
	
		time.sleep(3)#necessary because you can't do too many requests in a small period of time
		get_title()
		
		if EXE_limiter == 1:
			if end_time - EXE_start > 60:#after 60 seconds the limiter's value is zero again
				EXE_limiter = 0
			
		if WEB_limiter == 1:
			if end_time - WEB_start > 60:
				WEB_limiter = 0
	
		if PRINT_limiter == 1:
			if end_time - PRINT_start > 60:
				PRINT_limiter = 0


app_data = winshell.folder("CSIDL_APPDATA")
startup = winshell.startup()
documents = winshell.my_documents()
x = 1#this variable keeps the program running
off_limiter = 0#the limiters and controls variables are for preventing the program executing the same command many times at the same moment
EXE_limiter = 0
WEB_limiter = 0
HTTP_limiter = 0
PRINT_limiter = 0
msg_control = ''
id_control = ''
HTTP_control = ''
server = HTTPServer(('localhost', 0), BaseHTTPRequestHandler)
thread = threading.Thread(target = server.serve_forever)
thread.deamon = True

check_id()
time_control()