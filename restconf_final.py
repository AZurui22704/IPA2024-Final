import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.184/restconf/data/ietf-interfaces:interfaces/interface=Loopback{student_id}"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create(student_id):
    ip_suffix = student_id[-3:]
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{student_id}",
            "description": f"Loopback Interface for {student_id}",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": f"172.30.{ip_suffix}.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }
    resp = requests.put(api_url.format(student_id=student_id), data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code in [200, 201]:
        return f"Interface loopback {student_id} is created successfully"
    else:
        return f"Cannot create: Interface loopback {student_id}"


def delete(student_id):
    resp = requests.delete(api_url.format(student_id=student_id), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return f"Interface loopback {student_id} is deleted successfully"
    else:
        return f"Cannot delete: Interface loopback {student_id}"


def enable(student_id):
    yangConfig = {"ietf-interfaces:interface": {"enabled": True}}
    resp = requests.patch(api_url.format(student_id=student_id), data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return f"Interface loopback {student_id} is enabled successfully"
    else:
        return f"Cannot enable: Interface loopback {student_id}"


def disable(student_id):
    yangConfig = {"ietf-interfaces:interface": {"enabled": False}}
    resp = requests.patch(api_url.format(student_id=student_id), data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return f"Interface loopback {student_id} is shutdowned successfully"
    else:
        return f"Cannot shutdown: Interface loopback {student_id}"


def status(student_id):
    resp = requests.get(api_url.format(student_id=student_id), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["enabled"]
        oper_status = response_json.get("ietf-interfaces:interface", {}).get("oper-status", "down")
        if admin_status and oper_status == "up":
            return f"Interface loopback {student_id} is enabled"
        elif not admin_status:
            return f"Interface loopback {student_id} is disabled"
    elif resp.status_code == 404:
        return f"No Interface loopback {student_id}"
    else:
        return "Error retrieving interface status"
    