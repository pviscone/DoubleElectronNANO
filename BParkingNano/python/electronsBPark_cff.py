import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.electrons_cff import *
from PhysicsTools.NanoAOD.lowPtElectrons_cff import *

# Electron ID MVA raw values
mvaConfigsForEleProducer = cms.VPSet()
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff \
    import mvaEleID_Fall17_noIso_V2_producer_config
from PhysicsTools.BParkingNano.mvaElectronID_BParkRetrain_cff \
    import mvaEleID_BParkRetrain_producer_config
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_noIso_V1_cff \
    import mvaEleID_RunIIIWinter22_noIso_V1_producer_config

mvaConfigsForEleProducer.append( mvaEleID_Fall17_noIso_V2_producer_config )
mvaConfigsForEleProducer.append( mvaEleID_BParkRetrain_producer_config )
mvaConfigsForEleProducer.append( mvaEleID_RunIIIWinter22_noIso_V1_producer_config )

# evaluate MVA IDs
electronMVAValueMapProducer = cms.EDProducer(
    'ElectronMVAValueMapProducer',
    src = cms.InputTag('slimmedElectrons'),#,processName=cms.InputTag.skipCurrentProcess()),
    mvaConfigurations = mvaConfigsForEleProducer,
)

# Compute WPs
egmGsfElectronIDs = cms.EDProducer(
    "VersionedGsfElectronIdProducer",
    physicsObjectSrc = cms.InputTag('slimmedElectrons'),
    physicsObjectIDs = cms.VPSet( )
)

from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupVIDSelection
my_id_modules = [
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_noIso_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
    'PhysicsTools.BParkingNano.mvaElectronID_BParkRetrain_cff'
]
for id_module_name in my_id_modules: 
    idmod= __import__(id_module_name, globals(), locals(), ['idName','cutFlow'])
    for name in dir(idmod):
        item = getattr(idmod,name)
        if hasattr(item,'idName') and hasattr(item,'cutFlow'):
            setupVIDSelection(egmGsfElectronIDs, item)

# compute electron seed gain
seedGainElePF = cms.EDProducer("ElectronSeedGainProducer", src = cms.InputTag("slimmedElectrons"))
seedGainEleLowPt = cms.EDProducer("ElectronSeedGainProducer", src = cms.InputTag("updatedLowPtElectrons"))

# embed IDs and additional variables in slimmedElectrons collection
slimmedPFElectronsWithUserData = cms.EDProducer("PATElectronUserDataEmbedder",
    src = cms.InputTag("slimmedElectrons"),
    userFloats = cms.PSet(
        pfmvaId = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2BParkRetrainRawValues"),
        pfmvaId_Run2 = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2RawValues"),
        pfmvaId_Run3 = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2RunIIIWinter22NoIsoV1RawValues"),
    ),
    userIntFromBools = cms.PSet(
        PFEleMvaID_Winter22NoIsoV1wp90 = cms.InputTag("egmGsfElectronIDs:mvaEleID-RunIIIWinter22-noIso-V1-wp90"),
        PFEleMvaID_Winter22NoIsoV1wp80 = cms.InputTag("egmGsfElectronIDs:mvaEleID-RunIIIWinter22-noIso-V1-wp80")
        # other ones are already embedded in slimmedElectrons for both 2022/23
    ),
    userInts = cms.PSet(
        seedGain = cms.InputTag("seedGainElePF"),
    )
)

slimmedLowPtElectronsWithUserData = cms.EDProducer("PATElectronUserDataEmbedder",
    src = cms.InputTag("updatedLowPtElectrons"),
    userInts = cms.PSet(
        seedGain = cms.InputTag("seedGainEleLowPt"),
    ),
)


#Everything can be done here, in one loop and save time :)
electronsForAnalysis = cms.EDProducer(
  'ElectronMerger',
  trgLepton = cms.InputTag('electronTrgSelector:trgElectrons'),
  trgObjects = cms.InputTag('slimmedPatTrigger'),
  trgBits = cms.InputTag("TriggerResults","","HLT"),
  # lowptSrc = cms.InputTag('slimmedLowPtElectrons'), # Only used if saveLowPtE == True
  lowptSrc = cms.InputTag('slimmedLowPtElectronsWithUserData'), # Only used if saveLowPtE == True
  # pfSrc    = cms.InputTag('slimmedElectrons'),
  pfSrc    = cms.InputTag('slimmedPFElectronsWithUserData'),
  rho_PFIso = cms.InputTag("fixedGridRhoFastjetAll"),
  EAFile_PFIso = cms.FileInPath("RecoEgamma/ElectronIdentification/data/Run3_Winter22/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_122X.txt"),
  # pfmvaId = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2BParkRetrainRawValues"),
  # pfmvaId_Run2 = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2RawValues"),
  # pfmvaId_Run3 = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2RunIIIWinter22NoIsoV1RawValues"),
  pfmvaId = cms.InputTag(""), #use embedded values
  pfmvaId_Run2 = cms.InputTag(""), #use embedded values
  pfmvaId_Run3 = cms.InputTag(""), #use embedded values
  vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
  ## cleaning wrt trigger lepton [-1 == no cut] 
  drForCleaning_wrtTrgLepton = cms.double(-1), # do not check for dR matching to trg objs
  dzForCleaning_wrtTrgLepton = cms.double(1.),
  ## trigger matching parameter
  drMaxTrgMatching = cms.double(0.3),
  ## cleaning between pfEle and lowPtGsf
  drForCleaning = cms.double(0.05),
  dzForCleaning = cms.double(0.5), ##keep tighter dZ to check overlap of pfEle with lowPt (?)
  ## true = flag and clean; false = only flag
  flagAndclean = cms.bool(False),
  pf_ptMin = cms.double(1.),
  ptMin = cms.double(0.5),
  etaMax = cms.double(2.5),
  bdtMin = cms.double(-100.), # Open this up and rely on L/M/T WPs. was -2.5, this cut can be used to deactivate low pT e if set to >12
  useRegressionModeForP4 = cms.bool(False),
  useGsfModeForP4 = cms.bool(False), # If False, use REGRESSED energy for both PF and LowPt eles; else, use GSF (track) energy
  sortOutputCollections = cms.bool(True),
  saveLowPtE = cms.bool(True), # Use low-pT eles
  filterEle = cms.bool(True),
  # conversions
  conversions = cms.InputTag('gsfTracksOpenConversions:gsfTracksOpenConversions'),
  beamSpot = cms.InputTag("offlineBeamSpot"),
  addUserVarsExtra = cms.bool(False),
)
#cuts minimun number in B both mu and e, min number of trg, dz electron, dz and dr track, 
countTrgElectrons = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("electronTrgSelector", "trgElectrons")
)

electronBParkTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
 src = cms.InputTag("electronsForAnalysis:SelectedElectrons"),
 cut = cms.string(""),
    name= cms.string("Electron"),
    doc = cms.string("slimmedElectrons for BPark after basic selection"),
    singleton = cms.bool(False),
    extension = cms.bool(False),
    variables = cms.PSet(P4Vars,
        pdgId  = Var("pdgId", int, doc="PDG code assigned by the event reconstruction (not by MC truth)"),
        charge = Var("userFloat('chargeMode')", int, doc="electric charge from pfEle or chargeMode for lowPtGsf"),
        dz = Var("dB('PVDZ')",float,doc="dz (with sign) wrt first PV, in cm",precision=10),
        dzErr = Var("abs(edB('PVDZ'))",float,doc="dz uncertainty, in cm",precision=6),
        dxy = Var("dB('PV2D')",float,doc="dxy (with sign) wrt first PV, in cm",precision=10),
        dxyErr = Var("edB('PV2D')",float,doc="dxy uncertainty, in cm",precision=6),
        vx = Var("vx()",float,doc="x coordinate of vertex position, in cm",precision=6),
        vy = Var("vy()",float,doc="y coordinate of vertex position, in cm",precision=6),
        vz = Var("vz()",float,doc="z coordinate of vertex position, in cm",precision=6),
        dzTrg = Var("userFloat('dzTrg')",float,doc="dz from the corresponding triggered lepton, in cm",precision=10),
        ip3d = Var("abs(dB('PV3D'))",float,doc="3D impact parameter wrt first PV, in cm",precision=10),
        sip3d = Var("abs(dB('PV3D')/edB('PV3D'))",float,doc="3D impact parameter significance wrt first PV, in cm",precision=10),
        preRegEnergy = Var("superCluster().rawEnergy()",float,doc="energy before correction",precision=10),
        trackPt = Var("gsfTrack().ptMode()",float,doc="pt of the gsf track", precision=10),
        correctedEnergy = Var("correctedEcalEnergy()",float,doc="energy after correction",precision=10),
        # regressedEnergy = Var("ecalTrackRegressionEnergy()",float,doc="energy after regression",precision=10),

        # START MVA ID input variabiles (from RecoEgamma/ElectronIdentification/data/ElectronIDVariablesRun3.txt)
        deltaEtaSC = Var("superCluster().eta()-eta()",float,doc="delta eta (SC,ele) with sign",precision=10),
        sigmaietaieta = Var("full5x5_sigmaIetaIeta()",float,doc="sigma_IetaIeta of the supercluster, calculated with full 5x5 region",precision=10),
        sigmaiphiiphi = Var("full5x5_sigmaIphiIphi()",float,doc="sigma_IphiIphi of the supercluster, calculated with full 5x5 region",precision=10),
        circularity = Var("1.-full5x5_e1x5()/full5x5_e5x5()",float,doc="circularity of the supercluster",precision=10),
        r9 = Var("full5x5_r9()",float,doc="R9 of the supercluster, calculated with full 5x5 region",precision=10),
        scletawidth = Var("superCluster().etaWidth()",float,doc="width of the supercluster in eta",precision=10),
        sclphiwidth = Var("superCluster().phiWidth()",float,doc="width of the supercluster in phi",precision=10),
        hoe = Var("full5x5_hcalOverEcal()",float,doc="H/E of the supercluster, calculated with full 5x5 region",precision=10),
        kfhits = Var("closestCtfTrackNLayers()",int,doc="number of missing hits in the inner tracker"),
        kfchi2 = Var("closestCtfTrackNormChi2()",float,doc="normalized chi2 of the closest CTF track"),
        gsfchi2 = Var("gsfTrack().normalizedChi2()",int,doc="number of missing hits in the inner tracker"),
        fBrem = Var("fbrem()",float,doc="brem fraction from the gsf fit",precision=12),
        gsfhits = Var("gsfTrack().hitPattern().trackerLayersWithMeasurement()",int,doc="number of missing hits in the inner tracker"),
        expected_inner_hits = Var("gsfTrack().hitPattern().numberOfLostHits('MISSING_INNER_HITS')",int,doc="number of missing hits in the inner tracker"),
        conversionVertexFitProbability = Var("convVtxFitProb()",float,doc="conversion vertex fit probability"),
        eoverp = Var("eSuperClusterOverP()",float,doc="E/P of the electron",precision=10),
        eeleoverpout = Var("eEleClusterOverPout()",float,doc="E/E_{SC} of the electron",precision=10),
        IoEmIop = Var("1.0/ecalEnergy()-1.0/trackMomentumAtVtx().R()",float,doc="1/E - 1/P of the electron",precision=10),
        deltaetain = Var("abs(deltaEtaSuperClusterTrackAtVtx())",float,doc="delta eta (SC,track) with sign",precision=10),
        deltaphiin = Var("abs(deltaPhiSuperClusterTrackAtVtx())",float,doc="delta phi (SC,track) with sign",precision=10),
        deltaetaseed = Var("abs(deltaEtaSeedClusterTrackAtCalo())",float,doc="delta eta (seed,track) with sign",precision=10),
        psOverEraw = Var("superCluster().preshowerEnergy()/superCluster().rawEnergy()",float,doc="preshower energy over raw ECAL energy",precision=10),

        pfIso03_chg = Var("pfIsolationVariables().sumChargedHadronPt()",float,doc="PF absolute isolation dR=0.3, charged component",precision=10),
        pfIso03_chg_corr = Var("userFloat('PFIsoChg03_corr')",float,doc="corrected PF absolute isolation dR=0.3, charged component",precision=10),
        pfIso03_neu = Var("pfIsolationVariables().sumNeutralHadronEt()",float,doc="PF absolute isolation dR=0.3, neutral component",precision=10),
        pfIso03_all = Var("userFloat('PFIsoAll03')",float,doc="PF absolute isolation dR=0.3, total (with rho*EA PU Winter22V1 corrections)"),
        pfIso03_all_corr = Var("userFloat('PFIsoAll03_corr')",float,doc="corrected PF absolute isolation dR=0.3, total (with rho*EA PU Winter22V1 corrections)"),
        pfIso04_chg = Var("chargedHadronIso()",float,doc="PF absolute isolation dR=0.4, charged component"),
        pfIso04_chg_corr = Var("userFloat('PFIsoChg04_corr')",float,doc="corrected PF absolute isolation dR=0.4, charged component",precision=10),
        pfIso04_neu = Var("neutralHadronIso()",float,doc="PF absolute isolation dR=0.4, neutral component"),
        pfIso04_all = Var("userFloat('PFIsoAll04')",float,doc="PF absolute isolation dR=0.4, total (with rho*EA PU Winter22V1 corrections)"),
        pfIso04_all_corr = Var("userFloat('PFIsoAll04_corr')",float,doc="corrected PF absolute isolation dR=0.4, total (with rho*EA PU Winter22V1 corrections)"),
        ctfTrackPt = Var("?closestCtfTrackRef().isNonnull()?closestCtfTrackRef().pt():0",float,doc=""),
        ctfTrackEta = Var("?closestCtfTrackRef().isNonnull()?closestCtfTrackRef().eta():0",float,doc=""),
        ctfTrackPhi = Var("?closestCtfTrackRef().isNonnull()?closestCtfTrackRef().phi():0",float,doc=""),

        ecalPFclusterIso = Var("ecalPFClusterIso()",float,doc="sum of PF clusters in isolation cone",precision=10),
        hcalPFclusterIso = Var("hcalPFClusterIso()",float,doc="sum of PF clusters in isolation cone",precision=10),
        dr03TkSumPt = Var("dr03TkSumPt()",float,doc="sum of tracks in isolation cone",precision=10),
        # END MVA input variables

        # START Scale and smearing inputs
        seedGain = Var("userInt('seedGain')", int, doc="Gain of the seed crystal"),
        # END Scale and smearing inputs

        tightCharge = Var("isGsfCtfScPixChargeConsistent() + isGsfScPixChargeConsistent()",int,doc="Tight charge criteria (0:none, 1:isGsfScPixChargeConsistent, 2:isGsfCtfScPixChargeConsistent)"),
        convVeto = Var("passConversionVeto()",bool,doc="pass conversion veto"),
#        lostHits = Var("gsfTrack.hitPattern.numberOfLostHits('MISSING_INNER_HITS')","uint8",doc="number of missing inner hits"),
        trkRelIso = Var("trackIso/pt",float,doc="PF relative isolation dR=0.3, total (deltaBeta corrections)"),
        isPF = Var("userInt('isPF')",bool,doc="electron is PF candidate"),
        isLowPt = Var("userInt('isLowPt')",bool,doc="electron is LowPt candidate"),
        LPEleSeed_Fall17PtBiasedV1RawValue = Var("userFloat('LPEleSeed_Fall17PtBiasedV1RawValue')",float,doc="Seed BDT for low-pT electrons, Fall17 ptBiased model"), #@@ was called "ptBiased"
        LPEleSeed_Fall17UnBiasedV1RawValue = Var("userFloat('LPEleSeed_Fall17UnBiasedV1RawValue')",float,doc="Seed BDT for low-pT electrons, Fall17 unBiased model"), #@@ was called "unBiased"
        LPEleMvaID_2020Sept15RawValue = Var("userFloat('LPEleMvaID_2020Sept15RawValue')",float,doc="MVA ID for low-pT electrons, 2020Sept15 model"), #@@ was called "mvaId"
        PFEleMvaID_RetrainedRawValue = Var("userFloat('PFEleMvaID_RetrainedRawValue')",float,doc="MVA ID for PF electrons, BParkRetrainRawValues"), #@@ was called "pfmvaId"
        
        PFEleMvaID_Fall17NoIsoV2RawValue = Var("userFloat('PFEleMvaID_Fall17NoIsoV2RawValue')",float,doc="MVA ID for PF electrons, Fall17NoIsoV2RawValues"),
        PFEleMvaID_Fall17NoIsoV1wpLoose = Var("userInt('PFEleMvaID_Fall17NoIsoV1wpLoose')",bool,doc="MVA ID for PF electrons, mvaEleID-Fall17-noIso-V1-wpLoose"), #@@ to be deprecated
        PFEleMvaID_Fall17NoIsoV2wpLoose = Var("userInt('PFEleMvaID_Fall17NoIsoV2wpLoose')",bool,doc="MVA ID for PF electrons, mvaEleID-Fall17-noIso-V2-wpLoose"),
        PFEleMvaID_Fall17NoIsoV2wp90 = Var("userInt('PFEleMvaID_Fall17NoIsoV2wp90')",bool,doc="MVA ID for PF electrons, mvaEleID-Fall17-noIso-V2-wp90"),
        PFEleMvaID_Fall17NoIsoV2wp80 = Var("userInt('PFEleMvaID_Fall17NoIsoV2wp80')",bool,doc="MVA ID for PF electrons, mvaEleID-Fall17-noIso-V2-wp80"),
        
        PFEleMvaID_Winter22NoIsoV1RawValue = Var("userFloat('PFEleMvaID_Winter22NoIsoV1RawValue')",float,doc="MVA ID for PF electrons: RunIIIWinter22NoIsoV1RawValues"),
        PFEleMvaID_Winter22NoIsoV1wp90 = Var("userInt('PFEleMvaID_Winter22NoIsoV1wp90')",bool,doc="MVA ID for PF electrons, mvaEleID-RunIIIWinter22-noIso-V1-wp90"),
        PFEleMvaID_Winter22NoIsoV1wp80 = Var("userInt('PFEleMvaID_Winter22NoIsoV1wp80')",bool,doc="MVA ID for PF electrons, mvaEleID-RunIIIWinter22-noIso-V1-wp80"),

        isTriggering = Var("userInt('isTriggering')",int,doc="Is ele triggering?"),
        drTrg = Var("userFloat('drTrg')",float,doc="dR to the triggering lepton"),

        isPFoverlap = Var("userInt('isPFoverlap')",bool,doc="flag lowPt ele overlapping with pf in selected_pf_collection", precision=8),
        convOpen = Var("userInt('convOpen')",bool,doc="Matched to a conversion in gsfTracksOpenConversions collection"),
        convLoose = Var("userInt('convLoose')",bool,doc="Matched to a conversion satisfying Loose WP (see code)"),
        convTight = Var("userInt('convTight')",bool,doc="Matched to a conversion satisfying Tight WP (see code)"),
        convLead = Var("userInt('convLead')",bool,doc="Matched to leading track from conversion"),
        convTrail = Var("userInt('convTrail')",bool,doc="Matched to trailing track from conversion"),
        convExtra = Var("userInt('convExtra')",bool,doc="Flag to indicate if all conversion variables are stored"),
        skipEle = Var("userInt('skipEle')",bool,doc="Is ele skipped (due to small dR or large dZ w.r.t. trigger)?"),
        )
)

if electronsForAnalysis.addUserVarsExtra : 
    electronBParkTable.variables = cms.PSet(
        electronBParkTable.variables,
        convValid = Var("userInt('convValid')",bool,doc="Valid conversion"),
        convChi2Prob = Var("userFloat('convChi2Prob')",float,doc="Reduced chi2 for conversion vertex fit"),
        convQualityHighPurity = Var("userInt('convQualityHighPurity')",bool,doc="'High purity' quality flag for conversion"),
        convQualityHighEff = Var("userInt('convQualityHighEff')",bool,doc="'High efficiency' quality flag for conversion"),
        convTracksN = Var("userInt('convTracksN')",int,doc="Number of tracks associated with conversion"),
        convMinTrkPt = Var("userFloat('convMinTrkPt')",float,doc="Minimum pT found for tracks associated with conversion"),
        convLeadIdx = Var("userInt('convLeadIdx')",int,doc="Index of leading track"),
        convTrailIdx = Var("userInt('convTrailIdx')",int,doc="Index of trailing track"),
        convLxy = Var("userFloat('convLxy')",float,doc="Transverse position of conversion vertex"),
        convVtxRadius = Var("userFloat('convVtxRadius')",float,doc="Radius of conversion vertex"),
        convMass = Var("userFloat('convMass')",float,doc="Invariant mass from conversion pair"),
        convMassFromPin = Var("userFloat('convMassFromPin')",float,doc="Invariant mass from inner momeuntum of conversion pair"),
        convMassBeforeFit = Var("userFloat('convMassBeforeFit')",float,doc="Invariant mass from conversion pair before fit"),
        convMassAfterFit = Var("userFloat('convMassAfterFit')",float,doc="Invariant mass from conversion pair after fit"),
        convLeadNHitsBeforeVtx = Var("userInt('convLeadNHitsBeforeVtx')",int,doc="Number of hits before vertex for lead track"),
        convTrailNHitsBeforeVtx = Var("userInt('convTrailNHitsBeforeVtx')",int,doc="Number of hits before vertex for trail track"),
        convMaxNHitsBeforeVtx = Var("userInt('convMaxNHitsBeforeVtx')",int,doc="Maximum number of hits per track before vertex"),
        convSumNHitsBeforeVtx = Var("userInt('convSumNHitsBeforeVtx')",int,doc="Summed number of hits over tracks before vertex"),
        convDeltaExpectedNHitsInner = Var("userInt('convDeltaExpectedNHitsInner')",int,doc="Delta number of expected hits before vertex"),
        convDeltaCotFromPin = Var("userFloat('convDeltaCotFromPin')",float,doc="Delta cotangent theta from inner momenta"),
    )
    
electronsBParkMCMatchForTable = cms.EDProducer("MCMatcher",  # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src         = electronBParkTable.src,                 # final reco collection
    matched     = cms.InputTag("finalGenParticlesBPark"), # final mc-truth particle collection
    mcPdgId     = cms.vint32(11,22),                 # one or more PDG ID (11 = el, 22 = pho); absolute values (see below)
    checkCharge = cms.bool(False),              # True = require RECO and MC objects to have the same charge  
    mcStatus    = cms.vint32(1),                # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
    maxDeltaR   = cms.double(0.03),             # Minimum deltaR for the match
    maxDPtRel   = cms.double(0.5),              # Minimum deltaPt/Pt for the match
    resolveAmbiguities    = cms.bool(False),    # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(True),    # False = just match input in order; True = pick lowest deltaR pair first
    
)

selectedElectronsMCMatchEmbedded = cms.EDProducer(
    'ElectronMatchEmbedder',
    src = electronBParkTable.src,
    matching = cms.InputTag('electronsBParkMCMatchForTable')
)

electronBParkMCTable = cms.EDProducer("CandMCMatchTableProducerBPark",
    src     = electronBParkTable.src,
    mcMap   = cms.InputTag("electronsBParkMCMatchForTable"),
    objName = electronBParkTable.name,
    objType = electronBParkTable.name,
    branchName = cms.string("genPart"),
    docString = cms.string("MC matching to status==1 electrons or photons"),
)
    
electronsBParkSequence = cms.Sequence(
    modifiedLowPtElectrons +
    updatedLowPtElectrons +
    electronMVAValueMapProducer +
    egmGsfElectronIDs +
    seedGainElePF +
    seedGainEleLowPt +
    slimmedPFElectronsWithUserData +
    slimmedLowPtElectronsWithUserData +
    electronsForAnalysis
)

electronBParkMC = cms.Sequence(electronsBParkSequence + electronsBParkMCMatchForTable + selectedElectronsMCMatchEmbedded + electronBParkMCTable)
electronBParkTables = cms.Sequence(electronBParkTable)

###########
# Modifiers
###########

# from PhysicsTools.BParkingNano.modifiers_cff import *

# DiEle.toModify(electronsForAnalysis, ...)