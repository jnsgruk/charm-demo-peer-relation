# Copyright 2021 Canonical
# See LICENSE file for licensing details.

import unittest

from charm import PeerRelationDemoCharm
from ops.testing import Harness

# from unittest.mock import Mock


class TestCharm(unittest.TestCase):
    def test_config_changed(self):
        harness = Harness(PeerRelationDemoCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        self.assertEqual(list(harness.charm._stored.things), [])
        harness.update_config({"thing": "foo"})
        self.assertEqual(list(harness.charm._stored.things), ["foo"])
