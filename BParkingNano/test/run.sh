cmsRun run_nano_cfg.py isMC=1 maxEvents=1000 reportEvery=50 lhcRun=2 # MC with Run 2 (BParking 2018)
cmsRun run_nano_cfg.py isMC=0 maxEvents=1000 reportEvery=50 lhcRun=2 # Data with Run 2 (BParking 2018)
cmsRun run_nano_cfg.py isMC=1 maxEvents=1000 reportEvery=100 lhcRun=3 # MC with Run 3
cmsRun run_nano_cfg.py isMC=0 maxEvents=3000 reportEvery=100 lhcRun=3 is22=0 # Data with Run 3
cmsRun run_nano_cfg.py isMC=1 maxEvents=3000 reportEvery=100 lhcRun=3 is22=0 isSignal=0 # Data with Run 3

# export SINGULARITY_CACHEDIR="/eos/home-n/npalmeri/singularity"
# export APPTAINER_CACHEDIR="/eos/home-n/npalmeri/singularity"
# singularity shell -B /afs -B /eos -B /cvmfs docker://coffeateam/coffea-dask-almalinux8:latest
# # try accessing cvmfs inside of the container
# source /cvmfs/cms.cern.ch/cmsset_default.sh