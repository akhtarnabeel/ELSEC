#!/bin/bash

sudo mv ~/VNF4/SnortSetup/snort.conf /etc/snort

sudo mv ~/VNF4/SnortSetup/my.rules /etc/snort/rules/my.rules

sudo chmod 755 /etc/snort/snort.conf

sudo chmod 755 /etc/snort/rules/my.rules
