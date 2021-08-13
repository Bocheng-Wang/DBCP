from django.conf import settings

from DBCP_Scheduler.models import Server
import random


def AquireAvailableServer(type):
    allServer = Server.objects.filter(Server_Type=type, Server_IsBusy=False)
    if len(allServer):
        return random.choice(allServer)
    else:
        return None


def CheckServerIsBusy(server):
    s = Server.objects.get(id=server.id)
    if s.Server_IsBusy:
        return True
    else:
        return False


def PopAvailableServer(Server):
    Server.Server_IsBusy = False
    Server.save()
