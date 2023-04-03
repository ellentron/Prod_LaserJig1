from enum import Enum
import time
import logging

try:
    from toptica_.lasersdk.client import Client, NetworkConnection, SerialConnection


except ImportError:
    try:
        from toptica.lasersdk.client import Client, NetworkConnection, SerialConnection
    except ImportError:
        print(f"Client {Client}, NetworkConnection {NetworkConnection}, SerialConnection {SerialConnection}")
        print('no toptica.lasersdk module - cannot connect to Toptica laser')

'''
from toptica.lasersdk.client import Client, NetworkConnection
client = Client(NetworkConnection('10.0.10.11'))
 client.open
 client.close
client.get('emission', bool)
client.set('enable-emission', True)
client.get('laser1:intensity', float)
client.get('laser1:charm:reg:mh-occurred', bool)
client.get('laser1:charm:correction-status', int) returns 0-3
client.exec('laser1:charm:start-correction-initial')
client.get('laser1:serial-number', str)
client.get('laser1:model', str)
client.get('laser1:wavelength', float)
client.get('laser1:production-date', str)
client.get('laser1:ontime', int) # sec
client.get('laser1:health-txt', str)

laser1:tec:ready bool

'''


class Toptica405Laser:
    class ConnectionMuckUp:
        def __init__(self, ip_address=None, COM_port=None, timeout=5):
            if ip_address is not None and COM_port is not None:
                raise ValueError('Toptica laser at direct connection can have either IP address or COM port, not both')
            if ip_address is not None:
                self._toptica_client = Client(NetworkConnection(ip_address, timeout=timeout))
            else:
                self._toptica_client = Client(SerialConnection(COM_port))
            self._toptica_client.open()
            self._toptica_405_laser_number = 1

        def disconnet(self):
            self._toptica_client.close()

    class Laser405CharmFailed(Exception):
        pass

    class Laser405CharmNotStarted(Exception):
        pass

    class Laser405CharmTimeout(Exception):
        pass

    class CharmStatus(Enum):
        NotStarted = 0
        InProcess = 1
        Complete = 2
        Failed = 3
        Failed_1 = 4
        Completed_Open_Loop = 5

    def __init__(self, conn_obj=None, ip_address=None, COM_port=None, timeout=4):
        if conn_obj is not None:
            self._conn_obj = conn_obj
        else:
            self._conn_obj = Toptica405Laser.ConnectionMuckUp(ip_address, COM_port)
            self.disconnect = self._conn_obj.disconnet
        self._firstCharm = True
        self._set_on_time = None
        self._logger = logging.getLogger('ElipsonSys.Lasers')
        if self._client is not None:
            status_report = [('Charm', self.charm_status), ('was mode hop', self.was_a_mod_hop),
                             ('power', self.get_power), ('SN', self.get_serial_number),
                             ('wavelength', self.get_wavelength), ('on_time', self.get_on_time_seconds),
                             ('health_status', self.get_health_status), ('tec_ready', self.is_tec_ready)]
            self._logger.debug('Toptica 405 status: ' + ','.join(['%s=%s' % (p, f()) for p, f in status_report]))

    @property
    def _client(self):
        return self._conn_obj._toptica_client  # TopticaLaser('COM7',115200,timeout=1)

    @property
    def _laser_number(self):
        return self._conn_obj._toptica_405_laser_number

    def _getparam(self, P, otype):
        laser = 'laser' + str(self._laser_number) + ':'
        return self._client.get(laser + P, otype)

    def _setparam(self, P, val):
        laser = 'laser' + str(self._laser_number) + ':'
        # self._client.set(laser + 'enable-emission', val)
        self._client.set(laser + P, val)

    def _exec(self, C):
        laser = 'laser' + str(self._laser_number) + ':'
        self._client.exec(laser + C)

    '''
    def _write(self, STR):
        if self._serial_socket is None: return
        self._serial_socket.flush()
        STR = (STR).encode('UTF-8') + self._write_teminator
        self._serial_socket.write(STR)
        #time.sleep(self.defaultDelay)

    def _query(self, Q):
        if self._serial_socket is None: return
        self._serial_socket.flushInput()
        self._serial_socket.flush()
        self._write(Q)
        time.sleep(self._query_delay)
        A = self._serial_socket.read_until(self._read_terminator).decode('UTF-8').strip(Q).strip(
            self._read_terminator.decode('UTF-8')).strip('\r\n')
        try:
            return (float(A))
        except:
            return A
    '''

    def on(self):
        self._setparam('enable-emission', True)

        self._firstCharm = True
        self._set_on_time = time.time()

    def off(self):
        self._setparam('enable-emission', False)
        self._firstCharm = True

    def is_on(self):
        return self._getparam('emission', bool)

    def get_power(self):
        return self._getparam('intensity', float)

    def was_a_mod_hop(self):
        #        print('a', time.time())
        was_hop = self._getparam('charm:reg:mh-occurred', bool)
        #        print('b', time.time())
        return was_hop

    def do_charm(self):
        self.charm_start()
        return self.wait_for_charm_ending()

    def charm_start(self):
        if not self.is_on():
            print('Turn laser on before trying to CHARM.')
            return
        #        if self._set_on_time is not None and time.time()-self._set_on_time < 30*60:
        #            if 'y' not in input('it is recommanded the that laser will be on at least half an hour before'
        #                                ' charm (on for %.1f min). continue(y/n)?' % ((time.time()-self._set_on_time)/60)).lower():
        #                return
        # if self._firstCharm:
        #     self._exec('charm:start-correction-initial')
        # else:
        #     self._exec('charm:start-correction')
        self._exec('charm:start-correction')
        time.sleep(1)

    def charm_status(self):
        c_stat = self._getparam('charm:correction-status', int)
        return Toptica405Laser.CharmStatus(c_stat)

    #        print(c_stat)
    # charm_status =  Toptica405Laser.CharmStatus(c_stat )
    # if charm_status == Toptica405Laser.CharmStatus.Failed:
    #     raise Toptica405Laser.Laser405CharmFailed()
    # else:
    #     return charm_status

    def wait_for_charm_ending(self):
        if self.charm_status() == Toptica405Laser.CharmStatus.NotStarted:
            return
            # raise RuntimeError('Toptica 405 laser - charm not started')
        timeout = 3.5 * 60
        start_waiting = time.time()
        while time.time() - start_waiting < timeout:
            c_s = self.charm_status()
            if c_s == Toptica405Laser.CharmStatus.Complete or c_s == Toptica405Laser.CharmStatus.Failed or c_s == Toptica405Laser.CharmStatus.Completed_Open_Loop:
                return c_s
            time.sleep(5)
        else:
            raise Toptica405Laser.Laser405CharmTimeout(
                f'Toptica 405 laser - charm exceeds timeout of {timeout} seconds.')

    def get_charm_controller_firmware_version(self):
        return self._client.get('fw-ver', str)

    def get_software_version(self):
        return self._client.get('ssw-ver', str)

    def get_serial_number(self):
        return self._getparam('serial-number', str)

    def get_model(self):
        return self._getparam('model', str)

    def get_wavelength(self):
        return self._getparam('wavelength', float)

    def get_production_date(self):
        return self._getparam('production-date', str)

    def get_on_time_seconds(self):
        return self._getparam('ontime', int)

    def get_health_status(self):
        return self._getparam('health-txt', str)

    def is_tec_ready(self):
        return self._getparam('tec:ready', bool)
