import re
import logging
import pyark.cva_client as cva_client
from pyark.models.wrappers import VariantWrapper
from protocols.protocol_7_2.cva import VariantCoordinates


_singleton_instance = None


# NOTE: this method needs to be out of any class as it needs to be pickled (ie: serialised) by multiprocessing library
def _get_variant_by_id(identifier):
    return identifier, _singleton_instance.get_variant_by_id(identifier)


class VariantsClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "variants"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def count(self, **params):
        return self.get_variants(count=True, **params)

    def get_variant_by_id(self, identifier):
        """
        :type identifier: str
        :rtype: VariantWrapper
        """
        results, _ = self._get("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=identifier))
        if not results:
            logging.warning("No variant found with id {}".format(identifier))
            return None
        assert len(results) == 1, "Unexpected number of variants returned when searching by identifier"
        variant = VariantWrapper.fromJsonDict(results[0])
        return variant

    def get_variants_by_id(self, identifiers):
        """
        :type identifiers: list
        :rtype: dict
        """
        self._set_singleton()
        return VariantsClient.run_parallel_requests(_get_variant_by_id, identifiers)

    def get_variants(self, as_data_frame=False, max=None, **params):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            return results[0]
        else:
            return self._paginate(endpoint=self._BASE_ENDPOINT, as_data_frame=as_data_frame, max=max, **params)

    def variant_ids_to_coordinates(self, variant_ids, fail_on_structural=False):
        return list(filter(lambda x: x is not None,
                           [self.variant_id_to_coordinates(v, fail_on_structural) for v in variant_ids]))

    def variant_id_to_coordinates(self, variant_id, fail_on_structural=False):
        """
        :type variant_id: str
        :type fail_on_structural: bool
        :rtype: VariantCoordinates
        """
        match = re.match(r'(GRCh37|GRCh38):(.+):([ 0-9]+):(-| |[A|C|G|T]*):(-| |[A|C|G|T]*)', variant_id)
        if match and (len(match.group(4)) > 0 or len(match.group(5)) > 0):
            variant_coordinates = VariantCoordinates.fromJsonDict({
                'assembly': match.group(1),
                'chromosome': match.group(2),
                'position': match.group(3).strip(),
                'reference': match.group(4),
                'alternate': match.group(5)
            })
        else:
            variant = self.get_variant_by_id(variant_id)
            if variant is None:
                raise ValueError("The variant id {} could not be mapped".format(variant_id))
            variant_representation = variant.get_default_variant_representation()
            variant_coordinates = variant_representation.smallVariantCoordinates
            if variant_coordinates is None:
                if fail_on_structural:
                    raise ValueError("The variant id {} does not correspond to a small variant".format(variant_id))
                else:
                    return None
        return variant_coordinates

    def _set_singleton(self):
        global _singleton_instance
        _singleton_instance = self
