from opcua.common import xmlexporter
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class XmlExporter(xmlexporter.XmlExporter):

    def build_etree(self, node_list, uris=None):
        # This is from the library of FreeOPCUA
        logger.info('Building XML etree')

        self._add_namespaces(node_list, uris)

        # add all nodes in the list to the XML etree
        for node in node_list:
            try:
                self.node_to_etree(node)
            except Exception as e:
                logger.warn("Error building etree for node %s: %s" % (node, e))

        # add aliases to the XML etree
        self._add_alias_els()

    def _get_ns_idxs_of_nodes(self, nodes):

        # get a list of all indexes used or references by nodes

        idxs = []
        for node in nodes:
            node_idxs = [node.nodeid.NamespaceIndex]
            try:
                node_idxs.append(node.get_browse_name().NamespaceIndex)
            except Exception:
                logger.error("Namespace Index Problem")
            try:
                node_idxs.extend(ref.NodeId.NamespaceIndex for ref in node.get_references())
            except Exception:
                logger.error("Node.get_references is not working")
            node_idxs = list(set(node_idxs))  # assign to set and remove duplicates
            for i in node_idxs:
                if i != 0 and i not in idxs:
                    idxs.append(i)
        return idxs