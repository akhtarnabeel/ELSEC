#!/bin/bash

sleep 3

# kill all java processes
killall -v java
sleep 1

#run VNF1
java -jar vnf4.jar VNF4.properties


