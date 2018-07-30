
# EL-SEC: ELastic Management of SECurity Applications on Virtualized Infrastructure

### Overview:
The concept of Virtualized Network Functions (VNFs) aims to move Network Functions (NFs) out of dedicated hardware devices into software that runs on commodity hardware. A single NF consists of multiple VNF instances, usually running on virtual machines in a cloud infrastructure. The elastic management of an NF refers to load management across the VNF instances and the autonomic scaling of the number of VNF instances as load on the NF changes. Here provide EL-SEC, an autonomic framework to elastically manage security NFs on a virtualized infrastructure.

As a use case, we deploy the Snort Intrusion Detection System as the NF on the GENI testbed. Concepts from control theory are used to create an Elastic Manager, which implements various controllers – in this use case, Proportional Integral (PI) and Proportional Integral Derivative (PID) – to direct traffic across the VNF Snort instances by monitoring the current load. RINA (a clean-slate Recursive InterNetwork Architecture) is used to build a distributed application that monitors load and collects Snort alerts, which are processed by the Elastic Manager and an Attack Analyzer, respectively. Software Defined Networking (SDN) is used to steer traffic through the VNF instances, and to block attack traffic. Our results shows that virtualized security NFs can be easily deployed using our EL-SEC framework. With the help of real-time graphs, we show that PI and PID controllers can be used to easily scale the system, which leads to quicker detection of attacks.

<img src="https://github.com/akhtarnabeel/ELSEC/raw/master/Figures/EL_SEC_Overview.jpg" />

## Tutorial on GENI Testbed:
[Link](https://github.com/akhtarnabeel/ELSEC/blob/master/Tutorial.md) to EL-SEC Tutorial

## Video Demonstration:
[Link](https://www.youtube.com/watch?v=2T_d_J4AVn8) EL-SEC Elastic Management on GENI testbed

## Source Code:
[Source code](https://github.com/akhtarnabeel/ELSEC) of our GENI implementation is available on GitHub

## Experiment Traces:
[Link](https://github.com/akhtarnabeel/ELSEC/tree/master/ExperimentalTraces) to experiment traces.

## Publications:

- Nabeel Akhtar, Ibrahim Matta, Ali Raza and Yuefeng Wang <br>
  **EL-SEC: ELastic Management of SECurity Applications on Virtualized Infrastructure** <br>
  *IEEE INFOCOM International Workshop on Computer and Networking Experimental Research Using Testbeds (CNERT), 2018, Honolulu, Hawaii, USA, April 2018* <br>
    [\[PDF\]](http://cs-people.bu.edu/nabeel/papers/ELSEC.pdf)[\[Bibtex\]](http://cs-people.bu.edu/nabeel/papers/bib/ELSEC.txt)[\[ProjetPage\]](https://github.com/akhtarnabeel/ELSEC) <br>



- Nabeel Akhtar, Ibrahim Matta and Yuefeng Wang <br>
  **Managing NFV using SDN and Control Theory** <br>
  *IEEE/IFIP NOMS International Workshop on Management of the Future Internet (ManFI) 2016, Istanbul, Turkey, April 2016* <br>
  [\[PDF\]](http://cs-people.bu.edu/nabeel/papers/NOMS2016.pdf) [\[Bibtex\]](http://cs-people.bu.edu/nabeel/papers/bib/NOMS2016.txt) 
  


