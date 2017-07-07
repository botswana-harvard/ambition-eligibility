from django.test import TestCase, tag

from edc_sync.tests import SyncTestHelper


class TestNaturalKey(TestCase):

    sync_test_helper = SyncTestHelper()

    @tag('natural_key')
    def test_natural_key_attrs(self):
        self.sync_test_helper.sync_test_natural_key_attr(
            'ambition_screening')

    @tag('natural_key')
    def test_get_by_natural_key_attr(self):
        self.sync_test_helper.sync_test_get_by_natural_key_attr(
            'ambition_screening')
