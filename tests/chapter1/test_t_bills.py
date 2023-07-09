from unittest import TestCase

from chapter1.t_bills import TBills


class TestTBills(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTBills, self).__init__(*args, **kwargs)
        self.pre = 3

    def test_4w_TBills_str(self):
        t_bill = TBills(4, 1.85)
        self.assertEqual("Term: [4] weeks, Discount Rate: [1.85%], Investment Rate: [1.878%], "
                         "Price (per $100 in par value): [99.856111]", str(t_bill))

        self.assertAlmostEqual(1.878, t_bill.investment_rate_pct, places=self.pre)
        self.assertAlmostEqual(99.856111, t_bill.pv, places=self.pre)

    def test_4w_TBills(self):
        t_bill = TBills(4, 1.85)
        self.assertAlmostEqual(1.878, t_bill.investment_rate_pct, places=self.pre)
        self.assertAlmostEqual(99.856111, t_bill.pv, places=self.pre)

    def test_13w_TBills(self):
        t_bill = TBills(13, 1.9)
        self.assertAlmostEqual(1.936, t_bill.investment_rate_pct, places=self.pre)
        self.assertAlmostEqual(99.519722, t_bill.pv, places=self.pre)

    def test_26w_TBills(self):
        t_bill = TBills(26, 2.135)
        self.assertAlmostEqual(2.188, t_bill.investment_rate_pct, places=self.pre)
        self.assertAlmostEqual(98.914708, t_bill.pv, places=self.pre)

    def test_52w_TBills(self):
        t_bill = TBills(52, 2.295)
        self.assertAlmostEqual(2.368, t_bill.investment_rate_pct, places=self.pre)
        self.assertAlmostEqual(97.6795, t_bill.pv, places=self.pre)
