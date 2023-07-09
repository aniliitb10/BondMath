from unittest import TestCase
from chapter1.interest_rate import InterestRate
from chapter1.enums import QuotationBasis, DayCountConvention


class TestInterestRate(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestInterestRate, self).__init__(*args, **kwargs)
        self.pr = 5  # decimal precision

    def test_to_aor(self):
        dr = InterestRate.create(rate=0.0380, periodicity=2, quotation_basis=QuotationBasis.DiscountRate,
                                 day_count_convention=DayCountConvention.Actual360)
        aor = dr.to_aor()
        self.assertAlmostEqual(0.03874, aor.rate, places=self.pr)

        # testing other attributes
        self.assertEqual(dr.quotation_basis, QuotationBasis.DiscountRate)
        self.assertEqual(aor.quotation_basis, QuotationBasis.AddOnRate)

        self.assertEqual(dr.periodicity, aor.periodicity)
        self.assertEqual(dr.day_count_convention, aor.day_count_convention)

    def test_to_periodicity(self):
        old_rate = InterestRate.create(rate=0.0525, periodicity=12, quotation_basis=QuotationBasis.AddOnRate,
                                       day_count_convention=DayCountConvention.Actual360)
        new_rate = old_rate.to_periodicity(4)
        self.assertAlmostEqual(0.055273, new_rate, places=self.pr)
        self.assertEqual(old_rate.periodicity, 12)
        self.assertEqual(new_rate.periodicity, 4)

        self.assertEqual(old_rate.day_count_convention, new_rate.day_count_convention)
        self.assertEqual(old_rate.quotation_basis, new_rate.quotation_basis)

    def test_dr_to_aor(self):
        self.assertAlmostEqual(0.03874, InterestRate.dr_to_aor(dr=0.0380, days=180, days_in_year=360), places=self.pr)
        self.assertAlmostEqual(0.09534, InterestRate.dr_to_aor(dr=0.09387, days=59, days_in_year=360), places=self.pr)

    def test_change_periodicity(self):
        self.assertAlmostEqual(0.05273, InterestRate.change_periodicity(rate=0.0525, old=12, new=4), places=self.pr)
        self.assertAlmostEqual(0.05378, InterestRate.change_periodicity(rate=0.0525, old=12, new=1), places=self.pr)

        self.assertAlmostEqual(0.05265, InterestRate.change_periodicity(rate=0.0530, old=2, new=4), places=self.pr)
        self.assertAlmostEqual(0.05370, InterestRate.change_periodicity(rate=0.0530, old=2, new=1), places=self.pr)
