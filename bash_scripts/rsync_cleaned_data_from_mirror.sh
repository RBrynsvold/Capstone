#!/bin/bash

rsync -azv -e "ssh -i ~/aws.pem" vagrant@ec2-54-187-164-38.us-west-2.compute.amazonaws.com:/home/vagrant/ /home/vagrant/data/clean_books
