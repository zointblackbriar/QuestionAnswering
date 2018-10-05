import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from OPCUAUtils import HandlerClient



obj = HandlerClient("opc.tcp://DESKTOP-674D0I3:26543")
obj.connectClient()
#obj.getEndpoints("opc.tcp://desktop-674d0i3:62541/DynamicServer")
#obj.getEndpoints("opc.tcp://DESKTOP-674D0I3:26543")