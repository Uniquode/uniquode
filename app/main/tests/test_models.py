# -*- coding: utf-8 -*-

from main.components import Status, StatusModel


def test_status():
    assert Status.value_of(0) == Status.NOTPUBLISHED
    assert Status.value_of(1) == Status.PENDING
    assert Status.value_of(2) == Status.SCHEDULED
    assert Status.value_of(3) is None
    assert Status.value_of(9) == Status.PUBLISHED


def test_status_model():
    sm = StatusModel()
    assert sm.status == Status.NOTPUBLISHED
    assert sm.status.label == 'Not Published'
    sm.set_status(Status.PENDING, save=False)
    assert sm.status == Status.PENDING
    assert sm.status.label == 'Pending Approval'
