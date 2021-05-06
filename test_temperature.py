from unittest import TestCase
from temperature import Temperature


class TestTemperature(TestCase):
    # one stn id, no duplicate temps or duplicate lowest temps
    t0 = Temperature('test_data.csv')

    # multiple stn id, multiple duplicate temps and duplicate lowest temps
    t1 = Temperature('test_data_same_lowest_temp.csv')

    # 150+ rows, multiple_ids, duplicate temps
    t2 = Temperature('test_data_multiple_ids.csv')

    # empty csv
    t_empty = Temperature('test_data_empty.csv')

    def test_get_lowest_temp(self):
        # one stn id, no duplicate temps or duplicate lowest temps
        self.assertEqual(self.t0.get_lowest_temp(), ("68", "2000.542"))

        # multiple stn id, multiple duplicate temps and duplicate lowest temps
        self.assertEqual(self.t1.get_lowest_temp(), ("68", "2000.542"))

        # empty csv
        self.assertEqual(self.t_empty.get_lowest_temp(), (None, None))

        # 150+ rows, multiple_ids, duplicate temps
        self.assertEqual(self.t2.get_lowest_temp(), ('115', '2015.645'))

    def test_get_most_fluctuation(self):
        # one stn id
        self.assertEqual(self.t0.get_most_fluctuation(), "68")

        # multiple stn id, multiple duplicate temps and duplicate lowest temps
        self.assertEqual(self.t1.get_most_fluctuation(), "69")

        # 150+ rows, multiple_ids, duplicate temps
        self.assertEqual(self.t1.get_most_fluctuation(), "69")

        # empty csv
        self.assertEqual(self.t_empty.get_most_fluctuation(), None)

    def test_get_most_fluctuation_range(self):
        # Normal range
        self.assertEqual(self.t0.get_most_fluctuation_range('2000.375', '2000.958'), "68")
        self.assertEqual(self.t1.get_most_fluctuation_range('2000.375', '2001.345'), "69")
        self.assertEqual(self.t2.get_most_fluctuation_range('2000.375', '2001.345'), "69")
        self.assertEqual(self.t_empty.get_most_fluctuation_range('2000.375', '2001.345'), None)

        # only one item within date range
        self.assertEqual(self.t0.get_most_fluctuation_range('2000.888', '2000.999'), "68")
        self.assertEqual(self.t1.get_most_fluctuation_range('2000.888', '2000.999'), "68")
        self.assertEqual(self.t2.get_most_fluctuation_range('2000.888', '2000.999'), "68")
        self.assertEqual(self.t_empty.get_most_fluctuation_range('2000.888', '2000.999'), None)

        # no items within date range
        self.assertEqual(self.t0.get_most_fluctuation_range('2000.111', '2000.112'), None)
        self.assertEqual(self.t1.get_most_fluctuation_range('2000.111', '2000.112'), None)
        self.assertEqual(self.t2.get_most_fluctuation_range('2000.111', '2000.112'), None)
        self.assertEqual(self.t_empty.get_most_fluctuation_range('2000.111', '2000.112'), None)

    def test_calculate_fluctuation(self):
        # calculate fluctuation for data with on stn id
        for stn_id, data in self.t0.temperatures.items():
            fluctuation = self.t0.calculate_fluctuation(data)
            self.assertEqual(int(fluctuation), 22)
