from FWCore.ParameterSet.VarParsing import VarParsing
import FWCore.ParameterSet.Config as cms

options = VarParsing('python')

options.register('is22', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on 2022 data (else 23) if Run3"
)

options.register('isMC', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)

options.register('isSignal', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on signal MC (else J/psi)")

options.register('globalTag', 'NOTSET',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Set global tag"
)
options.register('wantSummary', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)
options.register('wantFullRECO', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)
options.register('reportEvery', 10,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "report every N events"
)
options.register('skip', 0,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "skip first N events"
)
options.register('lhcRun', 3,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "LHC Run 2 or 3 (default)"
)

options.setDefault('maxEvents', 1000)
options.setDefault('tag', '124X')
options.parseArguments()
print(options)

globaltag = None

if options.lhcRun == 3:
    # globaltag = '124X_mcRun3_2022_realistic_postEE_v1' if options.isMC else '124X_dataRun3_Prompt_v4'
    if options.is22:
        globaltag = '124X_mcRun3_2022_realistic_postEE_v1' if options.isMC else '124X_dataRun3_v15'
    else:
        globaltag = "130X_mcRun3_2023_realistic_v14" if options.isMC else "130X_dataRun3_PromptAnalysis_v1"
elif options.lhcRun == 2: globaltag = '102X_upgrade2018_realistic_v15' if options.isMC else '102X_dataRun2_v11'

if options._beenSet['globalTag']: globaltag = options.globalTag

print("Using global tag ", globaltag)

ext1 = {2:'Run2', 3:'Run3'}
ext2 = {False:'data', True:'mc'}
ext3 = {False:'23', True:'22'}
outputFileNANO = cms.untracked.string('_'.join(['BParkingNANO',
                                                ext1[options.lhcRun],
                                                ext3[options.is22],
                                                ext2[options.isMC],
                                                options.tag])+'.root')
outputFileFEVT = cms.untracked.string('_'.join(['BParkingFullEvt',
                                                ext1[options.lhcRun],
                                                ext3[options.is22],
                                                ext2[options.isMC],
                                                options.tag])+'.root')
if not options.inputFiles:
    if options.lhcRun == 2:
        options.inputFiles = [
            'file:///eos/cms/store/cmst3/group/bpark/BToKmumu_1000Events_MINIAOD.root'
        ] if options.isMC else [
            'root://cms-xrd-global.cern.ch//store/data/Run2018B/ParkingBPH4/MINIAOD/05May2019-v2/230000/6B5A24B1-0E6E-504B-8331-BD899EB60110.root'
        ]
    elif options.lhcRun == 3:
        if options.is22:
            options.inputFiles = [
                # # original
                # 'root://cms-xrd-global.cern.ch//store/user/jodedra/BuTOjpsiKEE20221103FIFTYMminiaod/BuTOjpsiKEE20221103FIFTYM/SUMMER22_MINIAOD/221106_001759/0000/step1_inMINIAODSIM_1.root', #4481 events

                # DARK PHOTON SAMPLES
                'root://cmsxrootd.fnal.gov///store/user/marlow/EtaToGammaTM_TMToEE_2022/EtaToGammaTM_TMToEE_2022_MINIAOD_388.root', #1000 events
                'root://cmsxrootd.fnal.gov///store/user/marlow/EtaToGammaTM_TMToEE_2022/EtaToGammaTM_TMToEE_2022_MINIAOD_828.root',
                'root://cmsxrootd.fnal.gov///store/user/marlow/EtaToGammaTM_TMToEE_2022/EtaToGammaTM_TMToEE_2022_MINIAOD_60.root',
                'root://cmsxrootd.fnal.gov///store/user/marlow/EtaToGammaTM_TMToEE_2022/EtaToGammaTM_TMToEE_2022_MINIAOD_19.root',
            ] if options.isMC and options.isSignal else [
                # central BuToKJpsi_JPsiToEE (should be similar), mini v1 bc of CMSSW compatibility reasons
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/0cc74dad-0a95-430d-82f1-113feb060680.root',            
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/79ca5368-3191-42f6-877d-28760fbae9d8.root',
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/904980f9-5a94-493d-8e6c-3673b289ca30.root',
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/adc7d31b-a38b-41a1-8df9-e71e0a7e1d40.root',
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/04603ab0-8eff-4d59-bccb-bb3e9c64e4a5.root',
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/358618a8-9aad-4283-8249-e1fb48354c73.root',
                # 'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv3/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2550000/9eafc8d8-d627-486d-a137-9931cd54f7f8.root',

                # central BuToKJpsi_JPsiToEE (should be similar), mini v4 2022
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/aeb83042-4174-49e8-8d7e-3f4acfff0a13.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/f6f9d6d6-ecff-47a6-9d9c-f0be003d99b8.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/0c772889-596b-4358-aeef-8cef53dfe216.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/1223aeb1-1145-4a07-93ae-8ce5d5dd77dd.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/4419ecf7-7341-4ad6-93f4-b81836d720bc.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/51c6d170-57f6-43d7-b02e-90a7e4588c40.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/96034a2c-5973-4f12-bedc-9321b5d98922.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/3ec09a45-2061-4a0a-8487-55c54b5bbdb0.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/ed7056bc-537a-47ed-a742-4055fef38e94.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/8dfdf330-83f9-475a-b057-c405baf43d3d.root',
                'root://cmsxrootd.fnal.gov///store/mc/Run3Summer22EEMiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/60000/6db4a541-5fc9-4dbc-a799-d69a1be12d1f.root',
            ] if options.isMC else [
                # 2022C files
                'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleElectronLowMass0/MINIAOD/10Dec2022-v2/30000/3a970b47-04fe-4b41-b3d3-6bd4dc7b7281.root',
                'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleElectronLowMass0/MINIAOD/10Dec2022-v2/2560000/f0c41013-6a45-4f13-ad74-19de9c08c528.root',
                'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleElectronLowMass0/MINIAOD/10Dec2022-v2/2560000/182138bf-9146-4760-a86b-5dafb19dd740.root',
                'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleElectronLowMass0/MINIAOD/10Dec2022-v2/2560000/6f79c2b1-a34c-4d51-8576-a9313059d5c0.root',
                'root://xrootd-cms.infn.it///store/data/Run2022C/ParkingDoubleElectronLowMass0/MINIAOD/10Dec2022-v2/2560000/de22bdd5-19b0-4709-88fe-cc9c182597b5.root',
                # 'root://cms-xrd-global.cern.ch//store/data/Run2022C/ParkingDoubleElectronLowMass0/MINIAOD/PromptReco-v1/000/356/170/00000/45c0f2ed-eb5b-4292-abc8-3117424d9432.root'
            ]
        else:
            options.inputFiles = [
                # # Z' SAMPLES
                f'file:/eos/cms/store/group/phys_susy/SOS/DarkPhoton_130X_Run3/MINIAOD/HAHM_ZdToEE_M5/HAHM_ZdToEE_M5.job{i}.root' for i in range(30)
                # f'file:/eos/cms/store/group/phys_susy/SOS/DarkPhoton_130X_Run3/MINIAOD/HAHM_ZdToEE_M15/HAHM_ZdToEE_M15.job{i}.root' for i in range(30)
            ] if options.isMC and options.isSignal else [
                # central BuToKJpsi_JPsiToEE (should be similar), mini v4 2023
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/40000/bc890edb-7cd8-4416-8938-42710506e833.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/30000/0b8d58b6-fed7-4b68-9391-962bf73de310.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/621b77eb-3b4c-4360-a056-4838d45f3e6c.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/f71f3d75-cecb-4418-b04f-c7c0cab95334.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/d5abfef3-f02c-4e89-bbe1-66ca3961eabe.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/98b9286c-bf31-4678-86c1-739c249d3339.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/7c043b6f-4d22-4022-8a0b-445bcb9ca444.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/d955f561-8613-4600-896d-5d05feb499ad.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/074180a5-76f9-4e1b-a1ed-c58dd85a6d55.root',
                'root://xrootd-cms.infn.it///store/mc/Run3Summer23MiniAODv4/BuToKJPsi_JPsiToEE_SoftQCD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/a48687cb-7819-4e17-ad8b-e239729c7a40.root',
            ] if options.isMC else [
                # 2023C files
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/5050267e-e959-4aec-a51c-8725965c8598.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550001/fd2e547d-6ec2-46ff-b4dd-c9e8bc4f3a11.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/cc7a5cda-ba6e-4269-aa3f-4b73002b64c5.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/9f9ff739-9ac6-47f8-88a8-d1a79ef5bcf3.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/4e24d9ca-589f-4fce-aa44-21ca6c4b8985.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550001/78c4aaba-0fe7-4088-80d2-9bc5a3ca788d.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/83cd7f48-ebd1-4325-a8f2-af19d911de02.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/24f87d86-965d-4ff2-8396-a97d2c992369.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550000/037e1859-dbd8-4115-bfc1-957529813110.root',
                'root://xrootd-cms.infn.it///store/data/Run2023C/ParkingDoubleElectronLowMass/MINIAOD/22Sep2023_v4-v1/2550001/de4ec1b4-3abe-44c1-a525-793b73f22e2d.root',
            ]
annotation = '%s nevts:%d' % (outputFileNANO, options.maxEvents)

# Process   
from Configuration.StandardSequences.Eras import eras
from PhysicsTools.BParkingNano.modifiers_cff import *
process = None
if   options.lhcRun == 3: process = cms.Process('BParkNANO',eras.Run3,BToKEE_DiEle)
elif options.lhcRun == 2: process = cms.Process('BParkNANO',eras.Run2_2018)

# import of standard configurations
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('PhysicsTools.BParkingNano.nanoBPark_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
# process.MessageLogger.cerr.threshold = "DEBUG"
# process.MessageLogger.debugModules = ["*"]

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring(),
    skipEvents=cms.untracked.uint32(options.skip),
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(options.wantSummary),
)

process.nanoMetadata.strings.tag = annotation
# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string(annotation),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = outputFileFEVT,
    outputCommands = (cms.untracked.vstring('keep *',
                                            'drop *_*_SelectedTransient*_*',
                     )),
    splitLevel = cms.untracked.int32(0)
)

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = outputFileNANO,
    outputCommands = cms.untracked.vstring(
      'drop *',
      "keep nanoaodFlatTable_*Table_*_*",     # event data
      "keep nanoaodUniqueString_nanoMetadata_*_*",   # basic metadata
    )

)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, globaltag, '')

from PhysicsTools.BParkingNano.nanoBPark_cff import *
if options.lhcRun == 2:
    process = nanoAOD_customizeMuonTriggerBPark(process)
    process = nanoAOD_customizeElectronFilteredBPark(process)
    process = nanoAOD_customizeTrackFilteredBPark(process)
    process = nanoAOD_customizeBToKLL(process)
    process = nanoAOD_customizeBToKstarEE(process)
    process = nanoAOD_customizeBToKstarMuMu(process)
elif options.lhcRun == 3:
    from PhysicsTools.BParkingNano.electronsTrigger_cff import *
    process = nanoAOD_customizeDiEle(process)
    process = nanoAOD_customizeElectronFilteredBPark(process)
    process = nanoAOD_customizeTriggerBitsBPark(process)
    process = nanoAOD_customizeTrackFilteredBPark(process)
    process = nanoAOD_customizeDielectron(process)
    # process = nanoAOD_customizeBToKLL(process) #remove B, K reco -- only need dielectrons

# Path and EndPath definitions
if options.lhcRun == 2:
    process.nanoAOD_KMuMu_step = cms.Path(process.nanoSequence + process.nanoTracksSequence + process.nanoBKMuMuSequence + CountBToKmumu )
    process.nanoAOD_Kee_step   = cms.Path(process.nanoSequence + process.nanoTracksSequence + process.nanoBKeeSequence   + CountBToKee   )
    process.nanoAOD_KstarMuMu_step = cms.Path(process.nanoSequence + process.nanoTracksSequence + process.KstarToKPiSequence + process.nanoBKstarMuMuSequence + CountBToKstarMuMu )
    process.nanoAOD_KstarEE_step  = cms.Path(process.nanoSequence + process.nanoTracksSequence + process.KstarToKPiSequence + process.nanoBKstarEESequence + CountBToKstarEE  )
elif options.lhcRun == 3:
    process.nanoAOD_DiEle_step = cms.Path(process.nanoSequence
                                          +process.nanoDiEleSequence
                                          +process.nanoTracksSequence
                                          +process.nanoBKeeSequence)
                                        #   +CountBToKee)

# customisation of the process.
if options.isMC:
    from PhysicsTools.BParkingNano.nanoBPark_cff import nanoAOD_customizeMC
    nanoAOD_customizeMC(process)

process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
if options.lhcRun == 3:

    process.schedule = cms.Schedule(process.nanoAOD_DiEle_step,
                                    process.endjob_step,
                                    process.NANOAODoutput_step)
    if options.wantFullRECO:
        process.schedule = cms.Schedule(process.nanoAOD_DiEle_step,
                                        process.endjob_step,
                                        process.FEVTDEBUGHLToutput_step,
                                        process.NANOAODoutput_step)
    from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
    associatePatAlgosToolsTask(process)
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('nanoAOD_DiEle_step')
    )

elif options.lhcRun == 2:

    process.schedule = cms.Schedule(
        process.nanoAOD_KMuMu_step,
        process.nanoAOD_Kee_step,
        #process.nanoAOD_KstarMuMu_step,
        #process.nanoAOD_KstarEE_step,
        process.endjob_step,
        process.NANOAODoutput_step
    )
    if options.wantFullRECO:
        process.schedule = cms.Schedule(
            process.nanoAOD_KMuMu_step,
            process.nanoAOD_Kee_step,
            #process.nanoAOD_KstarMuMu_step,
            #process.nanoAOD_KstarEE_step,
            process.endjob_step,
            process.FEVTDEBUGHLToutput_step,
            process.NANOAODoutput_step
        )
    from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
    associatePatAlgosToolsTask(process)
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring(
            'nanoAOD_KMuMu_step',
            'nanoAOD_Kee_step',
            #'nanoAOD_KstarMuMu_step',
            #'nanoAOD_KstarEE_step',
        )
    )

### from https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3287/1/1/1/1/1.html
process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
process.NANOAODoutput.fakeNameForCrab=cms.untracked.bool(True)

process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
