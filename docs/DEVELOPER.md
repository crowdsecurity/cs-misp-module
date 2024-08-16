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
- [Code formatting](#code-formatting)
- [Unit tests](#unit-tests)
- [Update documentation table of contents](#update-documentation-table-of-contents)
- [MISP Pull Request](#misp-pull-request)
  - [Sync fork with upstream](#sync-fork-with-upstream)
  - [Update fork sources](#update-fork-sources)
  - [During the pull request review](#during-the-pull-request-review)
  - [Once pull request is merged](#once-pull-request-is-merged)

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

To stop all containers and remove all data (if you want to come back to a fresh MISP installation): 

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


## MISP Pull Request

To make an update publicly available, we need to submit a pull request to the [MISP modules repository](https://github.com/MISP/misp-modules), 
and to submit a pull request, we use the [CrowdSec fork](https://github.com/crowdsecurity/misp-modules).

### Sync fork with upstream

Before modifying the code of our fork, we need to sync it from the upstream repo. There are many way to do it. Below is what you can do locally.

Using your local connectors folder defined [above](#prepare-local-environment), you should define two Git remote: origin (the fork) and upstream (the MISP modules repo).
You can check that with the following command: 

```shell
cd misp-modules
git remote -v
```

You should see the following result:

```
origin	git@github.com:crowdsecurity/misp-modules.git (fetch)
origin	git@github.com:crowdsecurity/misp-modules.git (push)
upstream	git@github.com:MISP/misp-modules.git (fetch)
upstream	git@github.com:MISP/misp-modules.git (push)
```



Once you have this, you can force update the fork develop branch :

```shell
git checkout main
git fetch upstream
git reset --hard upstream/main
git push origin main --force 
```

### Update fork sources

#### Create a release

Before creating a release, ensure to format correctly the `CHANGELOG.md` file and to update all necessary code related to the version number:
`src/misp_modules/modules/expansion/crowdsec.py`.

Then, you can use the [Create Release action](https://github.com/crowdsecurity/cs-misp-module/actions/workflows/release.yml).

#### Retrieve zip for release

At the end of the Create Release action run, you can download a zip containing the relevant files.  

#### Create a branch for the Pull Request

If your release is `vX.Y.Z`, you can create a `feat/release-X.Y.Z` branch:

```shell
cd misp-modules
git checkout amin
git checkout -b feat/release-X.Y.Z
```

#### Update sources

Before all, remove all files related to CrowdSec:

```shell
cd misp-modules
rm -rf misp_modules/modules/expansion/crowdsec.py
```

Then, unzip the `crowdsec-misp-module-X.Y.Z.zip` archive and copy files in the right folders:
- `src/misp_modules/modules/expansion/crowdsec.py` -> `misp_modules/modules/expansion/crowdsec.py`



Now, you can verify the diff.

Once all seems fine, add and commit your modifications:

```shell
git add .
git commit -m "[crowdsec] Update module (vX.Y.Z)"
```

#### Test locally before pull request 

You can test with the docker local stack by modifying the `misp-docker/docker-compose.override.yml` file:
Change

```
services:
  misp-modules:
    volumes:
      - ../cs-misp-module/src/misp_modules/modules/expansion/crowdsec.py:/usr/local/lib/python?.??/site-packages/misp_modules/modules/expansion/crowdsec.py

```

to 

```
services:
  misp-modules:
    volumes:
      - ../misp-modules/misp_modules/modules/expansion/crowdsec.py:/usr/local/lib/python?.??/site-packages/misp_modules/modules/expansion/crowdsec.py

```


#### Open a Pull request

Push your modification 

```shell
git push origin feat/release-X.Y.Z
```

Now you can use the `feat/release-X.Y.Z` branch to open a pull request in the MISP modules repository.
For the pull request description, you could use the release version description that you wrote in the `CHANGELOG.md` file.



### During the pull request review

As long as the pull request is in review state, we should not create a new release. 
If there are modifications to do, we can do it directly on the `feat/release-X.Y.Z`. 
All changes made to pass the pull request review must be back ported to a `feat/pr-review-X.Y.Z` branch created in this repository:

```shell
cd cs-misp-module
git checkout main
git checkout -b feat/pr-review-X.Y.Z
```

### Once pull request is merged

If pull request has been merged without any modification, there is nothing more to do.

If there were modifications, we need to update the sources anc create a patch release.

#### Sync fork with upstream

First, sync the connector fork like we did [here](#sync-fork-with-upstream). 

#### Retrieve last version

After this, you should have the last version of the CrowdSec module in `misp_modules/modules/expansion/crowdsec.py`.

You need to retrieve it and commit the differences.

```shell
cd cs-misp-module
git checkout feat/pr-review-X.Y.Z
```

Delete `src/misp_modules/modules/expansion/crowdsec.py`.

Copy all files from the modules fork: 

```
cp -r ../misp-modules/misp_modules/modules/expansion/crowdsec.py ./src/misp_modules/modules/expansion/crowdsec.py
```

Add and commit the result. Push the `feat/pr-review-X.Y.Z` and merge it into `main` with a pull request.


#### Create a new minor release

Once the `main` branch is updated, you can create a new minor `X.Y.Z+1` release with the following CHANGELOG content:

```
## Changed

- Synchronize content with MISP modules release [A.B.C](https://github.com/MISP/misp-modules/releases/tag/A.B.C)

```



 
