# EL-SEC Tutorial on GENI Testbed


<img src="http://groups.geni.net/geni/chrome/common/geni/header.gif"  height="200"/>

### Abstract:

The concept of Virtualized Network Functions (VNFs) aims to move Network Functions (NFs) out of dedicated hardware devices into software that runs on commodity hardware. A single NF consists of multiple VNF instances, usually running on virtual machines in a cloud infrastructure. The elastic management of an NF refers to load management across the VNF instances and the autonomic scaling of the number of VNF instances as load on the NF changes. 

In this demonstration, we present EL-SEC, an autonomic framework to elastically manage security NFs on a virtualized infrastructure. As a use case, we deploy the Snort Intrusion Detection System as the NF on the GENI testbed. Concepts from control theory are used to create an Elastic Manager, which implements various controllers – in this demo, Proportional Integral (PI) and Proportional Integral Derivative (PID) – to direct traffic across the VNF Snort instances by monitoring the current load. RINA (a clean- slate Recursive InterNetwork Architecture) is used to build a distributed application that monitors load and collects Snort alerts, which are processed by the Elastic Manager and an Attack Analyzer, respectively. Software Defined Networking (SDN) is used to steer traffic through the VNF instances, and to block attack traffic. Our demo shows that virtualized security NFs can be easily deployed using our EL-SEC framework. With the help of real-time graphs, we show that PI and PID controllers can be used to easily scale the system, which leads to quicker detection of attacks.

## Getting Started

### Prerequisites
- A [GENI account](https://portal.geni.net/), if you don't have one sign up! 
- Familiarity with how to reserve GENI resources (we will be using the GENI Experimenter Portal as our tool).
- Familiarity with [logging into GENI compute resources](http://groups.geni.net/geni/wiki/HowTo/LoginToNodes).
- Basic understanding of OpenFlow. An OpenFlow tutorial is [here](http://groups.geni.net/geni/wiki/GENIExperimenter/Tutorials/OpenFlowRyu)! 
- Familiarity with the Unix command line.
- Familiarity with the Python programming language. We will use a controller (Ryu controller) written in Python for this tutorial.
- You will need to be a member of a project.

### Tools
-  Open vSwitch 
-  Ryu controller
Both of the tools are already installed on the machines where the resources are provided.

## Tutorial Instruction


![Alt text](http://groups.geni.net/geni/attachment/wiki/GENIExperimenter/Tutorials/Graphics/design.png?format=raw "Design")
## Part 1: DESIGN

## 1. Design the experiment
The basic topology of the tutorial is shown below. We have two sources that will communicate with the destination via an OVS switch. We have four VMs (VNF1, VNF2, VNF3 and VNF4) running instances of the Snort Intrusion Detection System (IDS), representing the Virtual Network Function (VNF). In this tutorial, we will install forwarding rules in the OVS using a controller such that whenever a source sends packets to the destination, a copy of each packet is also sent to one of the IDS for intrusion detection analysis.


<img src="https://raw.githubusercontent.com/akhtarnabeel/ELSEC/master/Figures/GENI.jpeg"  height="350"/>

## 2. Establish environment

### 2.1 Pre-work: (Skip this section if you have already established your environment for your project.)

- Ensure SSH keys are setup. If your SSH keys are not setup before, do the following steps: 
  - Generate an SSH Private Key on the Profile page on the GENI portal 
  - Download the Private Key to ~/Downloads 
  - Open terminal and execute 
    ```
    $ mv ~/Downloads/id_geni_ssh_rsa ~/.ssh/. 
    $ chmod 0600 ~/.ssh/id_geni_ssh_rsa 
    $ ssh-add ~/.ssh/id_geni_ssh_rsa 
    ```
- Ensure you are part of a project. 

## 3. Obtain Resources
For this tutorial, you can use resources from any aggregate in GENI, but preferably an instaGENI aggregate (e.g., CENIC IG or Cornell IG). The experiment will need the following:

  - 1 Xen VM for the OpenFlow controller with a public IP (controller) 
  - 1 Xen VM for the OpenFlow virtual switch (OVS) 
  - 3 Xen VMs, two Sources and one Destination (S1, S2 and destination) 
  - 4 Xen VMs for two Virtual Network Function instances (VNF1, VNF2, VNF3 and VNF4) 

We will need two slices for this tutorial: 

1. A Slice for the OpenFlow controller. 
2. A Slice for the Network consisting of sources, destination, IDSes and OVS. 

To reserve resources, use the GENI portal.

### 3.1. Controller

Open the slice that will run the OpenFlow controller. You may call it 'Controller-xx', with xx replaced with your initials or last name. Select a VM running the controller using the RSpec that is available in the portal called **XEN OpenFlow Controllers**. This is shown in the picture below.


<img src="http://csr.bu.edu/rina/grw-bu2016/tutorial_files/image016.gif"  height="350"/>

Choose any InstaGENI aggregate (e.g. CENIC or Cornell IG) and reserve resources for the controller. You will see the controller VM as shown below.


<img src="http://csr.bu.edu/rina/grw-bu2016/tutorial_files/image018.gif"  height="350"/>

### 3.2. Network

Create a new slice 'Network-xx', with xx replaced by your initials or last name, for a network whose topology will consist of two sources, a destination, an OVS and two VNFs. Use [this given Rspec](https://raw.githubusercontent.com/akhtarnabeel/ELSEC/master/RSPEC/Network_with_NFVimage.xml) to reserve resources for this Network slice.

Although you can choose any InstaGENI aggregate to reserve resources for the Network slice, for this tutorial, it is simpler (and more effective!) to just use the same IG aggregate as the one used for your Controller slice. You will have a network of 8 VMs as shown below. This may take a while!

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/GENI_Network.png"  height="350"/>

### 3.3. Configure and Initialize

Although OVS is installed on the host and is meant to act as a software switch, it still needs to be configured. There are two things that need to be configured:

  (1) configure your software switch with the interfaces as ports and 
  (2) point the switch to the OpenFlow controller.

#### 3.3.1. Configure the Software Switch (OVS Window):

1. Login to the OVS host (on the Network slice)
2. Create an Ethernet bridge that will act as our software switch: 
```
sudo ovs-vsctl add-br br0
```
3. Prepare the interfaces to be added as ports to the OVS switch.  
Your OVS bridge will be a Layer 2 switch and your ports do not need IP addresses. Before we remove them let's keep some information  
    - Run ```ifconfig``` on ovs node  
    - Write down the interface names that correspond to the connections to your VNF1, VNF2, VNF3 and VNF4 hosts. The correspondence is  
      - Interface with IP 10.10.1.13 to VNF1 - ethW  
      - Interface with IP 10.10.1.14 to VNF2 – ethX  
      - Interface with IP 10.10.1.16 to VNF3 – ethY  
      - Interface with IP 10.10.1.17 to VNF4 – ethZ  
  *NOTE: Make sure you have noted the names of the interfaces before you proceed. We will need the interface names to run experiments. (Otherwise, you have to figure out later which OVS interface is connected to each host by pinging from, say, one source to each VNF, after running "sudo tcpdump -i ethX" on each OVS interface.)*

4. Prepare the interfaces to be added as ports to the OVS switch.  
  Your OVS bridge will be a Layer 2 switch and your ports do not need IP addresses. Remove the IP from your data interfaces.   
   ```
   sudo ifconfig eth1 0 
   sudo ifconfig eth2 0 
   sudo ifconfig eth3 0 
   sudo ifconfig eth4 0 
   sudo ifconfig eth5 0 
   sudo ifconfig eth6 0 
   sudo ifconfig eth7 0 
   ```

  *NOTE: Be careful not to bring down eth0. This is the control interface, if you bring that interface down you won't be able to login to your host. For all interfaces other than eth0 and l0, remove the IP from the interfaces (your interface names may vary).*  

Add all the data interfaces to your switch (bridge): Be careful not to add interface eth0. This is the control interface. The other seven interfaces are your data interfaces. (Use the same interfaces as you used in the previous step).
   ```  
   sudo ovs-vsctl add-port br0 eth1 
   sudo ovs-vsctl add-port br0 eth2 
   sudo ovs-vsctl add-port br0 eth3 
   sudo ovs-vsctl add-port br0 eth4 
   sudo ovs-vsctl add-port br0 eth5 
   sudo ovs-vsctl add-port br0 eth6 
   sudo ovs-vsctl add-port br0 eth7 
   ```

  Now the software switch is configured! To verify that the five ports are configured, run the following command to see all five ports listed:  
  ```
  sudo ovs-vsctl list-ports br0 
  ```
  
#### 3.3.2. Point your switch to a controller
*NOTE: An OpenFlow switch will not forward any packet unless instructed by a controller. Basically the forwarding table is empty, until an external controller inserts forwarding rules. The OpenFlow controller communicates with the switch over the control network and it can be anywhere in the Internet as long as it is reachable by the OVS host.*  

1. Login to your controller  
2. Find the control interface IP of your controller, use ifconfig and note down the IP address of eth0.  
3. In order to point our software OpenFlow switch to the controller, in the ovs terminal window, run:  
  ```
  sudo ovs-vsctl set-controller br0 tcp:<controller_ip >:6633
  ```  
4. Set your switch's fail-safe-mode to secure. For more info, read the standalone vs secure mode section below. Run:
  ```
  sudo ovs-vsctl set-fail-mode br0 secure
  ```
5. Trust but verify. You can verify your OVS settings by issuing the following:
  ```
  sudo ovs-vsctl show
  ```
  
##### NOTE: Standalone vs Secure mode 
The OpenFlow controller is responsible for setting up all flows on the switch, which means that when the controller is not running there should be no packet switching at all. Depending on the setup of your network, such a behavior might not be desired. It might be best that when the controller is down, the switch should default back to being a learning layer 2 switch. In other circumstances however this might be undesirable. In OVS this is a tunable parameter, called fail-safe-mode which can be set to the following parameters:  
- standalone [default]: in this case OVS will take responsibility for forwarding the packets if the controller fails.  
- secure: in this case only the controller is responsible for forwarding packets, and if the controller is down all packets are dropped.  

In OVS when the parameter is not set it falls back to the standalone mode. For the purpose of this tutorial we will set the fail-safe-mode to secure, since we want to be the ones controlling the forwarding.
  
#### 3.3.3. Use a simple learning switch controller
This is a very simple example where we are going to run a learning switch control to forward traffic from s1 to VNF1.  
  1. Start a ping from s1 to VNF1 in the window of s1, which should timeout, since there is no controller running.
  ```
  ping vnf1 -c 10
  ```

  2. Run the following command in the controller window to start the simple learning controller:  
  ```
  /tmp/ryu/bin/ryu-manager --verbose /tmp/ryu/ryu/app/simple_switch.py
  ```

  3. Now ping again from s1 to VNF1, the ping should work.  
  4. Stop the Ryu controller by typing Ctrl + c.  
  5. Run the following command in the OVS window to flush all the forwarding rules installed on the OVS node.  
  ```
  sudo ovs-ofctl del-flows br0
  ```

![Alt text](http://groups.geni.net/geni/attachment/wiki/GENIExperimenter/Tutorials/Graphics/execute.png?format=raw "EXECUTE")
## Part II: EXECUTE

In this section, we will use EL-SEC framework to elastically manage NFV resources that we reserved. Figure below shows the different components of EL-SEC that we will run on different GENI nodes.  
Snort IDS will run on each VNF nodes, along with RINA monitoring applications. RINA monitoring application will gather CPU load and Snort alerts from VNF nodes and provide this information to *PI/PID Controllers* and *Attack Anaylzer*. *PI/PID Controllers* will elastically manage load across VNF insatances and provide load balancing information to *OVS controller*. *Attack Analyzer* will process Snort alerts to create attacker-list. Attacker-list is used by *OVS controller* to block traffic from attackers.  
In this experiment, we will use *Port Scanning* attack as an example of attack on the system.

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/GENI_system_hori.jpg"  height="400"/>

## 1. Run RINA monitoring application
The RINA distributed application collects the CPU load of VNF1-VNF4, as well as any Snort alerts generated by the Snort applications running on VNF1 and VNF2. These Snort alerts are collected on the Controller node and saved in file /tmp/snortalerts by the RINA distributed application.

***NOTE: We need Java installed on the VNF1, VNF2, VNF3, VNF4 and controller nodes to run the RINA application. Check if Java is installed using: java -version. If not, install java on VNF1, VNF2, VNF3, VNF4 and controller nodes in new windows (Type Ctrl-C to exit netcat on the sources and destination). To install Java, execute:  ```sudo apt-get install openjdk-7-jdk```
(If the install fails, you may first run: ```sudo apt-get update```. In some cases, you may need to first run: ```sudo add-apt-repository ppa:openjdk-r/ppa``` followed by: ```sudo apt-get update```.)***

1. In the controller window, download the RINA controller code:
```
cd ~
wget https://github.com/akhtarnabeel/public/raw/master/NFV-GENI/Control.tar.gz
tar -xvf Control.tar.gz
```

2. Type ```ifconfig``` to get the IP address of the controller. Save this address as we will need this address to direct the RINA processes on the VNFs to the RINA process on the controller.

3. In a new VNF1 window, download the RINA VNF1 code:
```
cd ~
wget https://github.com/akhtarnabeel/ELSEC/raw/master/VNF1.tar.gz
tar -xvf VNF1.tar.gz
```

2. In a new VNF2 window, download the RINA VNF2 code.
```
cd ~
wget https://github.com/akhtarnabeel/ELSEC/raw/master/VNF2.tar.gz
tar -xvf VNF2.tar.gz
```


3. In a new VNF3 window, download the RINA VNF3 code.
```
cd ~
wget https://github.com/akhtarnabeel/ELSEC/raw/master/VNF3.tar.gz
tar -xvf VNF3.tar.gz
```

4. In a new VNF4 window, download the RINA VNF4 code.
```
cd ~
wget https://github.com/akhtarnabeel/ELSEC/raw/master/VNF4.tar.gz
tar -xvf VNF4.tar.gz
```

5. Now we will change the IP address in the RINA configuration files for *VNF1*, *VNF2*, *VNF3*, *VNF4* and *controller*, so these RINA processes can talk to each other. 
- In the VNF1 window, execute:
```
cd ~/VNF1/RINA
nano ipcVNF1.properties
```
At the bottom of the file, change the *rina.dns.name* and *rina.idd.name* to the IP address of the controller. The following screenshot shows an example.

<img src="http://csr.bu.edu/rina/grw-bu2016/nfv_ryu/pics/DNSIDDConfig.png">  

- In the VNF2 window, execute:  
```
cd ~/VNF2/RINA
nano ipcVNF2.properties
```
  At the bottom of the file, again change the rina.dns.name and rina.idd.name to the IP address of the controller.  

- In the VNF3 window, execute:  
```
cd ~/VNF3/RINA
nano ipcVNF3.properties
```
  At the bottom of the file, again change the rina.dns.name and rina.idd.name to the IP address of the controller.

- In the VNF4 window, execute:  
```
cd ~/VNF4/RINA
nano ipcVNF4.properties
```
  At the bottom of the file, again change the rina.dns.name and rina.idd.name to the IP address of the controller.

- In the controller window, execute:
```
cd ~/Control/RINA
nano ipcControl.properties
```
  At the bottom of the file, again change the rina.dns.name and rina.idd.name to the IP address of the controller.

6. To run the RINA application, follow these steps (make sure you installed Java as noted above):  

- In the controller window, execute the following commands:
```
cd ~/Control/RINA/
./run_controller.sh
```
- In the VNF1 window, execute the following commands:
```
cd ~/VNF1/RINA
./run_VNF1.sh
```
- In the VNF2 window, execute the following commands:
```
cd ~/VNF2/RINA
./run_VNF2.sh
```
- In the VNF3 window, execute the following commands:
```
cd ~/VNF3/RINA
./run_VNF3.sh
```
- In the VNF4 window, execute the following commands:
```
cd ~/VNF4/RINA
./run_VNF4.sh
```

  After sometime, you should see output on CPU load printed on controller node. 

  ***NOTE: The RINA application on VNF1 and VNF2 should be run as soon as possible after the RINA application on the controller is started. If you wait for too long, you will get null values for CPU usage, as the controller's RINA app is not able to subscribe to the CPU load of the VNFs. If this is the case, you should restart all RINA processes.***

  ***NOTE: To stop all RINA processes running on a VM, run ```killall -v java```***


## 2. PI/PID Controller

The PI-controller or PID-controller gets the load information of VNF1, VNF2, VNF3 and VNF4 using RINA's distributed application and makes the load balancing decision.

1. To run the PI-controller, open a new controller window and execute:
```
cd ~/Control/PI_PID_controller
python PI_controller4VNF.py ../RINA/NFV1.txt:../RINA/NFV2.txt:../RINA/NFV3.txt
```
Note that here we are directing PI_controller.py to the NFV1.txt, NFV2.txt, NFV3.txt file that is constantly updated by the RINA distributed application with the load information of VNFs.

*NOTE: You can either use PI or PID controller for the load balancing. If you wish to run PID controller, run ```python PID_controller4VNF.py ../RINA/NFV1.txt:../RINA/NFV2.txt:../RINA/NFV3.txt```.*

2. You should see the VNF state information printed on the screen. A sample output is shown below.

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/PI_output.png">  

Here the target load on VNFs is 50.0% of CPU usage, i.e. if the CPU load on a VNF *i* is more than 50.0%, traffic flows will be diverted to VNF *i+1*. The current CPU load shows the load on VNF1, VNF2 and VNF3. The next line of the output shows the percentage of flows that will be directed to VNF2, VNF3 and VNF4 and the last line shows the flows that were being directed to VNF2, VNF3 and VNF4 before the current control update.

**Do not close this window; leave the PI controller running.**


## 3. PI-based Ryu Controller

Next we are going to run Ryu controller that will install OpenFlow rules to support NFV load balancing as well as handling intrusion. With this controller, the traffic shall go from a source to destination, and duplicate packets are sent to one of the IDS nodes (VNF1, VNF2, VNF3 or VNF4) for intrusion detection.

1. First we need to download the source code and configuration files for the NFV Ryu controller onto the controller VM. In the window of controller, run the following:

```
wget https://github.com/akhtarnabeel/ELSEC/raw/master/RyuController/setup_nfv_ryu_controller.sh
chmod 755 setup_nfv_ryu_controller.sh
./setup_nfv_ryu_controller.sh
```

2. Now you should have all files needed for the NFV Ryu controller. Open *nfv_4VNF.config* file to configure the system parameters. You can use any editor to edit the file, and we use nano here as an example.

```
nano /tmp/ryu/ryu/app/nfv_4VNF.config
```

3. You will see the details of this configuration file as follows. 
  - Change the values of *vnf1_interface*, *vnf2_interface*, *vnf3_interface* and *vnf4_interface* to the values that you noted down in **Section 3.3.1** in the **Design** section of this tutorial (Values of W, X, Y and Z shown in the figure below). These values will tell the controller which interfaces are connected to VNF1, VNF2, VNF3 and VNF4.  
  - Change the value of **file_path_pi** to the text file that has the PI or PID controller's output.  
  */users/\<username\>/Control/PI_controller/NFV_ratio_4VNF.txt*  
  Change the **\<username\>** to your user name.  

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/RyuConfig.png"  height="300"/>

4. Now we can run the Ryu controller. Execute
```
/tmp/ryu/bin/ryu-manager --verbose /tmp/ryu/ryu/app/nfv_controller_4VNF.py
```

## 4. Run Snort
**Note: keep the RINA application processes, PI controller process and PI-based Ryu controller process from the previous 3 steps running in the background.**

1. We need to first configure Snort so that we can use our rules, or snort’s build-in rules to detect the intrusion traffic. To configure Snort, in separate windows for VNF1, VNF2, VNF3 and VNF4, execute the following commands

- For VNF1:
```
cd ~/VNF1/SnortSetup
chmod 755 config_snort.sh
./config_snort.sh
```

- For VNF2:
```
cd ~/VNF2/SnortSetup
chmod 755 config_snort.sh
./config_snort.sh
```

- For VNF3:
```
cd ~/VNF3/SnortSetup
chmod 755 config_snort.sh
./config_snort.sh
```

- For VNF4:
```
cd ~/VNF4/SnortSetup
chmod 755 config_snort.sh
./config_snort.sh
```


2. Make sure that file */etc/snort/rules/my.rules* is empty. This file contains any custom rules to generate Snort attack alerts. For this experiment, we will be using Snort build-in rules for detecting port-scanning attack.

3. Update */etc/snort/snort.conf* to enable the port scanning functionality of Snort. You can update it by uncommenting the following line:
```
preprocessor sfportscan: proto { all } memcap { 10000000 } sense_level { low }
```
and updating it as follows
```
preprocessor sfportscan: proto { all } memcap { 10000000 } sense_level { medium } logfile { /var/log/snort/alert }
```

2. We then run Snort IDS on VNF1, VNF2, VNF3 and VNF4. In separate windows for VNF1, VNF2, VNF3 and VNF4, execute the following command:
```
sudo /usr/local/bin/snort -A full -dev -c /etc/snort/snort.conf -i eth1
```
**Note: exit from previous instances of Snort if they are still running from earlier experiments before you run this instance of Snort.**

**Note: this command is different from Experiment 2. Here we specify the file /etc/snort/snort.conf to indicate which rule files to load.**

When Snort detects intrusion traffic, it will save the alert messages into the file */var/log/snort/alert*. The RINA distributed application keeps reading this alert file, and passes any intrusion information to the Ryu controller which will block the intrusion traffic.

## 5. Run Attack Analyzer
The Attack Analyzer reads the Snort alerts saved on the Controller node and makes decisions about which IP addresses to block. The Attack analyzer is the "brain" on the attack control system. It reads the file ```/tmp/snortalert```, which is generated by RINA on controller node and outputs ```/tmp/attacker.txt``` file which has the IP addresses of all the nodes that the Attack Analyzer decides to block based on Snort alerts.

Open a separate window for the Controller, and run the attack analyzer. 
```
cd ~/Control/AttackAnalyzer/
python AttackAnalyzer.py -f /tmp/snortalert 
```
**Note: If you want to re-run this experiment, make sure to remove ```/tmp/attacker.txt``` and ```/tmp/snortalert``` files on the controller node.**

## 6. Attack the system
We will run *Attacker.py* script to attack the system with Port Scanning attack. You will be running this script on your local machine. The script will remotely connect with S1 or S2 and run port scanning attach from one of these nodes. Note that you need linux or unix machine to run this code. Make sure you have added GENI key to *ssh-add* as shown in **Section 2.1** in **Part 1: Design**.  

- Download *Attacker.py* by running following on your local machine.
```
wget https://raw.githubusercontent.com/akhtarnabeel/ELSEC/master/Attacker.py
```
- Inside the script, change *controller* with address to controller node, *s1_ad* with address to source 1 and *s2_ad* with address to source 2. Example is shown in the figure below.

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/Attacker_py.png" />

- Run the attack by running the *Attacker.py* file on your local machine. A sample output is shown below where it took 8.2 seconds to detect attack

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/Attacker_output.png" />



## 7. Generate background traffic
The attack done is previous step is on unloaded system i.e. there is no background traffic. However, we want to compare how the system scales with EL-SEC and how Background traffic effects the time taken to detect attack.  
Background traffic is generated using script *TrafficGenerator.py*. You will be running this script on your local machine. 

- Download *TrafficGenerator.py* using following script.
```
wget https://raw.githubusercontent.com/akhtarnabeel/ELSEC/master/TrafficGenerator.py
```

- You can change the parameters of traffic generator in the code. Same parameters and their description is given in the figure below.

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/TG_param.png" />

- Change the address to your S1 node (*s1_address*) and S2 node (*s1_address*) in the code. Sample output is shown below

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/TG_SIS2.png" />

- Once you have adjusted parameters of Traffic Generator, you can run it on your local machine by running following command
```
python TrafficGenerator.py 
```
Sample output of Traffic Generator is shown below
<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/TG_output.png" />

## 8. Real Time Load Graph

On any Linux machine (including MAC OS), you can draw real-time CPU usage graphs for VNF1, VNF2, VNF3 and VNF4 nodes. A Matlab script is provided to produce these real-time graphs. The script periodically retrieves the CPU usage file from the Controller node and plots the graph for it.

- Download the python script RealTimeGraph.m to your laptop using the following link.
https://github.com/akhtarnabeel/ELSEC/raw/master/RealtimeGraphs.m

- Update the address to your controller node. Sample output is shown below
<img src="https://raw.githubusercontent.com/akhtarnabeel/ELSEC/master/Figures/RT_con.png" />

- Run the script in matlab. You should see real-time CPU graphs as shown below:  

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/CPU_load_graph.png" />

- You can check the performance of load balancer by increasing/decreasing load on the system by adjusting the parameters of *Traffic Generator*. You can also calculate the time taken to detect attack with and without load on the system using attack generator file *Attacker.py*.


![Alt text](http://groups.geni.net/geni/attachment/wiki/GENIExperimenter/Tutorials/Graphics/finish.png?format=raw "FINISH")
## Part III: FINISH

Tear down Experiment and Release Resources:  

  - After you are done with this experiment, close all your open windows and release your resources. In the GENI Portal, select the slice and click on the Delete button.  

 - Now you can start designing and running your own experiments!


**Author: Nabeel Akhtar
Supervised by: Ibrahim Matta
Boston University
email:  nabeel@bu.edu**


