## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
#!/bin/bash
PASSWORD=PASS

## Goal: create RIRs database destined to host data collected by the RIRs
#+-------------------------+
#| Tables_in_RIRs          |
#+-------------------------+
#| ASNs_AFRINIC            |
#| ASNs_APNIC              |
#| ASNs_ARIN               |
#| ASNs_LACNIC             |
#| ASNs_RIPE               |
#| IPv4_ressources_AFRINIC |
#| IPv4_ressources_APNIC   |
#| IPv4_ressources_ARIN    |
#| IPv4_ressources_LACNIC  |
#| IPv4_ressources_RIPE    |
#| IPv6_ressources_AFRINIC |
#| IPv6_ressources_APNIC   |
#| IPv6_ressources_ARIN    |
#| IPv6_ressources_LACNIC  |
#| IPv6_ressources_RIPE    |
#| IXPs_launch_date        |
#+-------------------------+
mysql -uroot -p $PASSWORD -Bse "CREATE DATABASE IF NOT EXISTS RIRs;"
  
  
mysql -uroot -p $PASSWORD -D RIRs -s -e"CREATE TABLE IF NOT EXISTS RIRs.ASNs_AFRINIC(
ASN VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
date VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
PRIMARY KEY (ASN));

CREATE TABLE IF NOT EXISTS RIRs.ASNs_APNIC(
ASN VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
date VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
PRIMARY KEY (ASN));


CREATE TABLE IF NOT EXISTS RIRs.ASNs_ARIN(
ASN VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
date VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
PRIMARY KEY (ASN));


CREATE TABLE IF NOT EXISTS RIRs.ASNs_LACNIC(
ASN VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
date VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
PRIMARY KEY (ASN));


CREATE TABLE IF NOT EXISTS RIRs.ASNs_RIPE(
ASN VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
date VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
PRIMARY KEY (ASN));



CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_AFRINIC (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_APNIC (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_LACNIC (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_ARIN (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_RIPE (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));



CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_AFRINIC (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_APNIC (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_LACNIC (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_ARIN (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));


CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_RIPE (
Al_id INT NOT NULL AUTO_INCREMENT,
NetIPaddress VARCHAR(50) NOT NULL,
Numb_IPadd VARCHAR(50) NOT NULL,
NetBits VARCHAR(50) NOT NULL,
CC VARCHAR(50) NULL,
Status VARCHAR(50) NULL,
date VARCHAR(50) NULL,
PRIMARY KEY (Al_id));

"


