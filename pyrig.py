import numpy as np
import pint as pt

ureg = pt.UnitRegistry()


BEAM = ureg("4.96m")
# from sykes chart
nominal_rm30 = 260000 * ureg("foot*lbs")
# from measuring Kess
measured_rm30 = 46785.6 *ureg("kg * m")
nominal_rm30 = measured_rm30

nominal_rm30 = 6925 * ureg("kg * m")
BEAM = ureg('3.3m')

def rm30(cant, weight, moment_arm):
    """
    cant: how far you tipped the boat, in degrees
    weight: how much weight you added to get that tilt, in kg
    moment_arm: how far away from the centerline you put the weight, in meters

    returns RM30: the foot-pounds of torque required to cant the boat to 30deg
    """
    cant = cant * ureg('degrees')
    weight = weight * ureg('kg')
    moment_arm = moment_arm * ureg('m')

    torque = weight * moment_arm
    RM30 = torque * 30 * ureg('degrees') / cant
    return RM30


def shroud_load(rm30=nominal_rm30, beam=BEAM, extra_factor=1.5):
    """
    rm30: Righting moment at 30 degrees, in torque units
    beam: beam of the ship in length units
    extra factor: some sort of safety factor in the rm30, defaults to 1.5
    """
    return rm30 * extra_factor / (0.5 * beam)


def mast_compression_load(rm30=nominal_rm30, beam=BEAM, extra_factor=1.5, extra_mast_factor=1.85):
    """
    rm30: Righting moment at 30 degrees, in torque units
    beam: beam of the ship in length units
    extra factor: some sort of safety factor in the rm30, defaults to 1.5
    extra_mast_factor: normally stays add an extra 85% to mast load
    """
    return rm30 * extra_factor * extra_mast_factor / (0.5 * beam)


def mast_moment(C, L, compression_load, deck_stepped=True):
    """
    C =  constant:
        transverse:
            Spruce, single spreader: 6.78
            Spruice, double_spreader: 8.11
            Aluminum, single spreader: 0.94
            Aluminum, double spreader: 1.12
            Steel, single spreader: .33

        longitudinal:
            spruce, masthead: 4.0
            spruce, fractional: 3.74
            aluminum, masthead: 0.54
            aluminum, fractional: 0.52
            steel, masthead: 0.189
    multiply by 1.5 if deck-steped

    L: Length between deck and spreaders, or deck and jibstay
    compression_load: compression load on mast computer above

    """

    C = C * ureg("in ** 2 / lb")
    moment = C * (L ** 2) * compression_load
    if deck_stepped:
        moment = moment * 1.5

    return moment / 1e8


if __name__ == "__main__":
    print("shroud loads")
    print(shroud_load())
    crosstrees_height = 12.26 * ureg('m')
    forestay_height = 13.5 * ureg('m')
    cl = mast_compression_load()
    print("Aluminum")
    print("longitudinal estimate")
    print(mast_moment(.54, forestay_height, cl).to("cm**4"))
    print("transverse estimate")
    print(mast_moment(.94, crosstrees_height, cl).to("cm**4"))
    print("Spruce")
    print("longitudinal estimate")
    print(mast_moment(4, forestay_height, cl).to("cm**4"))
    print("transverse estimate")
    print(mast_moment(6.78, crosstrees_height, cl).to("cm**4"))
    print("Steel")
    print("longitudinal estimate")
    print(mast_moment(.189, forestay_height, cl).to("cm**4"))
    print("transverse estimate")
    print(mast_moment(.33, crosstrees_height, cl).to("cm**4"))

