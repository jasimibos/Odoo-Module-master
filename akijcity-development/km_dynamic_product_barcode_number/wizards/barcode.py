import re


def generate_ean(self, ean):
    """Creates and returns a valid ean13 """
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    # prefix
    # prefix = self.env['ir.config_parameter'].sudo().get_param('km_dynamic_product_barcode_number.barcode_prefix')
    # if prefix == False:
    #     prefix = "99"

    prefix = "11"
    if len(ean) < 13:
        ean = str(prefix) + '0' * (5 - len(ean)) + ean + '0' * 6

    return ean