# Add main directory to search path
import sys
sys.path.append('../../')

import os, time, subprocess, unittest, math
from lib.rrdtool import lib_rrdtool

class TestLibRrdtool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.rrd = lib_rrdtool.RRDLibrary()

    def test_create_rrd(self):
        self.rrd.create_rrd('test_create_table.rrd', 'nothing', 1, 1, 0, 10)
        self.assertTrue(os.path.isfile(self.rrd.DATA_FOLDER + \
                                       'test_create_table.rrd'))
        if os.path.isfile(self.rrd.DATA_FOLDER + 'test_create_table.rrd'):
            os.remove(self.rrd.DATA_FOLDER + 'test_create_table.rrd')

    def test_update_rrd(self):
        self.rrd.create_rrd('test_update_table.rrd', 'test_values', 1, 1, 0, 10)
        time.sleep(1)
        self.rrd.update_rrd('test_update_table.rrd', 3)
        last_val = self.rrd.get_time_value_list('test_update_table.rrd',
                                                   1)[0][1]
        self.assertEqual(last_val, 3)
        if os.path.isfile(self.rrd.DATA_FOLDER + 'test_update_table.rrd'):
            os.remove(self.rrd.DATA_FOLDER + 'test_update_table.rrd')

    #TODO: Check to see if this function can be removed
    # def test_get_graph_path(self):
    #     table_name = 'test_get_graph_path_table'
    #     start_time = int(time.time())
    #     self.rrd.create_rrd(table_name, 'test_values', 1, 10, -10, 10, 1)
    #     for i in range(-3, 3):
    #         time.sleep(1)
    #         self.rrd.update_rrd(table_name, i)
    #     end_time = int(time.time())
    #     graph_image_path = self.rrd.get_graph_path(table_name, 'test_values',
    #                                              'fake units', start_time,
    #                                              end_time)
    #     self.assertTrue(os.path.isfile(self.rrd.DATA_FOLDER + table_name + \
    #         '.png'))
    #     subprocess.Popen(["display", graph_image_path])
    #     if os.path.isfile(self.rrd.DATA_FOLDER + table_name + '.rrd'):
    #         os.remove(self.rrd.DATA_FOLDER + table_name + '.rrd')         

    def test_get_time_value_list(self):
        table_name = 'test_get_time_value_list_table.rrd'
        sample_rate = 1
        hours = 1
        start_val = -10
        end_val = 10
        num_vals = end_val - start_val
        self.assertLess(start_val, end_val)
        list_to_compare = []
        self.rrd.create_rrd(table_name, 'test_values', sample_rate, hours,
                               start_val, end_val, 2*sample_rate)
        time.sleep(sample_rate)
        for i in range(start_val, end_val):
            self.rrd.update_rrd(table_name, i)
            time_to_compare = self.rrd.format_time(time.time(), sample_rate)
            list_to_compare.append((time_to_compare, i))
            time.sleep(sample_rate)
        time_vals = self.rrd.get_time_value_list(table_name, num_vals)
        self.assertEqual(time_vals, list_to_compare)
        single_time_val = self.rrd.get_time_value_list(table_name, 1)
        self.assertEqual(single_time_val[0][1], end_val - 1)
        if os.path.isfile(self.rrd.DATA_FOLDER + table_name):
            os.remove(self.rrd.DATA_FOLDER + table_name)

    # TODO: Move to client unit test
    # def test_calibrate_value(self):
    #     self.assertEqual(self.rrd.calibrate_value(5), 5)
    #     self.assertEqual(self.rrd.calibrate_value(5, 3, 8, 10, 56, 100),
    #                                                  140.2)

    def test_format_time(self):
        self.assertEqual(self.rrd.format_time(79, 4), 80)
        self.assertEqual(self.rrd.format_time(80.9999, 9), 81)
        self.assertEqual(self.rrd.format_time(81.0000001, 9), 90)
        self.assertEqual(self.rrd.format_time(72.5, 1), 73)
        self.assertEqual(self.rrd.format_time(25, 25), 25)

if __name__ == '__main__':
    unittest.main()