from OPCUAUtils import HandlerClient
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
import sys
sys.path.insert(0, "..")
import logging
import time

from opcua import Client
from opcua import ua

class SubHandler:


    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


#if __name__ == "__main__":
    #client = Client("opc.tcp://desktop-674d0i3:62541/DynamicServer")
    obj = HandlerClient
    try:
        #client.connect()
        obj.connectClient("opc.tcp://desktop-674d0i3:62541/DynamicServer")

        # root = client.get_root_node()
        # logger.info("Root node is: {} ".format(root))
        # nameOfRoot = root.get_browse_name()
        # logger.info("name of the root is: {}".format(nameOfRoot))
        # objects = client.get_objects_node()
        # logger.info("Objects node is: {}".format(objects))
        # children = root.get_children()
        # logger.info("Children of root are: {} ".format(children))
        #
        # myfloat = client.get_node("ns=4; s=Double")
        # logger.info("myfloat: {}".format(myfloat))
        # mydouble = client.get_node("ns=4;s=Double")
        # logger.info("mydouble: {}".format(mydouble))
        # myint64 = client.get_node("ns=4;s=Int64")
        # logger.info("myint64: {}".format(myint64))
        # myuint64 = client.get_node("ns=4;s=UInt64")
        # logger.info("myuint64: {}".format(myuint64))
        # myint32 = client.get_node("ns=4;s=Int32")
        # logger.info("myint32: {}".format(myint32))


    except:
        logger.error("There is an error")

    # finally:
    #     obj.disconnect(obj)
