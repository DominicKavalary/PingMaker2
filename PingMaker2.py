###imports###
import time
import requests
import threading
import subprocess

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
      Command = "ping -c 4 " + Address
      output = getOutput(Command)
      for line in output:
        if "% packet loss" in line:
          pktloss = int(line.split(', ')[3].split(" ")[0][:-1])
          if pktloss > 25:
            with open("/home/PingMaker/PingStats"+Address+".txt", "a") as statfile:
              errtime = time.strftime("%H:%M:%S")
              statfile.write("\nTarget: "+Address + "PacketLoss:"+str(pktloss)+ ", Time: "+errtime)
    except:
      FileName = ("/home/PingMaker/PingStats"+Address+".txt").replace("\n","")
      with open(FileName, "a") as f:
        f.write(Address)

####open targets file#####
ListofTargets = []
with open("/home/PingMaker/PingMakerTargets.txt", "r") as targetFile:
  for line in targetFile:
    ListofTargets=line.split(",")

####multithres ping targets and wirte to file###
# never stop until script is canceled
while 1==1:
  for Address in ListofTargets:
    PingThread = threading.Thread(target=PingandWrite, args=(Address,))
    PingThread.start()
  time.sleep(5)
