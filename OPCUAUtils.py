#This file only for testing purposes

import logging
import sys


from opcua import ua
from opcua import Client
from opcua.tools import endpoint_to_strings
from opcua import crypto
from opcua import Node

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HandlerClient:
    def __init__(self):
        self.client = None
        self._connected = False
        self._datachange_sub = None
        self._event_sub = None
        self._subs_dc = {}
        self._subs_ev = {}
        self.security_mode = None
        self.security_policy = None
        self.certificate_path = None
        self.private_key_path = None

    def helloSession(self):
        print('hello')

    def connectClient(self, uri):
        logger.info("Call disconnect and clear the memory")
        #self.disconnect()
        logger.info("connect method is started")
        self.client = Client(uri)
        if self.security_mode is not None and self.security_policy is not None:
            self.client.set_security(
                getattr(crypto.security_policies, 'SecurityPolicy' + self.security_policy),
                self.certificate_path,
                self.private_key_path,
                mode=getattr(ua.MessageSecurityMode, self.security_mode)
            )
        self.client.connect()
        self._connected = True
        self.save_secutity_settings(uri)

    def datachange_notification(self, node, val, data):
        print("python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

    def get_endpoints(uri, timeout=2):
        logger.info("Fetch all endpoints")
        client = Client(uri, timeout=2)
        client.connect_and_get_server_endpoints()
        endpoints = client.connect_and_get_server_endpoints()
        if(endpoints is None):
            logger.error("Endpoints are null")
        for counter, endp in enumerate(endpoints, start=1):
            logger.info('Endpoint %s:', counter)
            for(n, v) in endpoint_to_strings(endp):
                logger.info(' %s: %s', n, v)
            logger.info('')
        return endpoints

    def load_security_settings(self, uri):
        self.security_mode = None
        self.security_policy = None
        self.certificate_path = None
        self.private_key_path = None

        private_settings = self.settings.value("security_settings", None)
        logger.info("private settings loaded")
        if private_settings is None:
            return
        if uri in private_settings:
            mode, policy, cert, key = private_settings[uri]
            self.security_mode = None
            self.security_policy = None
            self.certificate_path = None
            self.private_key_path = None

    def retrieve_node(self, nodeId):
        logger.info("retrieve node is started")
        return self.client.get_node(nodeId)

    def disconnect(self):
        if self._connected:
            logger.info("Disconnecting from server")
            self._connected = False
            try:
                self.client.disconnect()
            finally:
                self._reset()

    def subscribe_datachange(self, node, handler):
        logger.info("subscribe_datachange")
        if not self._datachange_sub:
            self._datachange_sub = self.client.create_subscription(500, handler)
        handle = self._datachange_sub.subscribe_data_change(node)
        self._subs_dc[node.nodeId] = handle
        return handle

    def unsubscribe_datachange(self, node):
        self._datachange_sub.unsubscribe(self._subs_ev[node.nodeId])

    def get_node_attrs(self, node):
        if not isinstance(node, Node):
            node = self.client.get_node(node)
        attrs = node.get_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
        return node, [attrs.value.Value.to_string() for attr in attrs]

    @staticmethod
    def get_children(node):
        descs = node.get_children_descriptions()
        descs.sort(key=lambda x: x.BrowseName)
        return descs




