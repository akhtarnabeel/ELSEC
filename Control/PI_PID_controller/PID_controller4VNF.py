__author__ = 'Nabeel'
import time, sys


def main(args):

    path = args[1].strip(' \n').split(':')

    file1 = open(path[0], 'r')
    file2 = open(path[1], 'r')
    file3 = open(path[2], 'r')
    NFV1 = file1.read()
    NFV2 = file2.read()
    NFV3 = file3.read()

    NFV1_old = NFV1
    NFV2_old = NFV2
    NFV3_old = NFV3


    T = 50.0     # target load
    X_t_1 = {'VNF1': 0.0, 'VNF2': 0.0, 'VNF3': 0.0}  # load on VNF at t-1 (past)
    X_t = {'VNF1': 0.0, 'VNF2': 0.0, 'VNF3': 0.0}  # load on VNF at t (now)
    Ki = 0.1     # how fast to change
    Kd = 0.1     # K for D
    L_t_1 = {'VNF1': 0.0, 'VNF2': 0.0, 'VNF3': 0.0}  # load on VNF at t-1
    L_t = {'VNF1': 0.0, 'VNF2': 0.0, 'VNF3': 0.0}  # load on VNF at t (now)

    while(True):

        time.sleep(1.5)

        # that means files have changed
        if NFV1_old != NFV1 and NFV2_old != NFV2 and NFV3_old != NFV3:
            try:
                NFV1_latest = float(NFV1.split("=")[-1])
                NFV2_latest = float(NFV2.split("=")[-1])
                NFV3_latest = float(NFV3.split("=")[-1])

                NFV1_old = (NFV1_old.split("=")[-1])
                NFV2_old = (NFV2_old.split("=")[-1])
                NFV3_old = (NFV3_old.split("=")[-1])

            except:
                print "Error is converting values!!!"
                NFV1_old = NFV1
                NFV2_old = NFV2
                NFV3_old = NFV3
                file1 = open(path[0], 'r')
                file2 = open(path[1], 'r')
                file3 = open(path[2], 'r')
                NFV1 = file1.read()
                NFV2 = file2.read()
                NFV3 = file3.read()
                continue;

            prev = {'VNF1':0.0,'VNF2':0.0,'VNF3':0.0}

            for i in range(len(path)):

                if i == 0:
                    nam = 'VNF'+str(i+1)
                    L_t[nam] = NFV1_latest
                    X_t[nam] = max(0, min(1, X_t_1[nam] + Ki * (L_t[nam] - T) / T + Kd * (((L_t[nam] - T) / T) - ((L_t_1[nam] - T) / T))))
                    # updates things
                    NFV1_old = NFV1
                    prev[nam] = X_t_1[nam]
                    X_t_1[nam] = X_t[nam]
                    L_t_1[nam] = L_t[nam]
                elif i == 1:
                    nam = 'VNF' + str(i+1)
                    L_t[nam] = NFV2_latest
                    X_t[nam] = max(0, min(1, X_t_1[nam] + Ki * (L_t[nam] - T) / T + Kd * (((L_t[nam] - T) / T) - ((L_t_1[nam] - T) / T))))
                    # updates things
                    NFV2_old = NFV2
                    prev[nam] = X_t_1[nam]
                    X_t_1[nam] = X_t[nam]
                    L_t_1[nam] = L_t[nam]
                elif i == 2:
                    nam = 'VNF' + str(i+1)
                    L_t[nam] = NFV3_latest
                    X_t[nam] = max(0, min(1, X_t_1[nam] + Ki * (L_t[nam] - T) / T + Kd * (((L_t[nam] - T) / T) - ((L_t_1[nam] - T) / T))))
                    # updates things
                    NFV3_old = NFV3
                    prev[nam] = X_t_1[nam]
                    X_t_1[nam] = X_t[nam]
                    L_t_1[nam] = L_t[nam]
                else:
                    print 'ERROR IN UPDATING VALUES!!!'
                    NFV1_old = NFV1
                    NFV2_old = NFV2
                    NFV3_old = NFV3
                    file1 = open(path[0], 'r')
                    file2 = open(path[1], 'r')
                    file3 = open(path[2], 'r')
                    NFV1 = file1.read()
                    NFV2 = file2.read()
                    NFV3 = file3.read()
                    continue;

            print "** PID CONTROLLER **"
            print "Target CPU load =", T, " %"
            print "|-------------------------------------------------------------|"
            print "|                     |  VNF1   |  VNF2   |  VNF3   |  VNF4   |"
            print "|-------------------------------------------------------------|"
            print "|Current CPU load (%) | ", change6str(NFV1.split("=")[-1]), " | ",change6str(NFV2.split("=")[-1])," | ",change6str(NFV3.split("=")[-1])," |         |"
            print "|% Flows sent VNF i+1 |         | ", change6str(X_t['VNF1'] * 100), " | ",change6str(X_t['VNF2'] * 100), " | ", change6str(X_t['VNF3'] * 100)," | "
            print "|-------------------------------------------------------------|"
            #print "% of flows previously send to VNF2, VNF3 and VNF4:: ", prev['VNF1'] * 100, '%', ' : ',prev['VNF2'] * 100, '%', ' : ',prev['VNF3'] * 100, '%'
            print ""

            f_out = open("NFV_ratio_4VNF.txt",'w')
            f_out.write("X="+str(X_t['VNF1'])+':'+"X="+str(X_t['VNF2'])+':'+"X="+str(X_t['VNF3']))

        file1 = open(path[0], 'r')
        file2 = open(path[1], 'r')
        file3 = open(path[2], 'r')
        NFV1 = file1.read()
        NFV2 = file2.read()
        NFV3 = file3.read()

def change6str(num):
    num = float(str(num))
    num = "{0:.04f}".format(num)
    num = "{0:.05}".format(num)
    return num


if __name__ == "__main__":
   main(sys.argv)
