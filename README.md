# Cross sections for the (boosted) SVJ analysis

## Computing new cross sections

On a node with an `htcondor` queue (LPC, CMSConnect, etc.), do:

```
virtualenv myenv
source myenv/bin/activate
pip install qondor
qondor-submit computexs.py
```

Or, without needing `htcondor`, run locally (still requires a `/cvmfs` mount though):

```
virtualenv myenv
source myenv/bin/activate
pip install qondor
python computexs.py > my_new_log.txt 2>&1
```

## Read the job log

Using the prepared tarballs:

```
xrdcp root://cmseos.fnal.gov//store/user/lpcdarkqcd/boosted/other/crosssections/computexs_Oct12_highercount.tar .
python getxs.py
```
