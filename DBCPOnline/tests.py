from django.test import TestCase

# Create your tests here.
import os

from DBCP_Scheduler.models import CorrelationConnectivityTask, Server

servers = Server.objects.all()
server = servers[0]
# for server in servers:
IP = server.Server_IP
command = 'ssh root@' + IP + ' mv /root/projects/DataForPreprocess/Data/fmriprep_for_analysis/ /root/projects/DataForPreprocess/'
# print(os.system(command))
print(command)
command = 'ssh root@' + IP + ' rm -rf /root/projects/DataForPreprocess/Data/*'
os.system(command)
#
# command = 'ssh root@' + IP + ' mv /root/projects/DataForPreprocess/fmriprep_for_analysis /root/projects/DataForPreprocess/Data'
# os.system(command)
