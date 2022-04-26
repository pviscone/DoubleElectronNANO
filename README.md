# NanoAOD producer customized for BParking analyses 

The focus is on RK/K*/phi analyses.

## Recipe

Below is the original recipe for 10_2_X. To be updated ...

### Getting started

```shell
cmsrel CMSSW_10_2_15
cd CMSSW_10_2_15/src
cmsenv
git cms-init
```

### Add low-pT energy ID and regression

The ID model is `2020Sept15` (depth=15, ntrees=1000).

```shell
git cms-merge-topic -u CMSBParking:from-CMSSW_10_2_15_2020Sept15_v1
git clone --single-branch --branch from-CMSSW_10_2_15_2020Sept15 git@github.com:CMSBParking/RecoEgamma-ElectronIdentification.git $CMSSW_BASE/external/$SCRAM_ARCH/data/RecoEgamma/ElectronIdentification/data
```

To run on CRAB, the following three lines __must__ be executed:

```shell
git cms-addpkg RecoEgamma/ElectronIdentification
mkdir -p $CMSSW_BASE/src/RecoEgamma/ElectronIdentification/data/LowPtElectrons
cp $CMSSW_BASE/external/$SCRAM_ARCH/data/RecoEgamma/ElectronIdentification/data/LowPtElectrons/LowPtElectrons_ID_2020Sept15.root $CMSSW_BASE/src/RecoEgamma/ElectronIdentification/data/LowPtElectrons
```

### Add support for GBRForest to parse ROOT files

```shell
git cms-merge-topic -u CMSBParking:convertXMLToGBRForestROOT
```

### Add the modification needed to use post-fit quantities for electrons  

```shell
git cms-merge-topic -u CMSBParking:GsfTransientTracks # unsafe checkout (no checkdeps), but suggested here
```

### Add the modification needed to use the KinematicParticleVertexFitter  

```shell
git cms-merge-topic -u CMSBParking:fixKinParticleVtxFitter # unsafe checkout (no checkdeps), but suggested here
```

### Add the BParkingNano package and build everything

```shell
git clone git@github.com:CMSBParking/BParkingNANO.git ./PhysicsTools
git cms-addpkg PhysicsTools/NanoAOD
scram b
```

### To run on a test file

```shell
cd PhysicsTools/BParkingNano/test/
cmsenv 
cmsRun run_nano_cfg.py
```

## Provenance and branches

- This repo is forked from https://github.com/CMSBParking/BParkingNANO 
- The fork was made at revision https://github.com/CMSBParking/BParkingNANO/tree/b9bcad0b9b
- This revision is tagged as https://github.com/CMSRKR3/BParkingNANO/tree/from-BParkingNANO
   - Tag also available as https://github.com/CMSBParking/BParkingNANO/tree/from-BParkingNANO

**Default branches:**
- The default branch in CMSBParking is https://github.com/CMSBParking/BParkingNANO/tree/master
- The default branch in CMSRKR3 is https://github.com/CMSRKR3/BParkingNANO/tree/main

The default branch has been renamed for two reasons:

1) To promote more inclusive terminology, as per the GitHub guidelines
2) To clearly differentiate between the different development thread of the two repositories, namely:
   - CMSBParking/BParkingNANO:master targets the CMSSW development cycle CMSSW_10_2_X
   - CMSRKR3/BParkingNANO:main targets the CMSSW development cycle CMSSW_12_4_X

Further, two additional branches have been produced based on the revision above:

- CMSBParking/BParkingNANO:CMSSW_10_2_X and CMSBParking/BParkingNANO:CMSSW_12_4_X
- CMSRKR3/BParkingNANO:CMSSW_10_2_X and CMSRKR3/BParkingNANO:CMSSW_12_4_X

which may be of use. For example:

- CMSSW_10_2_X developments in CMSBParking/BParkingNANO should be merged into the master (and CMSSW_10_2_X) branch 
- CMSSW_12_4_X developments in CMSBParking/BParkingNANO should be merged into the CMSSW_12_4_X branch
- CMSSW_10_2_X developments in CMSRKR3/BParkingNANO should be merged into the CMSSW_10_2_X branch 
- CMSSW_12_4_X developments in CMSRKR3/BParkingNANO should be merged into the main (and CMSSW_12_4_X) branch

## Contributing

We use the _fork and pull_ model:

- Fork this repository https://github.com/CMSRKR3/BParkingNANO (top right _Fork_ button)

- If you haven't done so yet, clone this repository:

```shell
git clone git@github.com:CMSRKR3/BParkingNANO.git  ./PhysicsTools
```

- Add your fork of the repository as remote:

```shell
git remote add mine git@github.com:`git config user.github`/BParkingNANO.git
git checkout -b ${USER}_feature_branch origin/main
```

- Work on your feature, add, commit, etc. and push to your own fork

```shell
git push mine feature_branch
```

- Make a pull request on GitHub
