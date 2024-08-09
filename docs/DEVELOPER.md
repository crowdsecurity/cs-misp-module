![CrowdSec Logo](images/logo_crowdsec.png)
# MISP CrowdSec module

## Developer guide

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Local installation](#local-installation)
  - [Prepare local environment](#prepare-local-environment)
  - [Start Docker environment](#start-docker-environment)
  - [Stop Docker environment](#stop-docker-environment)
- [Manual testing in UI](#manual-testing-in-ui)
- [Update documentation table of contents](#update-documentation-table-of-contents)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Local installation

### Prepare local environment

The final structure of the project will look like below.

```markdown
crowdsec-misp (choose the name you want for this folder)
│       
│
└───misp-modules (do not change this folder name; Only needed for MISP Pull Request process)
│   │
│   │ (Clone of https://github.com/crowdsecurity/misp-modules)
│
└───misp-docker (do not change this folder name;)
│   │
│   │ (Clone of https://github.com/misp/misp-docker)
│
└───cs-misp-module (do not change this folder name)
    │   
    │ (Clone of this repo)

```

- Create an empty folder that will contain all necessary sources:
```bash
mkdir crowdsec-misp && cd crowdsec-misp
```

- Clone the fork of misp-modules repository:

```bash
git clone git@github.com:crowdsecurity/misp-modules.git
```

- Clone this repository:

``` bash
git clone git@github.com:crowdsecurity/cs-misp-modules.git
```

- Clone the MISP docker repository:

``` bash
git clone git@github.com:misp/misp-docker.git
```

### Start Docker environment

Before running the docker environment, we need to create a volume so that our local sources are mounted in the misp-modules container.

**Warning**: The python version that is hard-coded in the `docker-compose.override.yml` may change: it should be same version that is used by the misp-modules container.
Please look the `python_version` value at the end of the `misp-modules/Pipfile` file.

```bash
cp cs-misp-module/dev/docker-compose.override.yml misp-docker/
```

We also need to create a `env` file:

```bash
cp misp-docer/template.env misp-docker/.env
```

Then, start the docker environment:

```bash
cd misp-docker && docker compose up -d --build
```

Once running, you can browse to your MISP instance at `http://localhost:80` and login with the default credentials that you can find in the `.env` file.


### Stop Docker environment

To stop all containers: 

```bash
docker compose down
```

To stop all containers and remove all data (if you want to come back to a fresh TheHive/Cortex installation): 

```bash
docker compose down -v
```

## Manual testing in UI

When you have the docker environment running, you can test the module in the MISP UI.

After each modification in the module code, you need to restart the misp-modules container to apply the changes:

```bash
docker compose restart misp-modules
```

## Code formatting

The code is formatted using `black`, `isort` and `flake8`. You can run the following command to format the code:

```bash
python -m pip install --upgrade pip
pip install -r dev/requirements.txt
cd crowdsec-misp
black  -v ./cs-misp-module/src/misp_modules/modules/expansion/crowdsec.py
isort --profile black  -v ./cs-misp-module
cd cs-misp-module
flake8 ./src/misp_modules/modules/expansion/crowdsec.py
```

## Unit tests

First, prepare your virtual environment:

```bash
python -m pip install --upgrade pip
python -m pip install -r tests/requirements.txt
```

Then, run tests: 

```bash
python -m pytest -v
```

## Update documentation table of contents

To update the table of contents in the documentation, you can use [the `doctoc` tool](https://github.com/thlorenz/doctoc).

First, install it:

```bash
npm install -g doctoc
```

Then, run it in the documentation folder:

```bash
doctoc docs/* --maxlevel 3
```






 
