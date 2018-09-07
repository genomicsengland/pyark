from pyark import cva_client
from protocols.cva_1_1_0 import (
    PedigreeInjectRD,
    CancerParticipantInject,
    InterpretedGenomeInject,
    ClinicalReportInject,
    ExitQuestionnaireInjectRD,
    ExitQuestionnaireInjectCancer
)


class DataIntakeClient(cva_client.CvaClient):

    _INTERPRETED_GENOME_POST = "interpreted-genomes"
    _CLINICAL_REPORT_POST = "clinical-reports"
    _EXIT_QUESTIONAIRES_RD_POST = "exit-questionnaires-rd"
    _EXIT_QUESTIONAIRES_CANCER_POST = "exit-questionnaires-cancer"
    _PEDIGREE_POST = "pedigrees"
    _PARTICIPANT_POST = "participants"

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
        :type participant: CancerParticipantInject
        :type params: dict
        :rtype: dict
        """
        return self._post(self._PARTICIPANT_POST, participant.toJsonDict(), params)

    def post_interpreted_genome(self, tiered_variant, params={}):
        """
        :type tiered_variant: InterpretedGenomeInject
        :type params: dict
        :rtype: dict
        """
        return self._post(self._INTERPRETED_GENOME_POST, tiered_variant.toJsonDict(), params)

    def post_clinical_report(self, candidate_variant, params={}):
        """
        :type candidate_variant: ClinicalReportInject
        :type params: dict
        :rtype: dict
        """
        return self._post(self._CLINICAL_REPORT_POST, candidate_variant.toJsonDict(), params)

    def post_exit_questionaire(self, exit_questionaire, params={}):
        """
        :type exit_questionaire: ExitQuestionnaireInjectRD
        :type params: dict
        :rtype: dict
        """
        return self._post(self._EXIT_QUESTIONAIRES_RD_POST, exit_questionaire.toJsonDict(), params)

    def post_exit_questionaire_cancer(self, exit_questionaire, params={}):
        """
        :type exit_questionaire: ExitQuestionnaireInjectCancer
        :type params: dict
        :rtype: dict
        """
        return self._post(self._EXIT_QUESTIONAIRES_CANCER_POST, exit_questionaire.toJsonDict(), params)