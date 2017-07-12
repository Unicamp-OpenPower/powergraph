FROM ppc64le/ubuntu:16.04

#installing packages and downloading files
RUN apt update && \
	apt install -y ipmitool && \
	apt install -y python2.7 && \
	apt install -y apache2 && \
	apt install -y python-pip && \
	apt install -y git && \
	cd /var/www/ && \
	git clone https://github.com/Unicamp-OpenPower/powergraph.git && \
	cd powergraph/ && \
	pip install -r requirements.txt	&& \
	mv backend/* ../html/ && \
	mv frontend/* ../html/


