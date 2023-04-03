import time
from ophir_power_meter_util import Ophir


class PowerMeter:
    """
    Handle Power Meter Operations
    """

    # Constractor
    def __init__(self):
        """
        Power Meter object
        """
        self.__filter_state = 'IN'
        self.__power_meter_range_mW = '30.0mW'
        # Instantiate Ophir Power Meter instance

    # Getters and Setters
    @property
    def filter_state(self):
        """
        Get Power Meter filter state
        :return: Power Meter filter state
        """
        return self.__filter_state

    @filter_state.setter
    def filter_state(self, value):
        """
        Set Power Meter filter state
        """
        self.__filter_state = value

    @property
    def power_meter_range_mW(self):
        """
         Get power meter range
         :return: Power meter range [mW]
         """
        return self.__power_meter_range_mW

    @power_meter_range_mW.setter
    def power_meter_range_mW(self, value):
        """
        Set required power meter range
        :return: Power meter range [mW]
        """
        self.__power_meter_range_mW = value

    def initialize(self, wl):
        try:
            # Instantiate Ophir Power Meter instance
            self.__pm = Ophir(range_mw=self.power_meter_range_mW)
            self.__pm.set_wavelength(wl)
            self.__pm.set_filter(self.filter_state)
        except:
            print('Cannot connect to power meter.')
            raise

    def get_power(self):
        """
        Get latest power measurement
        :return: Power [mW]
        """
        return self.__pm.get_power()

    def flush_old_readings(self):
        """
        Flush old power meter readings
        :return:
        """
        for i in range(10):
            pwr = self.get_power()
            print(f"Power meter measured: {pwr} mW")
            time.sleep(0.1)
