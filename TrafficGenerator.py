
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

    timeForFlow = 1500
    rateOfFlow = 20 # for each s1 and s2
    packetSize = 1400
    timeToSleep = 29.3

    #os.system('eval "$(ssh-agent)"')

    # run 10 times
    for i in range(100):

        # send at rate 50 packets per second (on both s1 and s2)
        runNping('s1', rateOfFlow, timeForFlow, packetSize)
        runNping('s2', rateOfFlow, timeForFlow, packetSize)

        print "SENT NUMBER: ", i

        time.sleep(timeToSleep)
