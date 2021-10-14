"""
This script translates cross sections as printed in the logs to a .npz file
"""

import tarfile, os, os.path as osp, sys, re, numpy as np
from time import strftime

mz_pat = re.compile(r'mMediator=(\d+)')
xs_pat = re.compile(r'Cross\-section\s*:\s*([\de\+\-\.]+)\s*\+\-\s*([\de\+\-\.]+)')
lim_xs_pat = re.compile(r'Cross\-section\s*:\s*([\de\+\-]+)')

def read_tar(infile):
    mzs = []
    xss = []
    dxss = []
    with tarfile.open(infile) as tar:
        for member in tar.getmembers():
            if not osp.basename(member.name).startswith('err'): continue

            with tar.extractfile(member) as f:
                content = f.read().decode()

            mz = int(mz_pat.search(content).group(1))

            try:
                xs_match = xs_pat.search(content)
                xs = float(xs_match.group(1))
                dxs = float(xs_match.group(2))
            except AttributeError:
                xs_match = lim_xs_pat.search(content)
                xs = float(xs_match.group(1))
                dxss.append(-1.)
            
            mzs.append(mz)
            xss.append(xs)
            dxss.append(dxs)

    mzs = np.array(mzs)
    xss = np.array(xss)
    dxss = np.array(dxss)
    
    order = mzs.argsort()
    mzs = mzs[order]
    xss = xss[order]
    dxss = dxss[order]

    return mzs, xss, dxss

def print_arrays(mzs, xss, dxss):
    print(f'{"mz (GeV)":>9} {"xs (pb)":>9} {"dxs (pb)":>9}')
    for mz, xs, dxs in zip(mzs, xss, dxss):
        print(f'{mz:9.2f} {xs:9.2f} {dxs:9.2f}')

def compare():
    for infile in [
        'computexs_Oct12.tar',
        'computexs_Oct12_highercount.tar'
        ]:
        print(f'\n{infile}:')
        print_arrays(*read_tar(infile))

def make_npz():
    mzs, xss, dxss = read_tar('computexs_Oct12_highercount.tar')
    print_arrays(mzs, xss, dxss)
    outfile = strftime('crosssections_%b%d.npz')
    print(f'Dumping to {outfile}')
    np.savez(outfile, mz=mzs, xs=xss, dxs=dxss)

def main():
    make_npz()

if __name__ == '__main__':
    main()