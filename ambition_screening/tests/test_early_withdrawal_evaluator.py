from django.test import TestCase, tag
from edc_reportable.units import IU_LITER, TEN_X_9_PER_LITER

from ..early_withdrawal_evaluator import EarlyWithdrawalEvaluator
from ..early_withdrawal_evaluator import alt_ref, neutrophil_ref, platlets_ref


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

    def test_value_refs(self):
        # alt > 200 not eligible
        self.assertTrue(alt_ref.in_bounds(199, units=IU_LITER))
        self.assertTrue(alt_ref.in_bounds(200, units=IU_LITER))
        self.assertFalse(alt_ref.in_bounds(201, units=IU_LITER))
        self.assertFalse(alt_ref.in_bounds(202, units=IU_LITER))
        print(alt_ref.description())

        # neutrophil < 0.5 not eligible
        self.assertFalse(neutrophil_ref.in_bounds(
            0.3, units=TEN_X_9_PER_LITER))
        self.assertFalse(neutrophil_ref.in_bounds(
            0.4, units=TEN_X_9_PER_LITER))
        self.assertTrue(neutrophil_ref.in_bounds(0.5, units=TEN_X_9_PER_LITER))
        self.assertTrue(neutrophil_ref.in_bounds(0.6, units=TEN_X_9_PER_LITER))
        print(neutrophil_ref.description())

        # platlets < 50 not eligible
        self.assertFalse(platlets_ref.in_bounds(48, units=TEN_X_9_PER_LITER))
        self.assertFalse(platlets_ref.in_bounds(49, units=TEN_X_9_PER_LITER))
        self.assertTrue(platlets_ref.in_bounds(50, units=TEN_X_9_PER_LITER))
        self.assertTrue(platlets_ref.in_bounds(51, units=TEN_X_9_PER_LITER))
        print(platlets_ref.description())
