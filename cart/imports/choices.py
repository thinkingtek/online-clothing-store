SIZES = (
    ('', 'Select Size'),
    ('l', 'L'),
    ('md', 'md'),
    ('sm', 'sm'),
    ('xl', 'xl'),
)
COLORS = (
    ('', 'Select colour'),
    ('red', 'red'),
    ('blue', 'blue'),
    ('white', 'white'),
    ('black', 'black'),
    ('yellow', 'yellow'),
    ('purple', 'purple'),
    ('others', 'others'),
)
EMAIL_SUBJECTS = (
    ('', 'Email Subject'),
    ('complain', 'Complain'),
    ('testimonial', 'Testimonial'),
    ('inquiry', 'Inquiry'),
    ('others', 'Others'),
)
SHIPPING_METHOD = (
    ('', 'Shipping method'),
    ('home delivery', 'Home delivery'),
    ('personal pickup', 'Personal pickup'),
    ('express delivery', 'Express delivery')
)
PAYMENT_METHOD = (
    ('', 'Payment method'),
    ('cash', 'Cash'),
    ('bank transfer', 'Bank transfer'),
    ('paystack', 'Paystack'),
    ('flutterwave', 'Flutterwave'),
)
TAGS = (
    # ('', 'MALE / FEMALE'),
    ('classy', 'classy'),
    ('sport', 'sport'),
    ('occassion', 'occassion'),
    ('indoor', 'indoor'),
    ('outdoor', 'outdoor'),
)
CATEGORIES = (
    # ('', 'MALE / FEMALE'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('unisex', 'Unisex'),
    ('kids', 'Kids'),
)
ORDER_STATUS = (
    ('', 'Status (intransit/delivered)'),
    ('packaging', 'Packaging'),
    ('in-transit', 'In-Transit'),
    ('delivered', 'Delivered'),
    ('not-shipped', 'Not Shipped'),
    ('refunded', 'Refunded'),
)
states_options = (
    ('', '<- Choose State ->'),
    ('delta', 'Delta'),
    ('bayelsa', 'Bayelsa'),
    ('rivers', 'Rivers'),
    ('abuja', 'Abuja'),
    ('cross-rivers', 'Cross-Rivers'),
    ('akwa-ibom', 'Akwa-Ibom'),
    ('anambra', 'Anambra'),
    ('enugu', 'Enugu'),
    ('imo', 'Imo'),
    ('lagos', 'Lagos'),
    ('ogun', 'Ogun')
)

STATES = sorted(states_options, key=lambda x: x[1])
