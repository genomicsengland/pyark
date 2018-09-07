from protocols.protocol_7_0.cva import VariantCoordinates
import re


def map_variant_id_to_variant(variant_id):
    """
    :type variant_id: str
    :rtype: VariantRepresentation
    """

    match = re.match(r'(GRCh37|GRCh38):(.*):([ 0-9]*):(-| |[ACGTacgt]*):(-| |[ACGTacgt]*)', variant_id)
    if match:
        assembly = match.group(1)
        chromosome = match.group(2)
        position = match.group(3).strip()
        reference = match.group(4)
        alternate = match.group(5)
    else:
        raise ValueError("Wrong variant identifier: {}".format(variant_id))

    variant = VariantCoordinates()
    variant.assembly = assembly
    variant.chromosome = chromosome
    variant.position = position
    variant.reference = reference
    variant.alternate = alternate
    return variant
