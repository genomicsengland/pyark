from pyark import cva_client
from protocols.cva_1_0_0 import PedigreeInjectRD, ParticipantInjectCancer, TieredVariantInjectRD, \
    CandidateVariantInjectRD, ReportedVariantInjectRD, ExitQuestionnaireInjectRD,  \
    TieredVariantInjectCancer, CandidateVariantInjectCancer, ReportedVariantInjectCancer, \
    ExitQuestionnaireInjectCancer


class DataIntakeClient(cva_client.CvaClient):

    _TIERED_VARIANT_RD_POST = "tiered-variants/rd"
    _CANDIDATE_VARIANT_RD_POST = "candidate-variants/rd"
    _REPORTED_VARIANT_RD_POST = "reported-variants/rd"
    _EXIT_QUESTIONAIRES_RD_POST = "exit-questionnaires/rd"
    _TIERED_VARIANT_CANCER_POST = "tiered-variants/cancer"
    _CANDIDATE_VARIANT_CANCER_POST = "candidate-variants/cancer"
    _REPORTED_VARIANT_CANCER_POST = "reported-variants/cancer"
    _EXIT_QUESTIONAIRES_CANCER_POST = "exit-questionnaires/cancer"
    _PEDIGREE_POST = "pedigrees"
    _PARTICIPANT_POST = "participants"

    # mocked data endpoints
    # _TIERED_VARIANTS_INJECT_RD = "mocked-data/rd/tiered-variant-inject"
    # _CANDIDATE_VARIANTS_INJECT_RD = "mocked-data/rd/candidate-variant-inject"
    # _REPORTED_VARIANTS_INJECT_RD = "mocked-data/rd/reported-variant-inject"
    # _TIERED_VARIANTS_INJECT_CANCER = "mocked-data/cancer/tiered-variant-inject"
    # _CANDIDATE_VARIANTS_INJECT_CANCER = "mocked-data/cancer/candidate-variant-inject"
    # _REPORTED_VARIANTS_INJECT_CANCER = "mocked-data/cancer/reported-variant-inject"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def post_pedigree(self, pedigree, params={}):
        """
        :type pedigree: PedigreeInjectRD
        :type params: dict
        :rtype: dict
        """
        return self._post(self._PEDIGREE_POST, pedigree.toJsonDict(), params)

    def post_participant(self, participant, params={}):
        """
        :type participant: ParticipantInjectCancer
        :type params: dict
        :rtype: dict
        """
        return self._post(self._PARTICIPANT_POST, participant.toJsonDict(), params)

    def post_tiered_variant(self, tiered_variant, params={}):
        """
        :type tiered_variant: TieredVariantInjectRD
        :type params: dict
        :rtype: dict
        """
        return self._post(self._TIERED_VARIANT_RD_POST, tiered_variant.toJsonDict(), params)

    def post_candidate_variant(self, candidate_variant, params={}):
        """
        :type candidate_variant: CandidateVariantInjectRD
        :type params: dict
        :rtype: dict
        """
        return self._post(self._CANDIDATE_VARIANT_RD_POST, candidate_variant.toJsonDict(), params)

    def post_exit_questionaire(self, exit_questionaire, params={}):
        """
        :type exit_questionaire: ExitQuestionnaireInjectRD
        :type params: dict
        :rtype: dict
        """
        return self._post(self._EXIT_QUESTIONAIRES_RD_POST, exit_questionaire.toJsonDict(), params)

    def post_reported_variant(self, reported_variant, params={}):
        """
        :type reported_variant: ReportedVariantInjectRD
        :type params: dict
        :rtype: dict
        """
        return self._post(self._REPORTED_VARIANT_RD_POST, reported_variant.toJsonDict(), params)

    def post_tiered_variant_cancer(self, tiered_variant, params={}):
        """
        :type tiered_variant: TieredVariantInjectCancer
        :type params: dict
        :rtype: dict
        """
        return self._post(self._TIERED_VARIANT_CANCER_POST, tiered_variant.toJsonDict(), params)

    def post_candidate_variant_cancer(self, candidate_variant, params={}):
        """
        :type candidate_variant: CandidateVariantInjectCancer
        :type params: dict
        :rtype: dict
        """
        return self._post(self._CANDIDATE_VARIANT_CANCER_POST, candidate_variant.toJsonDict(), params)

    def post_exit_questionaire_cancer(self, exit_questionaire, params={}):
        """
        :type exit_questionaire: ExitQuestionnaireInjectCancer
        :type params: dict
        :rtype: dict
        """
        return self._post(self._EXIT_QUESTIONAIRES_CANCER_POST, exit_questionaire.toJsonDict(), params)

    def post_reported_variant_cancer(self, reported_variant, params={}):
        """
        :type reported_variant: ReportedVariantInjectCancer
        :type params: dict
        :rtype: dict
        """
        return self._post(self._REPORTED_VARIANT_CANCER_POST, reported_variant.toJsonDict(), params)
