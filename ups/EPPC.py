from ups import RfcUps


class PowerWalkerEPPC(RfcUps):
    """
    PowerWalker UPS identifying as EPPC
    """

    def input_frequency(self, phase=1) -> float:
        return super(PowerWalkerEPPC, self).input_frequency(phase)

    def input_voltage(self, phase=1) -> float:
        return super(PowerWalkerEPPC, self).input_voltage(phase)

    def input_current(self, phase=1) -> float:
        return super(PowerWalkerEPPC, self).input_current(phase)

    def input_true_power(self, phase=1):
        return super(PowerWalkerEPPC, self).input_true_power(phase)
