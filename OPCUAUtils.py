#This file only for testing purposes

import logging
import time
import sys
from opcua import ua
from opcua import Client
from opcua.tools import endpoint_to_strings
from opcua import crypto
from opcua import Node
import AppLogger
from opcua import Client
from opcua import ua

class HandlerClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self._client = None
        self.root = None
        self._objects = None
        self._serverNodes = None
        self._connected = None
        self._datachange_sub = None
        self._event_sub = None
        self._subs_dc = {}
        self._subs_ec = {}

    def dataChangeNotification(self, node, val, data):
        AppLogger.log.info("Python: new data change even")

    def eventNotification(self, event):
        print("Python: New event", event)


    def connectClient(self):
        self._client = Client(self.endpoint)
        try:
            self._client.connect()
            AppLogger.log.info("Client connected")
            self._client.load_type_definitions()
            AppLogger.log.info("Type definitions loaded")
            #You do not need to create a session here
            #connect() function handle it

            self.root=self._client.get_root_node()
            print("Write here the root node" ,self.root)
            self._objects = self._client.get_objects_node()
            print("Write object node here", self._objects)
            self._serverNodes = self._client.get_server_node()
            print("Server node is here", self._serverNodes)
            getNode = self.get_node("42")
            print("Specific Node is here", getNode)

            #Read Custom Structure
            #self.readCustomStructures()
            #print(self.get_node_attrs(self.root))
            #print(self.get_node_attrs(self._objects))
            #print("Write all children values", self.get_children(self.root))

            #Delete Nodes
            #self.testDeleteNodes()
            #self._client.close_session()

        except Exception as e:
            AppLogger.log.error("Something wrong in the connection" + str(e))

        finally:
            self._client.disconnect()

    def getEndpoints(self, uri):
        client = Client(uri, timeout=15)
        client.connect_and_get_server_endpoints()
        endpoints = client.connect_and_get_server_endpoints()
        for ı, ep in enumerate(endpoints, start=1):
            AppLogger.log.info('Endpoint %s:', ı)
            for(n, v) in endpoint_to_strings(ep):
                AppLogger.log.info('%s: %s', n, v)
            AppLogger.log.info('')
        return endpoints

    def readCustomStructures(self):
        structofAClient = self._client.get_node("ns=2, i=1")
        result = structofAClient.get_value()
        print("struct result is", result)


    def get_children(self, node):
        descs = node.get_children_descriptions()
        descs.sort(key=lambda x: x.BrowseName)
        return descs

    def get_node_attrs(self, node):
        if not isinstance(node, Node):
            node = self._client.get_node(node)
        attrs = node.get_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
        return node, [attr.Value.Value.to_string() for attr in attrs]


    def get_node(self, nodeId):
        return self._client.get_node(nodeId)

    def subscribe_datachange(self, node, handler):
        if not self._datachange_sub:
            self._datachange_sub = self._client.create_subscription(500, handler)
        handle = self._datachange_sub.subscribe_data_change(node)
        self.subs_dc[node.nodeId] = handle
        return handle

    def unsubscribe_datachange(self, node):
        self._datachange_sub.unsubscribe(self._subs_dc[node.nodeId])

    def subscribe_events(self, node, handler):
        if not self._event_sub:
            print("subscribing with handler: ", handler, dir(handler))
            self._event_sub = self._client.create_subscription(500, handler)
        handle = self._event_sub.subscribe_events(node)
        self._sub_ev[node.nodeId] = handle
        return handle

    def unsubscribe_events(self, node):
        self._event_sub.unsubscribe(self._subs.ev[node.nodeid])

    def get_node_attrs(self, node):
        if not isinstance(node, Node):
            node = self._client.get_node(node)
        #take attributes
        attrs = node.get_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
        return node, [attr.Value.Value.to_string() for attr in attrs]

    def testDeleteNodes(self):
        folder = self._objects.add_folder("ns=2; i=2", "2:Folder1")
        var = folder.add_variables("ns=1; i=1", "2 Variable1", 3.45)
        #Now getting a variable node using its browse path
        var.set_value(9.89)

        results = self._client.delete_nodes([folder, var])
        try:
            var.get_browse_name()
        except ua.UaStatusCodeError:
            print("The variable has been removed OK")


