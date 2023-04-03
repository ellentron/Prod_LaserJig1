# import matplotlib.pyplot as plt
import time

import matplotlib.animation as animation

from power_meter import PowerMeter

import tkinter as tk
import matplotlib.pyplot as plt
from gui import GUI
from toptica.lasersdk.client import Client, NetworkConnection


# class PmMeasure405
class PmMeasure405:
    def __init__(self):
        # matplotlib boilerplate
        self.is_plot_paused = False
        self.plt = plt
        self.xs = []
        self.ys = []
        self.fig, self.ax = self.plt.subplots()
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, fargs=(self.xs, self.ys), interval=1000)

        # tkinter boilerplate
        self.root = tk.Tk()
        self.app = GUI(master=self.root, start_test_callback=self.start_test,
                       pause_test_callback=self.pause_or_resume_test,
                       stop_test_callback=self.stop_test)
        self.app.start_test_callback = self.start_test


        self.pm = PowerMeter()

    def initialize(self):
        # self.plt = plt
        self.pm.initialize(wl=405)

        self.root.mainloop()

    def start_test(self):
        self.is_plot_paused = False
        # Show the plot
        # self.plt.show()
        print("Test started")
        run_laser405_pm_test = self.run_test()

    def pause_or_resume_test(self):
        if self.is_plot_paused:
            print("Resuming test")
            self.is_plot_paused = False
            self.ani.event_source.start()

        else:
            self.is_plot_paused = True
            self.ani.event_source.stop()
            print("Test Paused")
        print("Test paused")

    def stop_test(self):
        print("Stopping test")
        self.ani.event_source.stop()
        # plt.close()

    def update_plot(self, i, xs, ys):
        # Get the next measurement

        measurement = self.pm.get_power()
        print(f"Power meter measured: {measurement} mW")

        xs.append(i)
        ys.append(measurement)
        # Update the plot data
        self.ax.clear()
        self.ax.plot(xs, ys)


    def run_test(self):
        print("Running test")
        # Create laser 405 instance

        # Verify that the laser is connected
        my_laser_ip_address = '10.0.30.2'
        with Client(NetworkConnection(host=my_laser_ip_address, timeout=700)) as client:
            system_type = client.get('system-type')
            serial_number = client.get('serial-number')
            laser1_model = client.get('laser1:model')
            laser1_wavelength = client.get('laser1:wavelength')
            laser1_serial_number = client.get('laser1:serial-number')
            laser1_production_date = client.get('laser1:production-date')
            laser1_vendor = client.get('laser1:vendor')
            laser1_ontime_txt = client.get('laser1:ontime-txt')

            print('===============================================================================================')
            print(f"This is a {system_type} controller with serial number: {serial_number}")
            print(f"Laser1 - Model:{laser1_model}, Wavelength:{laser1_wavelength}, "
                  f"Serial Number:{laser1_serial_number}, Production Date:{laser1_production_date}, "
                  f"Vendor:{laser1_vendor}, On Time:{laser1_ontime_txt}")
            # print(f"Laser1 - On Time:{laser1_ontime}")
            print('===============================================================================================')

            # Turn laser on
            cmd_result = client.set('laser1:enable-emission', True)
            time.sleep(1)
            cmd_result = client.set('laser1:enable-emission', True)
            time.sleep(1)
            # Get laser emmission state
            laser1_emmision_state = client.get('laser1:emission')

            print(f"Laser1 - Emission State:{laser1_emmision_state}")

        # Verify that the power meter is connected
        dummy_pwr_reading = self.pm.get_power()
        print(f"Verify that the power meter is connected, Power meter measured: {dummy_pwr_reading} mW")

        # Get information from laser (S/N, wavelength, etc.)

        # Verify that the laser information matches the configuration file

        # Turn laser on

        # Get spec. from spec. file

        # Init mode hops counter

        # Init Error messages list

        # Init general massages list

        # Prepare folders tree (if doesn't exist)

        # Set filter state (IN)

        # Set power meter range (30mW)

        # Flush power meter buffer

        # Perform laser warmup (while measuring and looking for errors)

        # Perform extended CHARM
        with Client(NetworkConnection(host=my_laser_ip_address, timeout=700)) as client:
            laser1_charm_correction_status = client.get('laser1:charm:correction-status')
            print(f"Charm Status: {laser1_charm_correction_status}")
            # ch_status = client.exec('laser1:charm:start-correction-extended')
            time.sleep(2)
            laser1_charm_correction_status = client.get('laser1:charm:correction-status')
            print(f"Charm Status: {laser1_charm_correction_status}")


        # If no errors, perform main test loop

            # If no errors, perform post test loop

            # Measure itterations
            # Show the plot
            self.plt.show()

            # Time for CHARM ?

                # Perform for extended CHARM

        # Prepare final analysis

        # Turn laser off

        # Test finished...
