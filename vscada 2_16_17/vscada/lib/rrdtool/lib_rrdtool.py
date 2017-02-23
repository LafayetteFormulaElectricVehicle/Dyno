#!/usr/bin/env python3
"""Round robin database library module.

This module contains functions which can be used to create, update, retrieve,
and calibrate data from rrdtool round robin databases. It uses the updated
rrdtool Python bindings for Python 3 which were created by Christian Jurk,
which in turn use the rrdtool Python 2 bindings created by Hye-Shik Chang.
"""

import os, time, math, logging
import rrdtool

__author__ = "Adam Cornwell, Christian Jurk, and Hye-Shik Chang"
__version__ = "0.4.0"

class RRDLibrary:

    __XFF__ = 0.5
    """
    Xfiles factor used in creating a sensor. Define what part of a consolidation
    interval can be made up of *None* data without the consolidated value
    becoming None. In other words, define the ratio of *None* PDPs (primary
    data points) to the number of PDPs in the step interval being used for a command
    such as AVERAGE.
    """

    __DEFAULT_HEARTBEAT_FACTOR__ = 1
    """
    The heartbeat factor for use in creating a sensor; this multiplied by the sample
    step is used as the default heartbeat if none is entered.
    """

    # change the working directory to the location of this class
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    DATA_FOLDER = "../../data/rrd/"
    """
    The folder where the rrd database files are stored.
    """

    def __init__(self, _logger=None):
        if _logger == None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = _logger

    def create_rrd(self, filename, data_name, sample_rate, overwrite_period,
                   min_value=-65536, max_value=65536, heartbeat=None):
        """Create a round robin database file for a single data source.

        Create a database file for a single data source with the given
        parameters using LAST (last value) as the CF (consolidation function)
        for the RRA (round robin archive).

        Args:
            filename: The string filename with extension to use for the
                database.
            data_name: The string name of the data source, describes what's
                being measured.
            sample_rate: The integer number of seconds, or step, between each
                sample in the database.
            overwrite_period: The amount of time, given the sample rate, before
                values are overwritten in the rrd. Used in combination with
                sample_rate to determine the number of values which the database
                can hold.
            min_value: An optional float sample value which acts as the minimum
                value that can be entered into the database. A value less than
                this will be stored as None. By default -65536.
            max_value: An optional float sample value which acts as the maximum
                value that can be entered into the database. A value greater
                than this will be stored as None. By default 65536.
            heartbeat: An optional integer which becomes
                __DEFAULT_HEARTBEAT_FACTOR__*sample_rate if no value is entered.
                The amount of time to wait for a new data point before None is
                stored as the value. If heartbeat is greater than the
                sample_rate and no data is received in sample_rate seconds, the
                last value received is used up until heartbeat seconds passes.

        Returns:
                True, if rrd file creation was successful, False otherwise.
        """
        try:
            rrd_filename = self.DATA_FOLDER + str(filename)
            if os.path.isfile(rrd_filename):
                        old_rrd_filename = rrd_filename + '.old'
                        os.rename(rrd_filename, old_rrd_filename)
            path = os.path.dirname(rrd_filename)
            if not os.path.exists(path):
                os.makedirs(path)
            sample_rate = int(sample_rate)
            num_vals = int((3600*float(overwrite_period))/sample_rate)
            min_value = int(min_value)
            max_value = int(max_value)
            if heartbeat == None:
                heartbeat = RRDLibrary.__DEFAULT_HEARTBEAT_FACTOR__*sample_rate
            else:
                heartbeat = int(heartbeat)
            # added data_name default value since some data may not have units
            if data_name == '':
                data_name = 'default'
            data_source = 'DS:' + str(data_name) + ':GAUGE:' + \
                          str(heartbeat) + ':' + str(min_value) + ':' + \
                          str(max_value)
            round_robin_archive = 'RRA:LAST:' + str(RRDLibrary.__XFF__) \
                                  + ':1:' + str(num_vals)
            start_time = self.format_time(time.time(), sample_rate)
            rrd_ret_val = rrdtool.create(rrd_filename,
                                         '--step' , str(sample_rate),
                                         '--start', str(start_time),
                                         data_source,
                                         round_robin_archive)
            return True
        except rrdtool.ProgrammingError as e:
            self.logger.error('A user programming error occurred in create_rrd \
                              function in lib_rrdtool.')
            self.logger.error(e)
        except rrdtool.OperationalError as e1:
            self.logger.error('An operational error (such as a filesystem \
                              error) occurred in create_rrd function in \
                              lib_rrdtool.')
            self.logger.error(e1)
        except TypeError as e2:
            self.logger.error('Parameter of incorrect type used in create_rrd \
                              function in lib_rrdtool.')
            self.logger.error(e2)
        return False

    def update_rrd(self, filename, value, time_stamp=None):
        """Update the database of given string name with the given float value.

        Update the last data point of the round robin database with the given
        string filename to the given float value. Times are rounded up to the
        nearest time in seconds which is divisible by the given database's
        sampling rate.

        Args:
            filename: The string filename with extension of the database.
            value: The float value to update the database with; must be within
                the database's predefined range.
            time_stamp: An optional float which can be used to specify the time
                at which the value should be set as having been entered in the
                database. If not entered the current time is used. Whatever time
                that is used is rounded up to the nearest time in seconds which
                is divisible by the database's sampling rate.

        Returns:
            True, if rrd update was successful, False otherwise.
        """
        try:
            rrd_filename = self.DATA_FOLDER + str(filename)
            value = float(value)
            sample_rate = int(rrdtool.info(rrd_filename).get('step', '1'))
            if time_stamp == None:
                time_stamp = time.time()
            else:
                time_stamp = float(time_stamp)
            time_stamp = self.format_time(time_stamp, sample_rate)
            rrdtool.update(rrd_filename, '%d:%f' % (time_stamp, value))
            return True
        except rrdtool.ProgrammingError as e:
            self.logger.debug('A user programming error occurred in update_rrd \
                              function in lib_rrdtool.')
            self.logger.error(e)
        except rrdtool.OperationalError as e1:
            self.logger.debug('An operational error (such as a filesystem \
                              error) occurred in update_rrd function in \
                              lib_rrdtool.')
            self.logger.error(e1)
        except TypeError as e2:
            self.logger.debug('Parameter of incorrect type used in update_rrd \
                              function in lib_rrdtool.')
            self.logger.error(e2)
        return False

    # TODO: Check to see if this function can be removed
    # def get_graph_path(filename, data_name, units, start_time, end_time, slope=1,
    #                    offset=0):
    #     rrd_filename = self.DATA_FOLDER + str(filename) + '.rrd'
    #     graph_filename = str(filename) + '.png'
    #     graph_label = str(data_name)[:1].upper() + str(data_name)[1:]
    #     rrdtool.graph(self.DATA_FOLDER + graph_filename,
    #                   '--start', str(start_time),
    #                   '--end', str(end_time),
    #                   '--vertical-label', str(units),
    #                   '--imgformat', 'PNG',
    #                   '--title', str(graph_label),
    #                   '--lazy',
    #                   'DEF:data=%s:%s:LAST' % (rrd_filename, data_name),
    #                   'CDEF:calib_data=data,%s,*,%s,+' % (slope, offset),
    #                   'LINE1:calib_data#FF0000:%s' % data_name)
        
    #     return os.path.abspath(self.DATA_FOLDER + graph_filename)

    def get_time_value_list(self, filename, num_vals, sample_rate=None):
        """Return a list of time and value tuples from the given database.

        Returns the given number of values from the given rrd database in a list
        of tuples in the format [(1st_time, 1st_val), (2nd_time, 2nd_val), ...].
        If a sample rate is given, time value tuples are returned with
        sample_rate seconds between each value.

        Args:
            filename: The string filename with extension of the database.
            num_vals: The integer number of values to retrieve from the
                database; must be within the database's predefined size.
            sample_rate: An optional integer which can be used to specify the
                number of seconds between each value of the time value tuples
                being returned. If not specified the database's default sample
                rate is used.

        Returns:
            A list of tuples with each tuple containing a retrieved time and
            value, if rrd value retrieval was successful, or None otherwise.
            example: [(1st_time, 1st_val), (2nd_time, 2nd_val), ...]
        """
        try:
            rrd_filename = self.DATA_FOLDER + str(filename)
            num_vals = int(num_vals)
            if sample_rate == None:
                sample_rate = int(rrdtool.info(rrd_filename).get('step', '1'))
            else:
                sample_rate = int(sample_rate)
            end_time = rrdtool.last(rrd_filename) - sample_rate
            start_time = (end_time + sample_rate) - (sample_rate*num_vals)
            fetched_vals = rrdtool.fetch(rrd_filename,
                                         'LAST',
                                         '-r', str(sample_rate),
                                         '-s', str(start_time),
                                         '-e', str(end_time))
            # get values from fetched list and add times (in secs since epoch)
            time_values_list = []
            for index, value in enumerate(fetched_vals[2]): 
                time_values_list.append((start_time + ((index+1)*sample_rate),
                                        value[0]))
            return time_values_list
        except rrdtool.ProgrammingError as e:
            self.logger.debug('A user programming error occurred in \
                              get_time_value_list function in lib_rrdtool.')
            self.logger.error(e)
        except rrdtool.OperationalError as e1:
            self.logger.debug('An operational error (such as a filesystem \
                              error) occurred in get_time_value_list function \
                              in lib_rrdtool.')
            self.logger.error(e1)
        except TypeError as e2:
            self.logger.debug('Parameter of incorrect type used in \
                              get_time_value_list function in lib_rrdtool.')
            self.logger.error(e2)
        return None

    def format_time(self, time_stamp, sample_rate):
        #TODO: Expand docstring
        """Format time_stamp by rounding up to next sample_rate divisible value. 
        """
        try:
            time_stamp = float(time_stamp)
            formatted_time_stamp = \
                int(int(sample_rate)*math.ceil(float(time_stamp/int(
                    sample_rate))))
            return formatted_time_stamp
        except TypeError as e:
            self.logger.debug('Parameter of incorrect type used in \
                              format_time function in lib_rrdtool.')
            self.logger.error(e)
            return None