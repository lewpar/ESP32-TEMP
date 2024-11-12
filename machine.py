# STUB FOR MACHINE MODULE

class Pin:
    IN = 0
    """
    Input pin mode.
    """

    OUT = 0
    """
    Output pin mode.
    """

    IRQ_FALLING = 0
    IRQ_RISING = 0

    def __init__(self, pin_id, pin_mode):
        pass

    def on():
        """
        Writes a HIGH value to the GPIO pin. The pin must be configured as Pin.OUT.
        """

    def off():
        """
        Writes a LOW value to the GPIO pin. The pin must be configured as Pin.OUT.
        """

    def irq(handler: function = None, trigger: int = IRQ_FALLING | IRQ_RISING, *, 
            priority: int = 1, wake: int = None, hard: bool = False):
        """
        Creates an Interrupt Request (IRQ) when a trigger is detected on the pin.
        """