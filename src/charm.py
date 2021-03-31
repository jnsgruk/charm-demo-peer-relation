#!/usr/bin/env python3
# Copyright 2021 Canonical
# See LICENSE file for licensing details.

import logging

from ops.charm import (
    CharmBase,
    LeaderElectedEvent,
    PebbleReadyEvent,
    RelationChangedEvent,
    RelationDepartedEvent,
    RelationJoinedEvent,
)
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class PeerRelationDemoCharm(CharmBase):
    """A simple charm with a placeholder workload used to demonstrate
    how peer relations are formed, and how the relation data can be
    accessed and manipulated
    """

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.demo_pebble_ready, self._on_demo_pebble_ready)

        # Handle the case where Juju elects a new application leader
        self.framework.observe(self.on.leader_elected, self._on_leader_elected)
        # Handle the various relation events
        self.framework.observe(self.on.replicas_relation_joined, self._on_replicas_relation_joined)
        self.framework.observe(self.on.replicas_relation_departed, self._on_replicas_relation_departed)
        self.framework.observe(self.on.replicas_relation_changed, self._on_replicas_relation_changed)

        self._stored.set_default(leader_ip="")

    def _on_leader_elected(self, event: LeaderElectedEvent) -> None:
        """Handle the leader-elected event"""
        logging.debug("Leader %s setting some data!", self.unit.name)
        # Get the peer relation object
        peer_relation = self.model.get_relation("replicas")
        # Get the bind address from the juju model
        # Convert to string as relation data must always be a string
        ip = str(self.model.get_binding(peer_relation).network.bind_address)
        # Update some data to trigger a replicas_relation_changed event
        peer_relation.data[self.app].update({"leader-ip": ip})

    def _on_replicas_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Handle relation-joined event for the replicas relation"""
        logger.debug("Hello from %s to %s", self.unit.name, event.unit.name)

        # Check if we're the leader
        if self.unit.is_leader():
            # Get the bind address from the juju model
            ip = str(self.model.get_binding(event.relation).network.bind_address)
            logging.debug("Leader %s setting some data!", self.unit.name)
            event.relation.data[self.app].update({"leader-ip": ip})

        # Update our unit data bucket in the relation
        event.relation.data[self.unit].update({"unit-data": self.unit.name})

    def _on_replicas_relation_departed(self, event: RelationDepartedEvent) -> None:
        """Handle relation-departed event for the replicas relation"""
        logger.debug("Goodbye from %s to %s", self.unit.name, event.unit.name)

    def _on_replicas_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handle relation-changed event for the replicas relation"""
        logging.debug("Unit %s can see the following data: %s", self.unit.name, event.relation.data.keys())
        # Fetch an item from the application data bucket
        leader_ip_value = event.relation.data[self.app].get("leader-ip")
        # Store the latest copy locally in our state store
        if leader_ip_value and leader_ip_value != self._stored.leader_ip:
            self._stored.leader_ip = leader_ip_value

    def _on_demo_pebble_ready(self, event: PebbleReadyEvent) -> None:
        """Handle the demo-pebble-ready event"""
        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(PeerRelationDemoCharm)
