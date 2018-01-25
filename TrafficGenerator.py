
# -*- coding: utf-8 -*-
import os, time
import subprocess


s1_address = 'nabeel@pcvm4-3.instageni.gpolab.bbn.com'

s2_address = 'nabeel@pcvm4-4.instageni.gpolab.bbn.com'

def runNping(host, rate, time, datalength):
    '''
    runs Nping on destination
    :param host: host that you wish to run command on
    :param rate: rate at which to send packets
    :param time: time for which the packets need to be sent
    :param datalength: length of packets
    :return: nothing
    '''

    c = rate * time

    command = 'sudo nping --udp 10.10.1.5 -H --source-ip random --source-port random --source-mac random --data-length '+str(datalength)+' --rate '+str(rate)+' -c '+str(c)+' &'

    if host == 's1':
        cmd_ = 'ssh '+s1_address+" '"+command+"'"
        print("RUNNING on S1: ", cmd_)
        #os.system(cmd_)
        subprocess.Popen(cmd_,shell=True)
    else:
        cmd_ = 'ssh ' + s2_address + " '" + command + "'"
        print("RUNNING on S2: ", cmd_)
        #os.system(cmd_)
        subprocess.Popen(cmd_,shell=True)




if __name__=='__main__':

    timeForFlow = 700   # time (in seconds) to live for a flow
    rateOfFlow = 20     # number of packets per second sent in a flow
    packetSize = 1400   # size of each packet for a flow
    timeToSleep = 19.3  # time between each consecutive flows

    for i in range(100):

        # send at rate 50 packets per second (on both s1 and s2)
        runNping('s1', rateOfFlow, timeForFlow, packetSize)
        runNping('s2', rateOfFlow, timeForFlow, packetSize)

        print "SENT NUMBER: ", i

        time.sleep(timeToSleep)
