import re
from protocols.protocol_7_2.cva import Variant, Assembly, VariantRepresentation, VariantAnnotation


class VariantWrapper(Variant):

    def get_variant_representation_by_assembly(self, assembly):
        """
        :type assembly: Assembly
        :rtype: VariantRepresentation
        """
        for v in self.variants:
            if v.assembly == assembly:
                return v
        return None

    def get_default_variant_representation(self):
        """
        :rtype: VariantRepresentation
        """
        variant_representation = self.get_variant_representation_by_assembly(Assembly.GRCh38)
        if not variant_representation:
            variant_representation = self.get_variant_representation_by_assembly(Assembly.GRCh37)
        return variant_representation

    def get_variant_annotation_by_assembly(self, assembly):
        """
        :type assembly: Assembly
        :rtype: VariantAnnotationWrapper
        """
        variant_representation = self.get_variant_representation_by_assembly(assembly)
        return VariantAnnotationWrapper.fromJsonDict(variant_representation.annotation.toJsonDict())

    def get_default_variant_annotation(self):
        """
        :rtype: VariantAnnotationWrapper
        """
        variant_representation = self.get_default_variant_representation()
        return VariantAnnotationWrapper.fromJsonDict(variant_representation.annotation.toJsonDict())

    @staticmethod
    def is_small_variant(variant_id):
        fields = variant_id.split(':')
        seq_re = re.compile("^[ACGT]*$")
        return seq_re.match(fields[3]) and seq_re.match(fields[4])


class VariantAnnotationWrapper(VariantAnnotation):

    def get_max_allele_frequency(self):
        if not self.populationFrequencies:
            return 0.0
        return max([freq.altAlleleFreq for freq in self.populationFrequencies])
