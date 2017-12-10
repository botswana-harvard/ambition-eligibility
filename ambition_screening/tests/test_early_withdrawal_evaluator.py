from django.test import TestCase, tag

from ..early_withdrawal_evaluator import EarlyWithdrawalEvaluator


EarlyWithdrawalEvaluator.blood_result_model = 'ambition_screening.bloodresult'


class TestEarlyWithdrawalEvaluator(TestCase):

    @tag('7')
    def test_early_withdrawal_criteria_no(self):
        opts = dict(alt=None, neutrophil=None, platlets=None)
        obj = EarlyWithdrawalEvaluator(**opts)
        self.assertFalse(obj.eligible)

    @tag('7')
    def test_early_withdrawal_criteria_with_none(self):
        opts = dict(alt=None, neutrophil=None, platlets=None, allow_none=True)
        obj = EarlyWithdrawalEvaluator(**opts)
        self.assertTrue(obj.eligible)

    @tag('7')
    def test_early_withdrawal_criteria_ok(self):
        opts = dict(alt=200, neutrophil=0.5, platlets=50, allow_none=True)
        obj = EarlyWithdrawalEvaluator(**opts)
        self.assertTrue(obj.eligible)
