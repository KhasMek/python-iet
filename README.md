# INFOSEC ENGAGEMENT TOOLS (IET)

IET is a python library to assist in organizing and performing penetration tests. This includes:

- Bootstrapping working directories for various types of engagements in order to have consistency in project layouts.
- IP calculation and lookup tools.
- Wordlist generator for password spraying.
- Basic tools for dealing with cookies.
- More to come (unless I continue being the laziest panda)

---

## Table of Contents

- [Installation](#installation)
  - [pip](#pip)
  - [Local Development](#local-development)
- [Included Tools](#included-tools)
  - [Bootstrap](#bootstrap)
  - [Cookie Monster](#cookie-monster)
  - [IP Lookup](#ip-lookup)
  - [Wordlist Generator](#wordlist-generator)
- [TODO](#todo)

---

## Installation

Requirements:

- python3
- pip
- oh-my-zsh [autoenv](https://github.com/zpm-zsh/autoenv) plugin (for bootstrapping functionality)

### pip

To install IET via python pip execute the below command:

```shell
pip install git+https://github.com/KhasMek/python-iet
```

### Local Development

To clone the IET repo and install for local development perform the below commands:

```shell
git clone https://github.com/KhasMek/python-iet
cd python-iet
pip install -e .
```


## Included Tools

### Bootstrap

**Command:** `iet-bootstrap`

A tool to bootstrap a projects working directory, including project directories, logging, aliases and global variables set to the specific project. All of this is modular and can be customized by the user in the config. This command curretly requires [autoenv](https://github.com/zpm-zsh/autoenv) to function. However, this will soon be ported over to [direnv](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/direnv).

#### Usage

```
usage: iet-bootstrap [-h] [-c CONFIG] [-b BASENAME] [-pt PROJECT_TYPE] [-pn PROJECT_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Location of config file
  -b BASENAME, --basename BASENAME
                        directory to bootstrap
  -pt PROJECT_TYPE, --project_type PROJECT_TYPE
                        project directory name
  -pn PROJECT_NAME, --project_name PROJECT_NAME
                        project directory name
```

#### Example

```shell
iet-bootstrap -pt mobile-app -pn test-application
```

Will create the folder `test-application` at the current directory with mobile application focused tooling.

---

### Cookie Monster

**Command:** `iet-cookie-monster`

A very basic tool to grab cookies from a provided website.

#### Usage

```
usage: iet-cookie-monster [-h] [-c CONFIG] [-nv] [-o OUTFILE] target

positional arguments:
  target                Target domain to get cookies of

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Location of config file
  -nv, --no-verify      Disable Certificate verification
  -o OUTFILE, --outfile OUTFILE
                        Write cookies to file
```

---

### IP Lookup

**Command:** `iet-ip-lookup`

Tools to lookup different information about cidrs, IP ranges and single IP addresses.

#### Usage

```
usage: iet-ip-lookup [-h] [-c CONFIG] [-n NETBLOCK] {summary,range,isitin} target

positional arguments:
  {summary,range,isitin}
                        Type of query to perform. (default: summary)
  target                Target ip address, range or subnet

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Location of config file
  -n NETBLOCK, --netblock NETBLOCK
                        Netblock to look up for isitin function
```

---

### Wordlist Generator

**Command:** `iet-wordlist-gen`

Generate simple wordlists that can then be used in password spraying or other brute attacks. The options can be completely customized in the config.

#### Usage

```
usage: iet-wordlist-gen [-h] [-b] [-c CONFIG] [-cp] [-i ITERS] [-o OUTFILE] [-r REGEX] [-s]
                          [-w]

optional arguments:
  -h, --help            show this help message and exit
  -b, --basic           Generate basic (seasonal) wordlist
  -c CONFIG, --config CONFIG
                        Location of config file
  -cp, --copy           Copy to clipboard
  -i ITERS, --iters ITERS
                        Length of wordlist to generate
  -o OUTFILE, --outfile OUTFILE
                        Name of the worldlist file
  -r REGEX, --regex REGEX
                        Path to the file or directory to parse
  -s, --stdout          Print list to terminal
  -w, --write           Write the wordlist to file
```

---

## TODO

- [ ] add env variables to .in/.out for created directories (wip, etc.) for ez aliasing.
- [ ] aliases for semgrep, jwt_tool
- [ ] Add custom project for mobile apps - include the below aliases
        - `jadx -d android --deobf ../app-packages/$$APK_NAME$$
        - semgrep (different configs)
        - `mobsfscan -o ../../wip/mobsfscan-TYPE.txt .` (use pwd/basename or something to determine if android or iOS)
        -
- [ ] Add support for bootstrapping multiple project types (e.g. default,mobapp,int) and create all dirs/files while merging in/out files (if required)
