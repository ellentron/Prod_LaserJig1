# from Toptica405Laser_s import Toptica405Laser as tl
from toptica.lasersdk.client import Client, NetworkConnection

# laser_405_ip_address = '10.0.30.2'
# laser_405 = tl(conn_obj=None, ip_address=laser_405_ip_address, COM_port=None, timeout=4)
# print(f"CHARM Status: {tl.CharmStatus.}")
#
#
# charm_status_enum = tl.CharmStatus

my_laser_ip_address = '10.0.30.2'
with Client(NetworkConnection(host=my_laser_ip_address, timeout=5)) as client:
    system_type = client.get('system-type')
    serial_number = client.get('serial-number')
    laser1_model = client.get('laser1:model')
    laser1_wavelength = client.get('laser1:wavelength')
    laser1_serial_Number = client.get('laser1:serial-number')
    laser1_production_date = client.get('laser1:production-date')
    laser1_vendor = client.get('laser1:vendor')
    laser1_ontime_txt = client.get('laser1:ontime-txt')

    print('===============================================================================================')
    print(f"This is a {system_type} controller with serial number: {serial_number}")
    print(f"Laser1 - Model:{laser1_model}, Wavelength:{laser1_wavelength}, "
          f"Serial Number:{laser1_serial_Number}, Production Date:{laser1_production_date}, "
          f"Vendor:{laser1_vendor}")
    # print(f"Laser1 - On Time:{laser1_ontime}")
    print('===============================================================================================')

    """ Charm """
    # laser1_charm_correction_status = client.get('laser1:charm:correction-status')
    # print(f"Charm Status: {laser1_charm_correction_status}")
    # ch_status = client.exec('laser1:charm:start-correction-extended')
    # time. sleep(2)
    # laser1_charm_correction_status = client.get('laser1:charm:correction-status')
    # print(f"Charm Status: {laser1_charm_correction_status}")
    # while laser1_charm_correction_status == 1:
    #     laser1_charm_correction_status = client.get('laser1:charm:correction-status')
    #     print(f"Charm Status: {laser1_charm_correction_status}")
    #
    # laser1_charm_correction_status = client.get('laser1:charm:correction-status')
    # print(f"Charm Status: {laser1_charm_correction_status}")

    #service_report_txt = client.exec('service-summary-txt')

""" Service Report """
# with Client(NetworkConnection(host=my_laser_ip_address, timeout=700)) as client:
    # service_report = client.exec('service-report')
    # service_report_txt = client.exec('service-summary-txt')
