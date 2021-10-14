"""# submit
htcondor('request_memory', '4096')
for mz in [100.+10.*i for i in range(50)]:
    submit(mz=mz)
"""# endsubmit

import qondor, re
cmssw = qondor.svj.CMSSW.from_tarball(
    'root://cmseos.fnal.gov//store/user/klijnsma/semivis/crosssection_study/CMSSW_10_2_21_withmgpatch.tar.gz'
    )

physics = qondor.svj.Physics({
    'year' : 2018,
    'mz' : qondor.scope.mz,
    'mdark' : 10.,
    'rinv' : 0.3,
    'max_events' : 5000,
    'part' : 1
    })

output = cmssw.run_gridpack(physics)
output = '\n'.join(output)

# Extract cross section from the output
with open(
    'mgsummary_{0}_mz{1}.txt'
    .format(
        'nomgpatch' if 'nomgpatch' in qondor.scope.tarball else 'withmgpatch',
        qondor.scope.mz
        ),
    'w' 
    ) as f:
    match = re.search(r'Cross\-section\s*:\s*([\d+e\+\-\.]+)\s*\+\-\s*([\d+e\+\-\.]+)\s*pb', output)
    if match:
        xs = float(match.group(1))
        dxs = float(match.group(2))
        f.write('xs = {0:.3f}\ndxs = {1:.3f}\n'.format(xs, dxs))
    match = re.search(r'Nb of events\s*:\s*([\d+e\+\-\.]+)', output)    
    if match:
        f.write('nevents = {0}\n'.format(match.group(1)))