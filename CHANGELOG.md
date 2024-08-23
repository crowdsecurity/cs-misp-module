# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## SemVer public API

The [public API](https://semver.org/spec/v2.0.0.html#spec-item-1)  for this project is defined by the set of functions provided by the `src/misp_modules/modules/expansion/crowdsec.py` file.

---

## [2.1.1](https://github.com/crowdsecurity/cs-misp-module/releases/tag/v2.1.1) - 2024-08-23
[_Compare with previous release_](https://github.com/crowdsecurity/cs-misp-module/compare/v2.1.0...v2.1.1)

### Fixed

- Check if the IP is valid before calling CrowdSec API
- Use `crowdsec-ip-context` template from [MISP objects repository](https://github.com/MISP/misp-objects/tree/main/objects/crowdsec-ip-context)

---


## [2.1.0](https://github.com/crowdsecurity/cs-misp-module/releases/tag/v2.1.0) - 2024-08-22
[_Compare with previous release_](https://github.com/crowdsecurity/cs-misp-module/compare/v2.0.0...v2.1.0)

### Added

- Add attribute and tag for reputation, mitre techniques and cves
- Add config to enable/disable tag creation for IP attributes

---

## [2.0.0](https://github.com/crowdsecurity/cs-misp-module/releases/tag/v2.0.0) - 2024-08-02

- Initial release: synchronization with [MISP modules `v2.4.195` release](https://github.com/MISP/misp-modules/releases/tag/v2.4.195)
