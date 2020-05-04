

def set_price_for_modifiers(instance, **kwargs):
    """
    to set price to 0 when the modifiers are free of cost
    :param instance:
    :param kwargs:
    :return:
    """
    if instance.free == True:
        instance.price = 0


def seating_modifier(instance, **kwargs):

    id = instance.id
    instance.seating_number = id
    if instance.waiter is not None:
        instance.seating_status = 'occupied'
    elif instance.reservation is not None:
        instance.seating_status = 'reserved'
    else:
        instance.seating_status = 'available'


def invoice_modifier(instance, **kwargs):
    id = instance.id
    instance.invoice_number = id








