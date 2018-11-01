import pyark.cva_client as cva_client
from protocols.protocol_7_0.cva import VariantsCoordinates, VariantCoordinates
import pyark.models_mapping


class LiftOverClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "lift-overs"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def lift_over_by_identifiers(self, variant_identifiers, variant_format='VCF', force_symmetric=True):
        """
        :param variant_format: Any value from "VCF", "OPENCB"
        :type variant_format: str
        :param force_symmetric: only returns lift over if it is symmetric
        :type force_symmetric: bool
        :param variant_identifiers: the list of variant identifiers in format
        {assembly}:{chromosome}:{position}:{reference}:{alternate}
        :type variant_identifiers: list
        :return list of VariantCoordinates
        :rtype: list
        """
        variant_coordinates_list = [pyark.models_mapping.map_variant_id_to_variant(variant_id)
                                    for variant_id in variant_identifiers]
        variants_coordinates = VariantsCoordinates()
        variants_coordinates.variants = variant_coordinates_list

        results, _ = self._post(self._BASE_ENDPOINT, payload=variants_coordinates.toJsonDict(),
                                params={'variantFormat': variant_format, 'forceSymmetric': force_symmetric})
        assert len(results) == len(variant_identifiers), "Some variants failed to lift over"

        return [VariantCoordinates.fromJsonDict(x) for x in results]

    def lift_over_by_variants_coordinates(self, variant_coordinates_list, variant_format='VCF', force_symmetric=True):
        """
        :param variant_format: Any value from "VCF", "OPENCB"
        :type variant_format: str
        :param force_symmetric: only returns lift over if it is symmetric
        :type force_symmetric: bool
        :param variant_coordinates_list: the list of VariantCoordinates
        :type variant_coordinates_list: list
        :return list of VariantCoordinates
        :rtype: list
        """
        variants_coordinates = VariantsCoordinates()
        variants_coordinates.variants = variant_coordinates_list

        results, _ = self._post(self._BASE_ENDPOINT, payload=variants_coordinates.toJsonDict(),
                                params={'variantFormat': variant_format, 'forceSymmetric': force_symmetric})
        assert len(results) == len(variant_coordinates_list), "Some variants failed to lift over"

        return [VariantCoordinates.fromJsonDict(x) for x in results]
