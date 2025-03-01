![CrowdSec Logo](images/logo_crowdsec.png)

# MISP CrowdSec module

## User Guide

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Description](#description)
- [Configuration](#configuration)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Description

This is a MISP module which enriches your knowledge by using CrowdSec's CTI API.

## Configuration

You will find settings page at `http://your-misp-address/servers/serverSettings/Plugin`

![Configurations](images/screenshots/config.png)

Configuration parameters are described below:


| Setting name      | Mandatory | Type | Description                                                                                                                                                                                                                                         |
|-----------------------------------------------| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Plugin.Enrichment_crowdsec_enabled` | Yes  | Boolean | Enable or disable the crowdsec module                                                                                                                                             |
| `Plugin.Enrichment_crowdsec_restrict` | No | String | Restrict the crowdsec module to the given organisation. |
| `Plugin.Enrichment_crowdsec_api_key` | Yes          | String  | CrowdSec CTI  API key. See [instructions to obtain it](https://docs.crowdsec.net/docs/next/cti_api/getting_started/#getting-an-api-key)                                  |
| `Plugin.Enrichment_crowdsec_add_reputation_tag` | No        | String    | Enable/disable the creation of a reputation tag for the IP attribute. You can use  `True` or `False` as string value. Default: `True`     |
| `Plugin.Enrichment_crowdsec_add_behavior_tag` | No     | String    | Enable/disable the creation of a behavior tag for the IP attribute. You can use  `True` or `False` as string value. Default: `True`                                                  |
| `Plugin.Enrichment_crowdsec_add_classification_tag` | No        | String    | Enable/disable the creation of a classification tag for the IP attribute. You can use  `True` or `False` as string value. Default: `True`                                                        |
| `Plugin.Enrichment_crowdsec_add_mitre_technique_tag` | No        | String | Enable/disable the creation of a mitre technique tag for the IP attribute. You can use  `True` or `False` as string value. Default: `True`                                    |
| `Plugin.Enrichment_crowdsec_add_cve_tag` | No | String | Enable/disable the creation of a cve tag for the IP attribute. You can use  `True` or `False` as string value. Default: `True`                                        |


## Usage

Thanks to the CrowdSec Threat Intelligence, you can enrich your IP attributes.

![Enrich IP](images/screenshots/enrich-event-from-left-menu-popup.png)


Once enriched, you will find a `crowdsec-ip-context` object with all attributes retrieved from CrowdSec.

For more details about this object, please refer to the [Misp project documentation](https://www.misp-project.org/objects.html#_crowdsec_ip_context).


![Enriched IP part 1](images/screenshots/enriched-ip-event.png)

![Enriched IP part 2](images/screenshots/enriched-ip-event-2.png)