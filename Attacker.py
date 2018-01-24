
import os, time, subprocess
import datetime



controller = 'nabeel@pcvm2-15.instageni.gpolab.bbn.com'

s1_ad = 'nabeel@pcvm4-3.instageni.gpolab.bbn.com'

s2_ad = 'nabeel@pcvm4-4.instageni.gpolab.bbn.com'



def pingLogParser(S):

    S_a = S.split('\n')
    maxi = -1

    for i in S_a:

        ind_s = i.find('icmp_seq')
        ind_e = i.find('ttl=')
        if ind_s != -1:
            val = int(i[ind_s+9:ind_e])
            if val > maxi:
                maxi = val
    return maxi



if __name__ == '__main__':

    file = open('attacks.log','a+')
    file.write(str(datetime.datetime.now())+'\n')
    file.close()

    os.system('eval "$(ssh-agent)"')

    numberOfTimes = 1
    for i in range(numberOfTimes):

        if i%2 == 0:
            s_address = s1_ad
        else:
            s_address = s2_ad

        # remove files at the controller
        command = 'sudo rm /tmp/attacker.txt /tmp/snortalert'
        cmd_ = 'ssh ' + controller + " '" + command + "'"
        os.system(cmd_)
        time.sleep(2)

        # run PortScanner at the s1 or s2
        command = 'sudo ./PortScanAttack.sh'
        cmd_ = 'ssh ' + s_address + " '" + command + "'"
        subprocess.Popen(cmd_, shell=True)

        # sleep for 1 min
        time.sleep(2)
        print('waiting for attack to finish...')
        time.sleep(120)

        # kill nmap on s1 or s2
        command = 'sudo killall -v nmap'
        cmd_ = 'ssh ' + s_address + " '" + command + "'"
        os.system(cmd_)
        time.sleep(1)

        # get ping.log file. Just last line using grep
        #command = 'grep icmp_seq= ping.log | tail -1'
        command = 'cat ping.log'
        cmd_ = 'ssh ' + s_address + " '" + command + "'"
        proc = subprocess.Popen(cmd_, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        #print "program output:", out
        #pingCount = out.split()[5].split('=')[1]
        pingCount = pingLogParser(out)
        #print 'pingCount:',pingCount

        # count time it takes and add it to output log file
        timeTaken = float(pingCount)*0.2
        textToWrite = "Iteration:" + str(i) + ', timeTaken:' + str(timeTaken) + ' Source:S' + str((i%2)+1) + '\n'
        # print 'textToWrite:',textToWrite
        file = open('attacks.log', 'a+')
        file.write(textToWrite)
        file.close()

        print 'Time taken to detect attack:', str(timeTaken)
        
        # sleep for 1 minutes before new attack
        print('waiting before next attack...')
        time.sleep(20)

    file.close()
