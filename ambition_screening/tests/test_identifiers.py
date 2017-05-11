from django.test.testcases import TestCase

from model_mommy import mommy

from ..identifier import ScreeningIdentifier
from ambition_screening.models.identifier_history import IdentifierHistory


class TestIdentifiers(TestCase):

    def test_identifier(self):
        identifier = ScreeningIdentifier()
        self.assertTrue(identifier.identifier)
        self.assertTrue(identifier.identifier.startswith('S'))

    def test_identifier_history(self):
        identifier = ScreeningIdentifier()
        try:
            IdentifierHistory.objects.get(identifier=identifier.identifier)
        except IdentifierHistory.DoesNotExist:
            self.fail('IdentifierHistory.DoesNotExist unexpectedly raised')

    def test_model_allocates_identifier(self):
        obj = mommy.make_recipe('ambition_screening.subjectscreening')
        self.assertIsNotNone(obj.screening_identifier)
        self.assertTrue(obj.screening_identifier.startswith('S'))
