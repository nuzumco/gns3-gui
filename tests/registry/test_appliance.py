#!/usr/bin/env python
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pytest
import json

from gns3.registry.appliance import Appliance, ApplianceError
from gns3.registry.registry import Registry


@pytest.fixture
def registry(images_dir):
    return Registry(images_dir)


@pytest.fixture
def microcore_appliance(registry):
    """
    An instance of microcore Appliance object
    """
    return Appliance(registry, "tests/registry/appliances/microcore-linux.json")


def test_check_config(tmpdir, registry):

    test_path = str(tmpdir / "test.json")

    with open(test_path, "w+", encoding="utf-8") as f:
        f.write("")

    with pytest.raises(ApplianceError):
        Appliance(registry, "jkhj")

    with pytest.raises(ApplianceError):
        Appliance(registry, test_path)

    with open(test_path, "w+", encoding="utf-8") as f:
        f.write("{}")

    with pytest.raises(ApplianceError):
        Appliance(registry, test_path)

    with open(test_path, "w+", encoding="utf-8") as f:
        f.write('{"registry_version": 2}')

    with pytest.raises(ApplianceError):
        Appliance(registry, test_path)

    Appliance(registry, "tests/registry/appliances/microcore-linux.json")


def test_resolve_version(tmpdir):

    with open("tests/registry/appliances/microcore-linux.json", encoding="utf-8") as f:
        config = json.load(f)

    new_config = Appliance(registry, "tests/registry/appliances/microcore-linux.json")
    assert new_config["versions"][0]["images"] == {"hda_disk_image": config["images"][0]}


def test_search_images_for_version(linux_microcore_img, microcore_appliance):

    detected = microcore_appliance.search_images_for_version("3.4.1")
    assert detected["name"] == "Micro Core Linux 3.4.1"
    assert detected["images"][0]["type"] == "hda_disk_image"
    assert detected["images"][0]["path"] == linux_microcore_img


def test_search_images_for_version_unknow_version(microcore_appliance):

    with pytest.raises(ApplianceError):
        detected = microcore_appliance.search_images_for_version("42")


def test_search_images_for_version_missing_file(microcore_appliance):

    with pytest.raises(ApplianceError):
        detected = microcore_appliance.search_images_for_version("4.0.2")


def test_is_version_installable(linux_microcore_img, microcore_appliance):

    assert microcore_appliance.is_version_installable("3.4.1")
    assert not microcore_appliance.is_version_installable("4.0.2")



