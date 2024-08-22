![CrowdSec Logo](images/logo_crowdsec.png)

# MISP CrowdSec module

## Installation Guide

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Requirements](#requirements)
- [Installation](#installation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Requirements

- A CrowdSec CTI API key. See [instructions to obtain it](https://docs.crowdsec.net/docs/next/cti_api/getting_started/#getting-an-api-key)


## Installation

Enabling this module could be done by browsing to the Plugins tab of your MISP instance: 

- Navigate to plugin settings page at `http://your-misp-address/servers/serverSettings/Plugin`
- Click on Enrichment
- Set the value of `Plugin.Enrichment_crowdsec_enabled` to `true`
- Set the value of `Plugin.Enrichment_crowdsec_api_key` to your CrowdSec CTI API key

For more details on the settings available, please refer to the [User Guide](../USER_GUIDE.md#configuration).