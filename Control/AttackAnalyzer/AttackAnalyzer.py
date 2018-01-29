__author__ = 'Nabeel'

import os, time, argparse

def main():
    pauseTime = 0.2

    # set the argument parer to take input file as input
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="path to snort attacker file")
    args = parser.parse_args()

    if args.filepath == None:
        print 'Please enter file path to snort alert file'
        parser.print_help()
        exit(0)

    inputFile = args.filepath

    # print the name of input file
    print inputFile

    # get types of attacks and save them in array
#     exists = os.path.isfile('attackType.config')
#     if exists == 1:
#         # add to array
#         f1 = open('attackType.config', 'r')
#         attackType = f1.read()
#         f1.close()
#         attackType_list = attackType.split('\n')
#     else:
#         print 'File to defile attacks does not exist!'
#         return

	print 'Attack Analyzer running!'
	
    while(True):
        try:

            # check if file exists, otherwise wait for sometime and try again!
            while (True):
                ans = os.path.isfile(inputFile)

                # if file found, then proceed. Otherwise keep waiting
                if ans == 1:
                    break
                else:
                    #print 'Snort alert file does not exists at ', inputFile, '\nChecking again...'
                    time.sleep(pauseTime)

            snort_alert_f = open(inputFile, 'r')
            snort_alert = snort_alert_f.read()
            snort_alert_f.close()

            # read the file and if there is anything, add to alert.txt file
            attacker_list = []
            alerts = snort_alert.split('\n')

            j = 0
            while j < len(attackType_list):
                # ping attack
                if attackType_list[j] == 'PING':
                    attackString = '-> 10.10.1.5 ICMP'
                # port scanning attack
                elif attackType_list[j] == 'PORTSCAN':
                    attackString = '(portscan)'
                # detect all attacks on destination
                else:
                    attackString = '-> 10.10.1.5'

                # check for attack defined in attackString
                i=0
                while i < len(alerts):
                    line = alerts[i]

                    if attackString in line:
                        attackerIP = line.split(' ')[0]
                        if attackerIP not in attacker_list:
                            attacker_list.append(attackerIP)

                    i = i+1
                j = j+1

            print 'Following IP addresses are being blocked:'
            print '\n'.join(attacker_list)

            # write list to attacker list
            attackerFile = open('/tmp/attacker.txt','w')
            attackerFile.write('\n'.join(attacker_list))
            attackerFile.close()

            # check if the file has changed and if it has changed, do the same
            while True:
                snort_alert_f_new = open(inputFile, 'r')
                snort_alert_new = snort_alert_f_new.read()
                snort_alert_f_new.close()

                # if the file has not changed, then keep reading it
                if snort_alert_new == snort_alert:
                    # file not changed, pause before making next query
                    time.sleep(pauseTime)
                    continue
                else:
                    # file changed, change attacker file
                    snort_alert = snort_alert_new
                    break

        except:
            print 'Error Accessing file, running it again!'
            attacker_list = []


if __name__ == "__main__":
    # System argument is the name of the snort alert file.
    main()

