#### Setup ####
###Imports###
import time
import requests
import threading
import subprocess
import os

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
    try:
      errtime = time.strftime("%D:%H:%M:%S")
      Address = Address.replace("\n","")
      Command = "ping -c 4 " + Address
      output = getOutput(Command)
      packetLossNotFound = True
      for line in output:
        if "% packet loss" in line:
          packetLossNotFound = False
          pktloss = int(line.split(', ')[2].split(" ")[0][:-1])
          if pktloss > 25:
            csvExists = os.path.exists("/home/PingMaker/csv/"+Address+".csv")
            print(csvExists)
            with open("/home/PingMaker/csv/"+Address+".csv", "a") as statfilecsv:
              if csvExists:
                statfilecsv.write("\n"+Address +","+str(pktloss)+","+errtime)
              else:
                statfilecsv.write("pktloss,errtime")
                statfilecsv.write("\n"+str(pktloss)+","+errtime)
      if packetLossNotFound:
        with open("/home/PingMaker/errors/"+Address, "a") as errfile:
          errfile.write("No info found for: "+Address+", check format of address")
    except:
      with open("/home/PingMaker/errors/"+Address, "a") as errfile:
        errfile.write("Unkown error with pinging host "+Address+", "+errtime)

####Create Directory#####
subprocess.Popen("mkdir /home/PingMaker/csv", shell=True, stdout=subprocess.PIPE)
subprocess.Popen("mkdir /home/PingMaker/errors", shell=True, stdout=subprocess.PIPE)

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
