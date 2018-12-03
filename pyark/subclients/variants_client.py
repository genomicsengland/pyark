import pyark.cva_client as cva_client
from protocols.protocol_7_0.cva import Variant
import logging


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
        :rtype: Variant
        """
        results, _ = self._get("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=identifier))
        if not results:
            logging.warning("No variant found with id {}".format(identifier))
            return None
        assert len(results) == 1, "Unexpected number of variants returned when searching by identifier"
        variant = Variant.fromJsonDict(results[0])
        return variant

    def get_variants_by_id(self, identifiers):
        """
        :type identifiers: list
        :rtype: dict
        """
        self._set_singleton()
        return VariantsClient.run_parallel_requests(_get_variant_by_id, identifiers)

    def get_variants(self, as_data_frame=False, **params):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            return results[0]
        else:
            return self._paginate(endpoint=self._BASE_ENDPOINT, params=params, as_data_frame=as_data_frame)

    def _set_singleton(self):
        global _singleton_instance
        _singleton_instance = self
