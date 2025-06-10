# NanoAOD producer customized for BParking analyses 

The focus is on RK/K*/phi analyses.

## Recipe

This recipe is for 14_0_21, based on the updated working on 13_3_0 which is based on original working on 12_4_X. The original recipe for 10_2_X can be found [here](https://github.com/CMSBParking/BParkingNANO/blob/master/README.md).

Currently using release CMSSW_14_0_21 to be able to run on 2024 samples and to run EgammaPostRecoTools with the correct weights for Run 3 noIso MVA electron ID.

### Getting started

```shell
cmsrel CMSSW_14_0_21_patch1
cd CMSSW_14_0_21_patch1/src
cmsenv
# Add modifications needed to use post-fit quantities for electrons
git cms-merge-topic -u pviscone:14_0_21_GsfTransientTracks_124X # unsafe checkout (no checkdeps), but suggested here
# Add modifications to KinematicParticleVertexFitter
git cms-merge-topic -u pviscone:14_0_21_fixKinParticleVtxFitter_124X # unsafe checkout (no checkdeps), but suggested here
# Add the DoubleElectronNANO package
git clone -b 14_0_21 git@github.com:pviscone/DoubleElectronNANO.git ./PhysicsTools
# Add fixed NanoAOD 130X module + isolation and iso-correction for lowPt electrons
git cms-merge-topic -u pviscone:14_0_21_DoubleElectronNANO_nanoaodFix_leptonIso_1330  # unsafe checkout (no checkdeps), but suggested here
# Add CMSSW changes necessary to (optionally) save all NANOAOD collections in the event
git cms-merge-topic -u pviscone:14_0_21_dev_allNanoColl_cmssw1330  # unsafe checkout (no checkdeps), but suggested here
# Adding EgammaPostRecoTools for Run 3 noIso electron ID fix
git clone git@github.com:cms-egamma/EgammaPostRecoTools.git EgammaUser/EgammaPostRecoTools

# Remove CMSSW_14_X exception in EGammaPostRecoTools
cd EgammaUser/EgammaPostRecoTools
cat >> EGMPostReco.patch << EOF                                                                                                                                                                                                                    (master !?)
diff --git a/python/EgammaPostRecoTools.py b/python/EgammaPostRecoTools.py
index f9e0e25..63667dd 100644
--- a/python/EgammaPostRecoTools.py
+++ b/python/EgammaPostRecoTools.py
@@ -20,10 +20,10 @@ def _validRelease():

     if majorVersion not in allowedVersions:
         allowedStr = ', '.join(str(x) for x in allowedVersions.keys())
-        raise Exception("EgammaPostRecoTools: CMSSW major version {} is not supported; allowed versions: {}.\nPlease contact E/gamma POG to see if this version should be supported".format(majorVersion,allowedStr))
+        #raise Exception("EgammaPostRecoTools: CMSSW major version {} is not supported; allowed versions: {}.\nPlease contact E/gamma POG to see if this version should be supported".format(majorVersion,allowedStr))
     elif minorVersion not in allowedVersions[majorVersion]:
         allowedStr = ', '.join(str(x) for x in allowedVersions[majorVersion])
-        raise Exception("EgammaPostRecoTools: CMSSW major version {} is supported, but minor version {} is not, allowed versions: {}.\nPlease contact E/gamma POG to see if this version should be supported".format(majorVersion,minorVersion,allowedStr))
+        #raise Exception("EgammaPostRecoTools: CMSSW major version {} is supported, but minor version {} is not, allowed versions: {}.\nPlease contact E/gamma POG to see if this version should be supported".format(majorVersion,minorVersion,allowedStr))

 def _isULDataformat():
     cmsswVersion =_getCMSSWVersion()
EOF
git apply EGMPostReco.patch
cd $CMSSW_BASE/src

# Build 
scram b -j `nproc`
```

### Run on a test file
```shell
cd PhysicsTools/BParkingNano/test
cmsRun run_nano_cfg.py        # by default, runs over Run 3 2023 data
cmsRun run_nano_cfg.py isMC=1 # runs over BuToKJPsi_JPsiToEE MC for 2023
```

### Submit CRAB jobs to process Run 3 data and MC for 2022/2023

```shell
cd $CMSSW_BASE/src/PhysicsTools/BParkingNano/production
source /cvmfs/cms.cern.ch/common/crab-setup.sh
python3 submit_on_crab.py
# or ./run.sh for preconfig commands
```

---

## Provenance and branches

- This repo is forked from https://github.com/CMSBParking/BParkingNANO 
- The fork was made at revision https://github.com/CMSBParking/BParkingNANO/tree/b9bcad0b9b
- This revision is tagged as https://github.com/DiElectronX/BParkingNANO/tree/from-BParkingNANO
   - Tag also available as https://github.com/CMSBParking/BParkingNANO/tree/from-BParkingNANO

**Default branches:**
- The default branch in CMSBParking is https://github.com/CMSBParking/BParkingNANO/tree/master
- The default branch in DiElectronX is https://github.com/DiElectronX/BParkingNANO/tree/main

The default branch has been renamed for two reasons:

1) To promote more inclusive terminology, as per the GitHub guidelines
2) To clearly differentiate between the different development thread of the two repositories, namely:
   - CMSBParking/BParkingNANO:master targets the CMSSW development cycle CMSSW_10_2_X
   - DiElectronX/BParkingNANO:main targets the CMSSW development cycle CMSSW_12_4_X

Further, two additional branches have been produced based on the revision above:

- CMSBParking/BParkingNANO:CMSSW_10_2_X and CMSBParking/BParkingNANO:CMSSW_12_4_X
- DiElectronX/BParkingNANO:CMSSW_10_2_X and DiElectronX/BParkingNANO:CMSSW_12_4_X

which may be of use. For example:

- CMSSW_10_2_X developments in CMSBParking/BParkingNANO should be merged into the master (and CMSSW_10_2_X) branch 
- CMSSW_12_4_X developments in CMSBParking/BParkingNANO should be merged into the CMSSW_12_4_X branch
- CMSSW_10_2_X developments in DiElectronX/BParkingNANO should be merged into the CMSSW_10_2_X branch 
- CMSSW_12_4_X developments in DiElectronX/BParkingNANO should be merged into the main (and CMSSW_12_4_X) branch

## Contributing

We use the _fork and pull_ model:

- Fork this repository https://github.com/DiElectronX/BParkingNANO (top right _Fork_ button)

- If you haven't done so yet, clone this repository:

```shell
git clone git@github.com:DiElectronX/BParkingNANO.git  ./PhysicsTools
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
