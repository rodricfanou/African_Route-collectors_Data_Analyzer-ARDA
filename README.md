# African_Route-collectors_Data_Analyzer-ARDA

This repository contains the codes used to build the open-source and publicly available application: African
Route-Collectors Data Analyzer (ARDA): https://arda.af-ix.net. The ARDA is the fruit of a 2,5 years collaboration with
UC3M-ISOC from December 2015, aiming at building an open-source platform able to support the growth of IXPs within a
region, in this case, applied to the Internet frontier: AfriNIC Region. The codes released ARDA 1.0 were written by the
authors of their commits : Rodérick Fanou (Architecture design, data collection and Computation modules) and Victor
Sanchez-Agüero (Architecture design, Data Collection and Visualization modules). These codes were implementing ideas
largely discussed by the members of the ISOC-UC3M-IMDEA team composed of: Rodérick Fanou, Victor Sanchez Aguero,
Francisco Valera, Michuki Mwangi, Jane Coffin. Note the scripts are also split into two Virtual Machines (VMs) for
delivering the results to the end-users in nearly real-time: the Computation and the Visualization VMs.

A.R.D.A. is an open-source web application, which offers unique views of the current status of interconnection and
traffic exchange in the African region and its evolution from 2005. A.R.D.A makes use of data collected from all PCH and
RouteViews collectors deployed at existing African IXPs. The computed and displayed statistics are classified into 3
views:

1. The IXP View where we provide several statistics per IXP
2. The National View where we display statistics per set of IXPs in the same country
3. The Regional View where we plot statistics computed based on the data from all IXPs in the region

The application has been launched on April 21, 2017. It can be replicated for/extended to any Internet region for
profiling the IXPs in that region and monitoring their growth: this depends on how it is configured by its
administrator.

As a first step to install it, please download and install these packages:

- automake-1.6.1
- bgp
- bgpatools-0.2
- dateutil-master
- install_bgpdump
- libbgpdump-1.4.99.11
- libev-4.15
- mysql++-3.2.2
- netaddr-0.7.10
- Ocelot-master
- pycountry-1.20
- python-cymru-services-master

Acknowledgements:
This work was partially supported by the Internet Society (ISOC). During ARDA's implementation, technical support have
also been provided by Nishal Goburdhan, Dibya Khatiwada, the JINX technical team, and the Af-IX. 
