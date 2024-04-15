import xml.etree.ElementTree as ET

def filter_and_associate_tags(xml_file_path, wildcard_tags):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find and remove elements that do not match the conditions
    for testcase in root.findall(".//testcase"):
        classname = testcase.get('classname')
        if 'NI - SAP - Create Sales Order' not in classname:
            root.remove(testcase)

    # Associate tags with the remaining test cases
    for testcase in root.iter('testcase'):
        classname = testcase.get('classname')
        for wildcard, tags in wildcard_tags.items():
            if wildcard in classname:
                # If the classname contains the specified wildcard, associate tags
                current_tags = testcase.get('tags', '').split(',')
                current_tags.extend(tags)
                testcase.set('tags', ','.join(filter(None, current_tags)))

    tree.write("/var/lib/jenkins/workspace/SAP-Order-To-Cash/certify_results.xml")

# Example usage:
xml_file_path = "/var/lib/jenkins/workspace/SAP-Order-To-Cash/junit_results.xml"
wildcard_tags = {
    'NI - SAP - Create Sales Order': ['TC-50']
}

filter_and_associate_tags(xml_file_path, wildcard_tags)
