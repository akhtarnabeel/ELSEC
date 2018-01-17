__author__ = 'Nabeel'

import sys, getopt, os, time
import matplotlib.pyplot as plt

def main(argv):
    nodeName = ''
    path = ''
    key = ''
    pauseTime = 5
    
    try:
        opts, args = getopt.getopt(argv,"hn:k:",["nodeName=","key="])
    except getopt.GetoptError:
        print 'RealTimeGraph.py -n <username@controllerIP> -k <path to geni key>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'RealTimeGraph.py -n <username@controllerIP> -k <path to geni key>'
            sys.exit()
        elif opt in ("-n", "--nodeName"):
            nodeName = arg
        elif opt in ("-k", "--key"):
            key = arg

    nodeName = nodeName.strip()
    path = path.strip('/')

    # if path entered, then use path. Else use the default path
    if path == '':
        path = '~/Control/RINA/'
    else:
        path = '/'+path

    print 'Controller is:', nodeName
    print 'Path to private key:', key

    ans = os.system('rm *.txt')

    if key == '':
        commandToFile = 'scp ' + nodeName + ':' + path + '/NFV* .'
    else:
        commandToFile = 'scp -i ' + key +' '+ nodeName + ':' + path + '/NFV* .'

    print 'Command is: ', commandToFile

    plt.ion()

    # check if the files exists on the server you are pinging
    while(True):
        ans = os.system(commandToFile)
        # if file found, proceed!
        if ans == 0:
            break
        else:
            print 'NFV CPU load files do not exist at the controller! checking again...'
            time.sleep(pauseTime)

    fileNameNFV1 = 'NFV1.txt'
    fileNameNFV2 = 'NFV2.txt'

    cpu1_old_f = open(fileNameNFV1, 'r')
    cpu2_old_f = open(fileNameNFV2, 'r')

    cpu1_old = cpu1_old_f.read()
    cpu2_old = cpu2_old_f.read()

    cpu1_old_f.close()
    cpu2_old_f.close()

    while(True):

        try:
            # pause before making next query
            time.sleep(pauseTime)
            
            # check if the files exists on the server you are pinging
            while(True):
                ans = os.system(commandToFile)
                # if file found, proceed!
                if ans == 0:
                    break
                else:
                    print 'NFV CPU load files does not exists at the path! checking again...'
                    time.sleep(pauseTime)

            cpu1_f = open(fileNameNFV1, 'r')
            cpu2_f = open(fileNameNFV2, 'r')
            cpu1 = cpu1_f.read()
            cpu2 = cpu2_f.read()
            cpu1_f.close()
            cpu2_f.close()

            # check if the files have changed
            if (cpu1==cpu1_old or cpu2==cpu2_old):
                print('CPU load file did not change! checking again...')
                continue

            print 'CPU load file changed...'

            cpu1_old = cpu1
            cpu2_old = cpu2

            c1 = cpu1.split('\n')
            c2 = cpu2.split('\n')

            array_1 = []
            array_2 = []

            for i in range(1,len(c1)):
            	d1 = c1[i].split('=')[1];
            	d2 = c2[i].split('=')[1];
            	try:
            		d1 = float(d1)
            		d2 = float(d2)
            	except:
            		print('ERROR!!!')
            		continue;
        
                array_1.append(d1)
                array_2.append(d2)

            counter = len(array_1)

            y = range(0,counter)

            print('Plotting...')


            plt.clf()
            vnf1, = plt.plot(y,array_1,'b',label='SNORT-IDS-1')
            vnf2, = plt.plot(y,array_2,'r',label='SNORT-IDS-2')
            plt.xlabel('Time')
            plt.ylabel('% CPU usage')
            plt.axis([0, counter-1, 0, 100])
            plt.title('CPU Usage Graph')
            plt.legend()
            #plt.draw()
            plt.pause(0.1)

        except:

            print 'Unexpected Error! trying again...'
            e = sys.exc_info()[0]
            print('REASON FOR EXCEPTION:')
            print(e)
            time.sleep(pauseTimes)


if __name__ == "__main__":
    # First is nodeName, second is path
    main(sys.argv[1:])

