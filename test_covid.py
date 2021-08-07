import unittest
import pandas as pd
import pandas.testing as pd_testing
from pandas.util.testing import assert_frame_equal

from test_covid_compare import load_df #load custom load df function

class TestCovidApi(unittest.TestCase):
    # class initiation
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
         self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_covid(self):
        # simulate a correct df
        actual = pd.DataFrame({
        'num_confirmed' : [54380,481357],
        'num_deaths' : [1008,6136],
        'num_recovered' : [51143,0]
        })

        # df to compare vs actual
        self.assertEqual(load_df('output/covid_data.xls'), actual)