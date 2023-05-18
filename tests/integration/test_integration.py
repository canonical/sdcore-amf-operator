#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.


import logging
from pathlib import Path

import pytest
import yaml

logger = logging.getLogger(__name__)

METADATA = yaml.safe_load(Path("./metadata.yaml").read_text())
APP_NAME = METADATA["name"]
DB_CHARM_NAME = "mongodb-k8s"
NRF_CHARM_NAME = "sdcore-nrf"


@pytest.fixture(scope="module")
@pytest.mark.abort_on_fail
async def build_and_deploy(ops_test):
    """Build the charm-under-test and deploy it."""
    charm = await ops_test.build_charm(".")
    resources = {
        "amf-image": METADATA["resources"]["amf-image"]["upstream-source"],
    }
    await ops_test.model.deploy(
        charm,
        resources=resources,
        application_name=APP_NAME,
        series="jammy",
    )
    await ops_test.model.deploy(
        DB_CHARM_NAME,
        application_name=DB_CHARM_NAME,
        series="jammy",
    )
    await ops_test.model.deploy(
        NRF_CHARM_NAME,
        application_name=NRF_CHARM_NAME,
        channel="edge",
        series="jammy",
    )


@pytest.mark.abort_on_fail
async def test_relate_and_wait_for_active_status(
    ops_test,
    build_and_deploy,
):
    await ops_test.model.add_relation(relation1=APP_NAME, relation2=DB_CHARM_NAME)
    await ops_test.model.add_relation(relation1=APP_NAME, relation2=NRF_CHARM_NAME)
    await ops_test.model.wait_for_idle(
        apps=[APP_NAME],
        status="active",
        timeout=1000,
    )