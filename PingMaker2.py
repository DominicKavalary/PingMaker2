#### Setup ####
###Imports###
import time
import requests
import threading
import subprocess
import os.path

##Functions###
#subprocess outputgrab function#
def getOutput(Command):
  temp = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE)
  output,error = temp.communicate()
  output = output.decode("utf-8")
  output = output.splitlines()
  return output

#Ping and write thread function#
def PingandWrite(Address):
      Address = Address.replace("\n","")
      Command = "ping -c 4 " + Address
      output = getOutput(Command)
      for line in output:
        if "% packet loss" in line:
          pktloss = int(line.split(', ')[2].split(" ")[0][:-1])
          if pktloss > 25:
            with open("/home/PingMaker/csv/"+Address+".csv", "a") as statfilecsv:
              errtime = time.strftime("%D:%H:%M:%S")
              if csvExists:
                statfilecsv.write("\n"+Address +","+str(pktloss)+","+errtime)
              else:
                statfilecsv.write("Address,pktloss,errtime")
                statfilecsv.write("\n"+Address+","+str(pktloss)+","+errtime)

####Create Directory#####
subprocess.Popen("mkdir /home/PingMaker/csv", shell=True, stdout=subprocess.PIPE)

####MAIN####
ListofTargets = []
with open("/home/PingMaker/PingMakerTargets.txt", "r") as targetFile:
  for line in targetFile:
    ListofTargets.append(line)

####multithres ping targets and wirte to file###
# never stop until script is canceled

while 1==1:
  for Address in ListofTargets:
    PingThread = threading.Thread(target=PingandWrite, args=(Address,))
    PingThread.start()
  time.sleep(1)
