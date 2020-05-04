ITEM_TYPE_CHOICES = (
    ('veg', 'Veg'),
    ('non_veg', 'Non-veg'),
    ('undefined', 'Undefined')
)

ORDER_TYPE_CHOICES = (
    ('take_away', 'take away'),
    ('dine_in', 'dine in'),
    ('delivery', 'delivery')
)

ENABLE_DISABLE_CHOICES = (
    ('enabled', 'Enabled'),
    ('disabled', 'Disabled')
)

PAYMENT_CHOICE = (
    ('cash', 'Cash'),
    ('card', 'Card'),
    ('credit', 'Credit')
)

INVOICE_STATUS = (
    ('unpaid', 'Unpaid'),
    ('paid', 'Paid'),
    ('canceled', 'Canceled')
)

DELIVERY_CHOICES = (
    ('in_progress', 'In Progress'),
    ('delivered', 'Delivered')
)

SEATING_STATUS = (
    ('reserved', 'Reserved'),
    ('occupied', 'Occupied'),
    ('available', 'Available'),
)

CREDIT_STATUS_CHOICES = (
    ('credited', 'Credited'),
    ('debited', 'Debited')
)

ORDER_STATUS_CHOICES = (
    ('ordered', 'Ordered'),
    ('in_progress', 'In progress'),
    ('ready', 'Ready'),
    ('served', 'Served'),
    ('revised', 'Revised')
)

EMPLOYEE_TYPE_CHOICES = (
    ('superadmin', 'Super Admin'),
    ('companyadmin', 'Company Admin'),
    ('BranchAdmin', 'Branch Admin'),
    ('staff', 'Staff')
)

PAYMENT_MODE =(
    ('cash', 'Cash'),
    ('credit', 'Credit'),
)

CREDIT_LIMIT = (
    ('1', 'notify over limit'),
    ('2', 'hold over limit')
)

PAYMENT_STATUS = (
    ('paid', 'paid'),
    ('unpaid', 'unpaid')
)

PAYMENT_MODE_FOR_VENDOR = (
    ('cash', 'cash'),
    ('cheque', 'cheque')
)