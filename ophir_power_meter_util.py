import time
import numpy as np
import win32com.client


class Ophir(object):

    def __init__(self, head=0, sensor=0, range_mw=None):
        self.Type = 'Powermeter'
        self.sensor = sensor
        self.ophir = win32com.client.Dispatch('OphirLMMeasurement.CoLMMeasurement')
        self.ophir.StopAllStreams()
        self.ophir.CloseAll()
        heads = self.ophir.ScanUSB()
        # print(heads)
        if len(heads) > 0:
            self.USB = self.ophir.OpenUSBDevice(heads[head])
            self.ophir.StartStream(self.USB, sensor)
            self.initOK = True
            self.ranges_list = self.get_ranges()[1]
            if range_mw is None:
                range_mw = 0
            if isinstance(range_mw, str):
                idx = np.where(range_mw == np.array(self.ranges_list))[0]
                if len(idx) == 0:
                    raise ValueError(f'range_mw string value "{range_mw}" does not exist in power meter ranges list.')
                else:
                    range_mw = int(idx)

            if isinstance(range_mw, int):
                self.set_range(range_mw)
                if range_mw > 0:
                    print('Power meter range is set to', self.ranges_list[range_mw])
            else:
                raise TypeError('range_mw should be None, int or string')

        else:
            print('No Ophir devices found')
            self.initOK = False
        self.wl_range = self.get_wavelength_extra()[1:3]

    def close(self):
        self.ophir.StopStream(self.USB, self.sensor)
        self.ophir.Close(self.USB)

    def get_data(self):
        return np.array(self.ophir.GetData(self.USB, self.sensor))

    def get_last_data(self):
        data = self.get_data()
        if len(data[0]) > 0:
            return data[:, -1]
        else:
            return np.nan

    def get_power(self):
        try:
            p = self.get_last_data()[0] * 1000
            return p
        except:
            return -1

    def get_ranges(self):
        return self.ophir.GetRanges(self.USB, self.sensor)

    def set_range(self, r):
        self.ophir.StopStream(self.USB, self.sensor)
        time.sleep(0.2)
        self.ophir.SetRange(self.USB, self.sensor, r)
        time.sleep(0.2)
        self.ophir.StartStream(self.USB, self.sensor)

    def get_wavelengths(self):
        return self.ophir.GetWavelengths(self.USB, self.sensor)

    def set_wavelength(self, wl):
        wls = self.get_wavelengths()
        active_wl = int(wls[1][wls[0]])
        if active_wl == wl: return
        if wl < self.wl_range[0] or wl > self.wl_range[1]:
            print('Input wavelength is out of sesor range [200-1800nm]')
            return
        if str(wl) in wls[1]:
            self.set_wavelength_index(wls[1].index(str(wl)))
        else:
            self.add_wavelength(wl)
            wls = self.get_wavelengths()
            self.set_wavelength_index(wls[1].index(str(wl)))

    def add_wavelength(self, wl):
        self.ophir.StopStream(self.USB, self.sensor)
        time.sleep(0.2)
        self.ophir.AddWavelength(self.USB, self.sensor, wl)
        time.sleep(0.2)
        self.ophir.StartStream(self.USB, self.sensor)

    def get_wavelength_extra(self):
        self.ophir.StopStream(self.USB, self.sensor)
        time.sleep(0.2)
        out = self.ophir.GetWavelengthsExtra(self.USB, self.sensor)
        time.sleep(0.2)
        self.ophir.StartStream(self.USB, self.sensor)
        return out

    def set_wavelength_index(self, wl_idx):
        self.ophir.StopStream(self.USB, self.sensor)
        time.sleep(0.2)
        self.ophir.SetWavelength(self.USB, self.sensor, wl_idx)
        time.sleep(0.2)
        self.ophir.StartStream(self.USB, self.sensor)

    def get_filter(self):
        filter = self.ophir.GetFilter(self.USB, self.sensor)
        return filter[1][filter[0]]

    def set_filter_index(self, filter_idx):
        self.ophir.StopStream(self.USB, self.sensor)
        time.sleep(0.2)
        self.ophir.SetFilter(self.USB, self.sensor, filter_idx)
        time.sleep(0.2)
        self.ophir.StartStream(self.USB, self.sensor)

    def set_filter(self, filter_state):
        filter_state = str(filter_state).upper()
        if filter_state not in ['IN', 'OUT']:
            print("Input filter state is not an option ['IN','OUT']")
            return
        current_filter = self.get_filter()
        if current_filter == filter_state:
            return
        else:
            filters = self.ophir.GetFilter(self.USB, self.sensor)
            self.set_filter_index(filters[1].index(filter_state))


if __name__ == "__main__":
    pm = Ophir()
    pm.set_filter('OUT')
    time.sleep(1)
    #    print(pm.get_wavelengths())
    pm.set_wavelength(532)
    print('power = %0.3f' % pm.get_power())
#    pm.close()
