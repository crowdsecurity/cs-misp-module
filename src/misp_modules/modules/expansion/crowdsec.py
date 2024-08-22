import json

import pycountry
import requests
from pymisp import MISPEvent, MISPObject

from . import check_input_attribute, standard_error_message

mispattributes = {"input": ["ip-dst", "ip-src"], "format": "misp_standard"}
moduleinfo = {
    "version": "2.1",
    "author": "Shivam Sandbhor <shivam@crowdsec.net>",
    "description": "Module to access CrowdSec CTI API.",
    "module-type": ["hover", "expansion"],
}
moduleconfig = [
    "api_key",
    "add_reputation_tag",
    "add_behavior_tag",
    "add_classification_tag",
    "add_mitre_technique_tag",
    "add_cve_tag",
]

crowdsec_template = {
    "attributes": {
        "as-name": {
            "categories": ["Network activity", "External analysis"],
            "description": "Autonomous system name",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": True,
            "ui-priority": 0,
        },
        "as-num": {
            "categories": ["Network activity", "External analysis"],
            "description": "Autonomous system number",
            "disable_correlation": True,
            "misp-attribute": "AS",
            "multiple": True,
            "ui-priority": 0,
        },
        "attack-details": {
            "description": "Triggered scenarios",
            "disable_correlation": True,
            "misp-attribute": "text",
            "ui-priority": 1,
        },
        "background-noise": {
            "description": "High background noise scores highlight untargeted, mild threat mass-attacks",
            "disable_correlation": True,
            "misp-attribute": "float",
            "ui-priority": 1,
        },
        "behaviors": {
            "description": "Attack categories",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": True,
            "ui-priority": 1,
        },
        "city": {
            "description": "City of origin",
            "disable_correlation": True,
            "misp-attribute": "text",
            "ui-priority": 1,
        },
        "classifications": {
            "description": "Classification category of the IP address",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": True,
            "ui-priority": 1,
        },
        "country": {
            "description": "Country of origin",
            "disable_correlation": True,
            "misp-attribute": "text",
            "ui-priority": 1,
        },
        "country-code": {
            "description": "Country Code",
            "disable_correlation": True,
            "misp-attribute": "text",
            "ui-priority": 0,
        },
        "cves": {
            "description": "CVEs",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": True,
            "ui-priority": 1,
        },
        "dst-port": {
            "categories": ["Network activity", "External analysis"],
            "description": "Destination port",
            "disable_correlation": True,
            "misp-attribute": "port",
            "multiple": True,
            "ui-priority": 1,
        },
        "false-positives": {
            "description": "False positive category of the IP address",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": True,
            "ui-priority": 1,
        },
        "ip": {
            "categories": ["Network activity", "External analysis"],
            "description": "IP Address",
            "misp-attribute": "ip-src",
            "ui-priority": 1,
        },
        "ip-range": {
            "categories": ["Network activity", "External analysis"],
            "description": "destination IP address",
            "misp-attribute": "text",
            "ui-priority": 1,
        },
        "ip-range-score": {
            "categories": ["Network activity", "External analysis"],
            "description": "destination IP address",
            "disable_correlation": True,
            "misp-attribute": "float",
            "ui-priority": 1,
        },
        "latitude": {
            "description": "Latitude of origin",
            "disable_correlation": True,
            "misp-attribute": "float",
            "ui-priority": 1,
        },
        "longitude": {
            "description": "Longitude of origin",
            "disable_correlation": True,
            "misp-attribute": "float",
            "ui-priority": 1,
        },
        "mitre-techniques": {
            "description": "MITRE ATT&CK techniques",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": True,
            "ui-priority": 1,
        },
        "reputation": {
            "description": "IP reputation",
            "disable_correlation": True,
            "misp-attribute": "text",
            "multiple": False,
            "ui-priority": 1,
        },
        "reverse-dns": {
            "categories": ["Network activity", "External analysis"],
            "description": "Reverse DNS name",
            "misp-attribute": "hostname",
            "ui-priority": 1,
        },
        "scores": {
            "description": "Scores",
            "disable_correlation": True,
            "misp-attribute": "text",
            "ui-priority": 1,
        },
        "target-countries": {
            "description": "Target countries (top 10)",
            "disable_correlation": True,
            "misp-attribute": "text",
            "ui-priority": 1,
        },
        "trust": {
            "description": "Trust level",
            "disable_correlation": True,
            "misp-attribute": "float",
            "ui-priority": 1,
        },
    },
    "description": "CrowdSec Threat Intelligence - IP CTI search",
    "meta-category": "network",
    "name": "crowdsec-ip-context",
    "requiredOneOf": ["ip"],
    "uuid": "0f0a6def-a351-4d3b-9868-d732f6f4666f",
    "version": 4,
}


def handler(q=False):
    if q is False:
        return False

    request = json.loads(q)
    if not request.get("config"):
        return {"error": "Missing CrowdSec Config"}

    if not request["config"].get("api_key"):
        return {"error": "Missing CrowdSec API key"}

    if not request.get("attribute") or not check_input_attribute(request["attribute"]):
        return {
            "error": f"{standard_error_message}, which should contain at least a type, a value and an uuid."
        }

    if request["attribute"].get("type") not in mispattributes["input"]:
        return {
            "error": f"Wrong input type. Please choose on of the following: {', '.join(mispattributes['input'])}"
        }

    return _handler_v2(request)


def _get_boolean_config(request_data, config: str, default_config: bool):
    if request_data["config"].get(config) is None:
        return default_config
    raw_config = request_data["config"].get(config).lower()
    # falsy values, return False
    if raw_config in ["false", "0", "no", "off"]:
        return False
    # truthy values, return True
    if raw_config in ["true", "1", "yes", "on"]:
        return True
    return default_config


def _handler_v2(request_data):
    attribute = request_data["attribute"]
    ip = attribute["value"]

    crowdsec_cti = requests.get(
        f"https://cti.api.crowdsec.net/v2/smoke/{ip}",
        headers={
            "x-api-key": request_data["config"]["api_key"],
            "User-Agent": "crowdsec-misp/v2.1.0",
        },
    )
    crowdsec_cti.raise_for_status()
    crowdsec_cti = crowdsec_cti.json()

    add_reputation_tag = _get_boolean_config(request_data, "add_reputation_tag", True)
    add_behavior_tag = _get_boolean_config(request_data, "add_behavior_tag", True)
    add_classification_tag = _get_boolean_config(
        request_data, "add_classification_tag", True
    )
    add_mitre_technique_tag = _get_boolean_config(
        request_data, "add_mitre_technique_tag", True
    )
    add_cve_tag = _get_boolean_config(request_data, "add_cve_tag", True)

    misp_event = MISPEvent()
    misp_attribute = misp_event.add_attribute(**attribute)
    crowdsec_context_object = MISPObject(
        "crowdsec-ip-context", misp_objects_template_custom=crowdsec_template
    )
    crowdsec_context_object.from_dict(
        first_seen=crowdsec_cti["history"]["first_seen"],
        last_seen=crowdsec_cti["history"]["last_seen"],
    )
    ip_attribute = crowdsec_context_object.add_attribute("ip", crowdsec_cti["ip"])
    reputation = crowdsec_cti["reputation"] or "unknown"
    crowdsec_context_object.add_attribute("reputation", reputation)
    if add_reputation_tag:
        tag = f'crowdsec:reputation="{reputation}"'
        ip_attribute.add_tag(tag)
    crowdsec_context_object.add_attribute("ip-range", crowdsec_cti["ip_range"])
    crowdsec_context_object.add_attribute(
        "ip-range-score", crowdsec_cti["ip_range_score"]
    )
    crowdsec_context_object.add_attribute(
        "country", get_country_name_from_alpha_2(crowdsec_cti["location"]["country"])
    )
    crowdsec_context_object.add_attribute(
        "country-code", crowdsec_cti["location"]["country"]
    )
    if crowdsec_cti["location"].get("city"):
        crowdsec_context_object.add_attribute("city", crowdsec_cti["location"]["city"])
    crowdsec_context_object.add_attribute(
        "latitude", crowdsec_cti["location"]["latitude"]
    )
    crowdsec_context_object.add_attribute(
        "longitude", crowdsec_cti["location"]["longitude"]
    )
    crowdsec_context_object.add_attribute("as-name", crowdsec_cti["as_name"])
    crowdsec_context_object.add_attribute("as-num", crowdsec_cti["as_num"])
    if crowdsec_cti.get("reverse_dns") is not None:
        crowdsec_context_object.add_attribute(
            "reverse-dns", crowdsec_cti["reverse_dns"]
        )
    crowdsec_context_object.add_attribute(
        "background-noise", crowdsec_cti["background_noise_score"]
    )
    for behavior in crowdsec_cti["behaviors"]:
        crowdsec_context_object.add_attribute(
            "behaviors", behavior["label"], comment=behavior["description"]
        )
        if add_behavior_tag:
            tag = f'crowdsec:behavior="{behavior["name"]}"'
            ip_attribute.add_tag(tag)
    for technique in crowdsec_cti["mitre_techniques"]:
        technique_name = technique["name"]
        mitre_url = (
            f"https://attack.mitre.org/tactics/{technique_name}"
            if technique_name.startswith("TA")
            else f"https://attack.mitre.org/techniques/{technique_name}"
        )
        crowdsec_context_object.add_attribute(
            "mitre-techniques",
            technique["label"],
            comment=f'{technique["description"]} ({mitre_url})',
        )
        if add_mitre_technique_tag:
            tag = f'crowdsec:mitre-technique="{technique_name}"'
            ip_attribute.add_tag(tag)

    for cve in crowdsec_cti["cves"]:
        cve_url = f"https://nvd.nist.gov/vuln/detail/{cve}"
        crowdsec_context_object.add_attribute("cves", cve, comment=cve_url)
        if add_cve_tag:
            tag = f'crowdsec:cve="{cve}"'
            ip_attribute.add_tag(tag)

    for feature, values in crowdsec_cti["classifications"].items():
        field = feature[:-1]
        for value in values:
            crowdsec_context_object.add_attribute(
                feature, value["label"], comment=value["description"]
            )
            if add_classification_tag:
                tag = f'crowdsec:{field}="{value["name"]}"'
                ip_attribute.add_tag(tag)
    crowdsec_context_object.add_attribute(
        "attack-details",
        ", ".join(
            f"{scenario['name']} - {scenario['label']} ({scenario['description']})"
            for scenario in crowdsec_cti["attack_details"]
        ),
    )
    crowdsec_context_object.add_attribute(
        "target-countries",
        ", ".join(
            map(get_country_name_from_alpha_2, crowdsec_cti["target_countries"].keys())
        ),
    )
    crowdsec_context_object.add_attribute(
        "trust", crowdsec_cti["scores"]["overall"]["trust"]
    )
    scores = []
    for time_period, indicators in crowdsec_cti["scores"].items():
        tp = " ".join(map(str.capitalize, time_period.split("_")))
        indicator = (
            f"{indicator_type.capitalize()}: {indicator_value}"
            for indicator_type, indicator_value in indicators.items()
        )
        scores.append(f"{tp}: {' - '.join(indicator)}")
    crowdsec_context_object.add_attribute("scores", ", ".join(scores))
    crowdsec_context_object.add_reference(misp_attribute.uuid, "related-to")
    misp_event.add_object(crowdsec_context_object)

    event = json.loads(misp_event.to_json())
    results = {
        key: event[key]
        for key in ("Attribute", "Object")
        if (key in event and event[key])
    }
    return {"results": results}


def get_country_name_from_alpha_2(alpha_2):
    country_info = pycountry.countries.get(alpha_2=alpha_2)
    return country_info.name if country_info else None


def introspection():
    return mispattributes


def version():
    moduleinfo["config"] = moduleconfig
    return moduleinfo
