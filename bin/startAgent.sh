#!/bin/bash
rm log/*
java -cp lib/json-20080701.jar:lib/grinder.jar:lib/commons-io-1.4.jar net.grinder.Grinder scenarier/$1.properties
