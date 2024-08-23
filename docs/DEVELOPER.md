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

**Warning 2**: You can comment `the crowdsec-ip-context-definition.json` if you want to use the definition coming from 
the [MISP Objects repository](https://github.com/MISP/misp-objects/blob/main/objects/crowdsec-ip-context/definition.json).
If you need to modify the definition during the development, you can uncomment it and modify the`cs-misp-module/dev/crowdsec-ip-context-definition.json` file.

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

Once running, you can browse to your MISP instance at `http://127.0.0.1:80` and login with the default credentials that you can find in the `.env` file.


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

For the rest of the process, we will use the release version `vX.Y.Z` as an example.

#### Retrieve zip for release

At the end of the Create Release action run, you can download a zip containing the relevant files.  

#### Create a branch for the Pull Request

If your release `vX.Y.Z` has been published on `YYYY-MM-DD`, you can create a `feat/release-YYYYMMDD` branch:

```shell
cd misp-modules
git checkout amin
git checkout -b feat/release-YYYYMMDD
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
      - ../cs-misp-module/src/misp_modules/modules/expansion/crowdsec.py:/usr/local/lib/python3.12/site-packages/misp_modules/modules/expansion/crowdsec.py

```

to 

```
services:
  misp-modules:
    volumes:
      - ../misp-modules/misp_modules/modules/expansion/crowdsec.py:/usr/local/lib/python3.12/site-packages/misp_modules/modules/expansion/crowdsec.py

```

**Beware**: The python version that is hard-coded in the `docker-compose.override.yml` may change: it should be same version that is used by the misp-modules container.


#### Open a Pull request

Push your modification 

```shell
git push origin feat/release-YYYYMMDD
```

Now you can use the `feat/release-YYYYMMDD` branch to open a pull request in the MISP modules repository.
For the pull request description, you could use the release version description that you wrote in the `CHANGELOG.md` file.


### During the pull request review

If there are modifications to do, we use the `feat/pr-<pr-number>-ongoing` branch to do them: 

```shell
cd cs-misp-module
git checkout main
git checkout -b feat/pr-<pr-number>-ongoing
```

We have to update `feat/release-YYYYMMDD` and `feat/pr-<pr-number>-ongoing` branches simultaneously.

If modifications are related to the public API of the module (defined at the top of `CHANGELOG.md`), a new release (patch, minor or major depending on the changes) 
should be created. The release zip archive will be used to update once again the `feat/release-YYYYMMDD` in `misp-modules` fork, updating automatically the current pull request.

If modifications are not related to the public API, the `feat/release-YYYYMMDD` and `feat/pr-<pr-number>-ongoing` branches should be updated directly.


### Once pull request is merged

Pull Request should have been merged without any modification related to the public API of the module (defined at the top of `CHANGELOG.md`).

Thus, it should be unnecessary to create a new release.

To backport remaining modifications (test files, documentation, etc.) to the `main` branch, we can merge the `feat/pr-<pr-number>-ongoing` branch into `main`:

```shell
cd cs-misp-module
git checkout main
git merge feat/pr-<pr-number>-ongoing
git push origin main
```










 
