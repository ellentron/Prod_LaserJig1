"""""""""""""""""""""""""""""""""
Production Laser Jig Utility
"""""""""""""""""""""""""""""""""
from pm_measure_405 import PmMeasure405

pmm405 = PmMeasure405()
pmm405.initialize()




# import time
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
# from power_meter import PowerMeter
#
# import tkinter as tk
# from gui import GUI
#
# class AppInfo:
#     version = '0.0.1'
#
#
# def stop_test():
#     print("Stopping test")
#     ani.event_source.stop()
#     #plt.close()
#
#
# def start_test():
#     print("Test started")
#
#     # Show the plot
#     plt.show()
#
#
# def pause_or_resume_test():
#     global is_plot_paused
#     if is_plot_paused:
#         print("Resuming test")
#         is_plot_paused = False
#         ani.event_source.start()
#
#     else:
#         is_plot_paused = True
#         ani.event_source.stop()
#         print("Test Paused")
#     print("Test paused")
#
# # Define the function that will update the mplotlib plot
# def update_plot(i, xs, ys):
#     # Get the next measurement
#     # measurement = get_next_measurement()
#     measurement = pm.get_power()
#     print(f"Power meter measured: {measurement} mW")
#     # xs.append(measurement[0])
#     xs.append(i)
#     ys.append(measurement)
#     # Update the plot data
#     ax.clear()
#     ax.plot(xs, ys)
#
# """
# Main
# """
# # Instance of application information class
# if __name__ == "__main__":
#     app_info = AppInfo()
#     print(f"Laser testing utility application version: {app_info.version}")
#
#     # Create instance of power meter class
#     pm = PowerMeter()
#     # Initialize power meter
#     pm.initialize(wl=405)
#
#     """
#     GUI
#     """
#     root = tk.Tk()
#     app = GUI(master=root, start_test_callback=start_test, pause_test_callback=pause_or_resume_test, stop_test_callback=stop_test)
#     app.start_test_callback = start_test
#
#
#     # Initialize plot data arrays
#     xs = []
#     ys = []
#
#     # Initialize the figure and axis objects
#     fig, ax = plt.subplots()
#
#
#     # Create the animation object
#     ani = animation.FuncAnimation(fig, update_plot, fargs=(xs, ys), interval=1000)
#
#     is_plot_paused = False
#
#     root.mainloop()
#
# # if __name__ == "__main__":
# #     import tkinter as tk
# #     from gui import GUI
# #     root = tk.Tk()
# #     app = GUI(master=root, start_test_callback=start_test, pause_test_callback=pause_or_resume_test, stop_test_callback=stop_test)
# #     app.start_test_callback = start_test
# #     root.mainloop()
#
# """
# Plot
# """
#
#
#
#
#
#
# """
# ✓ Laser 405
# """
#
#
# """
# Laser 457 and 532
# """
#
# """
# ✓ Power Meter
# """
# # See power_meter.py
#
# """
# ✓ Wavelength Meter
# """
# # See wlm.py
#
# """
# Spectrum Analyzer
# """
#
# """
# Fiber Scope
# """
#
# """
# Reports
# """
