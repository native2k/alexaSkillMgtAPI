#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

class FakeAPI(object):
    def __init__(self, manifests):
        self.manifests = manifests

    def skillGet(self, id):
        return self.manifests[int(id)]['skillManifest']

    def modelGet(self, id, locale):
        return self.manifests[int(id)]



@pytest.fixture
def api(testdata):
    return FakeAPI(testdata)
