import xml.etree.ElementTree as ET
import json
import sys

def convert_to_junit(suite_execution_result):
    root = ET.Element("testsuite")

    for completed_execution in suite_execution_result.get("CompletedExecutions", []):
        testcase = ET.SubElement(root, "testcase")
        classname = completed_execution.get("CertifyProcessName", "")
        name = completed_execution.get("Title", "")
        time = str(completed_execution.get("ElapsedTime", ""))

        failed_count = completed_execution.get("TestStepFailedCount")

        # Check if failed_count is not None and is a valid number
        if failed_count is not None and failed_count.isdigit():
            failed_count = int(failed_count)
        else:
            failed_count = 0

        status = "failure" if failed_count > 0 else "success"

        testcase.set("classname", classname)
        if name is not None:
            testcase.set("name", name)
        if time is not None:
            testcase.set("time", time)
        if status is not None:
            testcase.set("status", status)  # Add the status attribute

        if status == "failure":
            failure = ET.SubElement(testcase, "failure")
            failure_message = "Test failed. See Certify logs for details."
            failure.set("message", failure_message)
            failure.text = failure_message

    tree = ET.ElementTree(root)
    tree.write("junit_results.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_to_junit.py <path_to_certify_results.json>")
        sys.exit(1)

    certify_results_path = sys.argv[1]

    with open(certify_results_path, "r") as file:
        certify_results_json = json.load(file)

    convert_to_junit(certify_results_json)