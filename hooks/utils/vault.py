# Copyright 2022 MobiledgeX, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import requests

vault_addr = os.environ["VAULT_ADDR"]
vault_role_id = os.environ["VAULT_ROLE_ID"]
vault_secret_id = os.environ["VAULT_SECRET_ID"]

def vault_login():
    r = requests.post(f"{vault_addr}/v1/auth/approle/login",
                      json={"role_id": vault_role_id,
                            "secret_id": vault_secret_id})
    r.raise_for_status()
    return r.json()["auth"]["client_token"]

def vault_cert_domain(domainlist):
    if isinstance(domainlist, list):
        d = ",".join(sorted(set(domainlist)))
    else:
        d = domainlist
    return d.replace("*", "_")

def vault_get_cert(token, domainlist):
    domain = vault_cert_domain(domainlist)

    logging.debug(f"Fetching cert for domain(s): {domain}")
    url = f"{vault_addr}/v1/certs/cert/{domain}"
    r = requests.get(url, headers={"X-Vault-Token": token})
    if r.status_code != requests.codes.ok:
        raise Exception(f"{url}: {r.status_code} {r.text}")

    return r.json()["data"]
