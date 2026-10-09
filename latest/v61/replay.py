#!/usr/bin/env python3
"""Integrity and clean byte-for-byte rebuild of the v61 calculations."""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def integrity():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    if manifest['version']!='v61':raise ValueError('Wrong snapshot')
    total=0
    for rel,rec in manifest['files'].items():
        p=ROOT/rel
        if not p.is_file() or p.stat().st_size!=rec['bytes'] or sha(p)!=rec['sha256']:
            raise AssertionError(('integrity mismatch',rel))
        total+=rec['bytes']
    return manifest,total

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rebuild',action='store_true');args=parser.parse_args()
    manifest,total=integrity()
    names=['analytic_certificate.json','geometry_certificate.json']
    expected={name:(ROOT/name).read_bytes() for name in names}
    logs=[]
    if args.rebuild:
        with tempfile.TemporaryDirectory(prefix='mahler_v61_clean_') as td:
            fresh=Path(td)
            for rel in manifest['files']:
                dst=fresh/rel;dst.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(ROOT/rel,dst)
            for script,name in [('analytic_verifier.py',names[0]),('geometry_verifier.py',names[1])]:
                (fresh/name).unlink()
                done=subprocess.run([sys.executable,str(fresh/script),'--output',str(fresh/name)],
                                    cwd=fresh,capture_output=True,text=True,timeout=300)
                if done.returncode:
                    raise RuntimeError(f'{script} failed\n{done.stdout}\n{done.stderr}')
                if (fresh/name).read_bytes()!=expected[name]:
                    raise AssertionError(('regenerated certificate differs',name))
                logs.append(dict(script=script,stdout=done.stdout.strip(),byte_identical=True))
        integrity()
    a=json.loads(expected[names[0]]);g=json.loads(expected[names[1]])
    assert a['status']==g['status']=='PASS'
    assert a['complete_terminal_cases']==12 and a['negative_coefficients']==0
    assert a['positive_coefficients']==1092 and a['zero_coefficients']==391
    assert g['independently_reconstructed_pairs']==31
    assert g['independent_cap_intersections']==g['independent_bridge_hulls']==27
    assert g['monotone_path_segments']==6
    assert not a['general_four_dimensional_Mahler_proved']
    result=dict(status='PASS',version='v61',rebuild=args.rebuild,
        files_integrity_checked=len(manifest['files']),bytes_integrity_checked=total,
        new_certificates_regenerated=2 if args.rebuild else 0,logs=logs,
        earlier_mathematics_replayed=False,
        full_four_dimensional_Mahler_proved=False,
        formal_proof_assistant_used=False)
    (ROOT/'replay_output.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
