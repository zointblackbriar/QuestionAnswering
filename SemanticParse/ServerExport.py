#@Reference plt-tud
#https://github.com/plt-tud/opc_ua_xml_export_client

import argparse
import logging
import sys
import os


logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

from opcua import Client

from XmlExporter import XmlExporter


class ServerExport(object):
    def __init__(self, server_url, outputFile):
        self.nodes = []
        self.namespaces = {}
        self.visited = []
        self.client = None
        self.server_url = server_url
        self.outputFile = outputFile

    def iterater_over_child_nodes(self, node):
        self.nodes.append(node)
        logger.debug("Add %s" % node)
        for child in node.get_children(refs=33):
            if child not in self.nodes:
                self.iterater_over_child_nodes(child)

    def export_xml(self, namespaces=None, output_file="export.xml"):
        if namespaces:
            logger.info("Export only NS %s" % namespaces)
            nodes = [node for node in self.nodes if node.nodeid.NamespaceIndex in namespaces]
        else:
            nodes = self.nodes

        logger.info("Export nodes to %s" % output_file)
        exp = XmlExporter(self.client)
        exp.build_etree(nodes)
        exp.write_xml(output_file)
        logger.info("Export finished")

    def import_nodes(self, server_url="opc.tcp://localhost:16664"):
        from opcua.crypto import security_policies
        import types
        from opcua.ua.uaprotocol_hand import CryptographyNone

        self.client = Client(server_url)

        sec_policy = security_policies.SecurityPolicy()
        sec_policy.symmetric_key_size = 8
        self.client.security_policy = sec_policy

        def signature(self, data):
            return None

        fixed_signature = types.MethodType(signature, CryptographyNone)
        self.client.security_policy.asymmetric_cryptography.signature = fixed_signature

        try:
            self.client.connect()
        except Exception as e:
            logger.error("No connection established", e)
            logger.error(e)
            logger.error("Exiting ...")
            sys.exit()

        logger.info("Client connected to %s" % server_url)

        for ns in self.client.get_namespace_array():
            self.namespaces[self.client.get_namespace_index(ns)] = ns

        root = self.client.get_root_node()
        logger.info("Starting to collect nodes. This may take some time ...")
        self.iterater_over_child_nodes(root)
        logger.info("All nodes collected")

    def statistics(self):
        types = {}
        for node in self.nodes:
            try:
                node_class = str(node.get_node_class())
                ns = node.nodeid.NamespaceIndex
                if ns not in types:
                    types[ns] = {}
                if node_class not in types[ns]:
                    types[ns][node_class] = 1
                else:
                    types[ns][node_class] += 1
            except Exception as e:
                logger.info("some error with %s: %s" % (node, e))

        for ns in types:
            logger.info("NS%d (%s)" % (ns, self.namespaces[ns]))
            for type in types[ns]:
                logger.info("\t%s:\t%d" % (type, types[ns][type]))
        logger.info("\tTOTAL in namespace: %d" % len(self.nodes))


if __name__ == "__main__":
    #exporter = ServerExport("opc.tcp://desktop-674d0i3:62541/DynamicServer", "DynamicServer.xml")
    #exporter = ServerExport("opc.tcp://DESKTOP-674D0I3:26543", "Node-OPCServer.xml")
    exporter = ServerExport("opc.tcp://desktop-674d0i3:48030", "UANodeServer.xml")
    exporter.import_nodes(server_url=exporter.server_url)
    exporter.statistics()
    exporter.export_xml(exporter.namespaces, exporter.outputFile)

exporter.client.disconnect()