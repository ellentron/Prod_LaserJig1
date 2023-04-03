import time
from wheels.High_Finesse_Spectrum.high_finesse import WavelengthMeter


wlm = WavelengthMeter()
wlm.wl = 405  # !!!!!!!!!!! temporary
wlm.operation = wlm.OperationState.measurement

wl_to_n = {
    405: 1.00029356,
    457: 1.00029135,
    532: 1.00028927
}


def vaccum_to_air(nominal_wl, wl_vac):
    if wl_vac == 0 or not wl_vac:
        return 0
    refraction_index = wl_to_n.get(nominal_wl)
    if refraction_index is None:
        raise ValueError(f'Refraction index for WL {nominal_wl} is not defined')
    return wl_vac / refraction_index


get_meas_func = lambda: vaccum_to_air(nominal_wl=wlm.wl, wl_vac=wlm.wavelengths[0])

for i in range(10):
    print(f"Measured wavelength:{get_meas_func()} nm")
    time.sleep(1)


def vaccum_to_air(nominal_wl, wl_vac):
    if wl_vac == 0 or not wl_vac:
        return 0
    refraction_index = wl_to_n.get(nominal_wl)
    if refraction_index is None:
        raise ValueError(f'Refraction index for WL {nominal_wl} is not defined')
    return wl_vac / refraction_index
