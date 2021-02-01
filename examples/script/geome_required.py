"""
Script to determine list of columns that have been required in at least one project.

Sources:
  network config:
    https://api.geome-db.org/v1/network/1/config
  list of public projects:
    https://api.geome-db.org/v1/projects/?includePublic=true&admin=false
"""

import sys
import logging
import requests
import json
import csv
import click
import common


def getLogger():
    return logging.getLogger("geome-req")


RULE_REQUIRED = "RequiredValue"
ERROR_LEVEL = "ERROR"
GEOME_API = "https://api.geome-db.org/v1"
TIMEOUT = 30 #seconds


def processGeomeConfig(doc, proj_id=0, title="network"):
    res = []
    for entity in doc.get("entities", []):
        alias = entity.get("conceptAlias")
        cols = set()
        for r in entity.get("rules"):
            if r.get("name") == RULE_REQUIRED and r.get("level") == ERROR_LEVEL:
                cols.update(r.get("columns"))
        for c in cols:
            row = (alias, c, proj_id, title)
            res.append(row)
    return res


def getProjectConfig(project_id):
    url = f"{GEOME_API}/projects/{project_id}/config"
    response = requests.get(url, timeout=TIMEOUT)
    cfgdoc = response.json()
    return cfgdoc


def processProjects():
    L = logging.getLogger("loader")
    url = f"{GEOME_API}/projects/"
    params = {"includePublic": "true", "admin": "false"}
    response = requests.get(url, params=params, timeout=TIMEOUT)
    projects = response.json()
    res = []
    for project in projects:
        proj_id = project.get("projectId")
        title = project.get("projectTitle")
        L.info(f"Loading: {proj_id} - {title}")
        doc = getProjectConfig(proj_id)
        res += processGeomeConfig(doc, proj_id=proj_id, title=title)
    return res


@click.command()
@click.option(
    "-v",
    "--verbosity",
    default="INFO",
    help="Specify logging level",
    show_default=True,
)
def main(verbosity):
    common.setupLogging(verbosity)
    response = requests.get(f"{GEOME_API}/network/1/config", timeout=TIMEOUT)
    network_config = response.json()
    res = processGeomeConfig(network_config)
    res += processProjects()
    output = csv.writer(sys.stdout, dialect="excel")
    header = ["record_alias", "column_name", "project_id", "project_title"]
    output.writerow(header)
    for row in res:
        output.writerow(row)


if __name__ == "__main__":
    main()
