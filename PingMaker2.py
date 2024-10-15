#### Setup ####
###Imports###
import time
import requests
import threading
import subprocess

###Functions###
#subprocess output grab function#
def getOutput(Command):
  temp = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE)
  output,error = temp.communicate()
  output = output.decode("utf-8")
  output = output.splitlines()
  return output

#Ping and write thread function#
def PingandWrite(Address):
#    try:
# replace newlines in address. if doesnt work replace them later on in the text
      Address = Address.replace("\n","")
# make the command and get its output
      Command = "ping -c 4 " + Address
      output = getOutput(Command)
# for every line in that output, grab the packetloss
      for line in output:
        if "% packet loss" in line:
          pktloss = int(line.split(', ')[2].split(" ")[0][:-1])
# if packet loss is greater than 25%, write the timestamp and packet loss to a text file
          if pktloss > 25:
            with open("/home/PingMaker/PingStats_"+Address+".txt", "a") as statfile:
              errtime = time.strftime("%D:%H:%M:%S")
              statfile.write("\nTarget: "+Address + " | PacketLoss: %"+str(pktloss)+ " | Time: "+errtime)

    #except:

   #   FileName = ("/home/PingMaker/PingStats"+Address+".txt").replace("\n","")

  #    with open(FileName, "a") as f:

 #       f.write(Address)

#### MAIN ####
###open targets file and create list of targets###
ListofTargets = []
with open("/home/PingMaker/PingMakerTargets.txt", "r") as targetFile:
  for line in targetFile:
    ListofTargets.append(line)

####multithread ping targets###
#never stop until script is canceled, sleep for 5 seconds before doing another thread
while 1==1:
  for Address in ListofTargets:
    PingThread = threading.Thread(target=PingandWrite, args=(Address,))
    PingThread.start()
  time.sleep(2)
