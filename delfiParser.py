import xml.etree.ElementTree as elemTree
tree = elemTree.parse('country_data.xml')
root = tree.getroot()