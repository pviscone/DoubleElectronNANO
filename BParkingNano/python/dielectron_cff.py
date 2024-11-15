import FWCore.ParameterSet.Config as cms
from PhysicsTools.BParkingNano.common_cff import *
from PhysicsTools.BParkingNano.electronsBPark_cff import electronsForAnalysis

electronPairs = cms.EDProducer(
    'DiElectronBuilder',
    src = cms.InputTag('electronsForAnalysis', 'SelectedElectrons'),
    transientTracksSrc = cms.InputTag('electronsForAnalysis', 'SelectedTransientElectrons'),
    lep1Selection = cms.string('pt > 1.3'),
    lep2Selection = cms.string(''),
    filterBySelection = cms.bool(True),
    preVtxSelection = cms.string(
        'abs(userCand("l1").vz - userCand("l2").vz) <= 1. && mass() < 6 '
        f'&& mass() > 0 && charge() == 0 && userFloat("lep_deltaR") > {electronsForAnalysis.drForCleaning} && userInt("nlowpt") < 3'  
    ),
    postVtxSelection = cms.string('userFloat("sv_chi2") < 998 && userFloat("sv_prob") > 1.e-5'),
)

electronPairsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag('electronPairs:SelectedDiLeptons'),
    cut = cms.string(""),
    name= cms.string("DiElectron"),
    doc = cms.string("SelectedElectron pairs for BPark with sucessful vertex fit"),
    singleton = cms.bool(False), 
    extension = cms.bool(False),                                                
    variables = cms.PSet(P4Vars,
        lep_deltaR = Var("userFloat('lep_deltaR')", float, doc="deltaR between the two leptons"),
        l1idx = Var("userInt('l1_idx')", int, doc="index of the first electron (leading)"),
        l2idx = Var("userInt('l2_idx')", int, doc="index of the second electron (subleading)"),
        l1_postfit_pt = Var("userFloat('l1_postfit_pt')", float, doc="pt of the first electron after vertexing"),
        l1_postfit_eta = Var("userFloat('l1_postfit_eta')", float, doc="eta of the first electron after vertexing"),
        l1_postfit_phi = Var("userFloat('l1_postfit_phi')", float, doc="phi of the first electron after vertexing"),
        l2_postfit_pt = Var("userFloat('l2_postfit_pt')", float, doc="pt of the second electron after vertexing"),
        l2_postfit_eta = Var("userFloat('l2_postfit_eta')", float, doc="eta of the second electron after vertexing"),
        l2_postfit_phi = Var("userFloat('l2_postfit_phi')", float, doc="phi of the second electron after vertexing"),
        nlowpt = Var("userInt('nlowpt')", int, doc="number of low pt electrons"),
        pre_vtx_sel = Var("userInt('pre_vtx_sel')", bool, doc="Satisfies pre-vertexing selections?"),
        sv_chi2 = Var("userFloat('sv_chi2')", float, doc="chi2 of the vertex fit"),
        sv_prob = Var("userFloat('sv_prob')", float, doc="probability of the vertex fit"),
        sv_ndof = Var("userFloat('sv_ndof')", float, doc="ndof of the vertex fit"),
        sv_x = Var("userFloat('sv_x')", float, doc="x position of the vertex fit"),
        sv_y = Var("userFloat('sv_y')", float, doc="y position of the vertex fit"),
        sv_z = Var("userFloat('sv_z')", float, doc="z position of the vertex fit"),
        fitted_mass = Var("userFloat('fitted_mass')", float, doc="fitted dielectron"),
        fitted_massErr = Var("userFloat('fitted_massErr')", float, doc="fitted dielectron mass error"),
        post_vtx_sel = Var("userInt('post_vtx_sel')", bool, doc="Satisfies post-vertexing selections?"),
        )
)

DiElectronSequence = cms.Sequence(
    electronPairs + 
    electronPairsTable
)


## MUONS
# (could be useful eventually)

# muonPairs = cms.EDProducer(
#     'DiMuonBuilder',
#     src = cms.InputTag('muonTrgSelector', 'SelectedMuons'),
#     transientTracksSrc = cms.InputTag('muonTrgSelector', 'SelectedTransientMuons'),
#     lep1Selection = cms.string('pt > 1.5'),
#     lep2Selection = cms.string(''),
#     filterBySelection = cms.bool(True),
#     preVtxSelection = cms.string('abs(userCand("l1").vz - userCand("l2").vz) <= 1. && mass() < 5 '
#                                  '&& mass() > 0 && charge() == 0 && userFloat("lep_deltaR") > 0.03'),
#     postVtxSelection = electronPairs.postVtxSelection,
# )
