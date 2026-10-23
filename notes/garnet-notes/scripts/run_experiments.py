#!/usr/bin/env python3
"""Run from a pinned gem5 checkout. Outputs remain outside the checkout."""
import configparser
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

repo = Path.cwd()
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=False)
binary = repo / 'build/Garnet_standalone/gem5.opt'
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
records = []
cases = [(f'load_{r}', r, []) for r in (0.01, 0.1, 0.3, 0.6)]
cases += [('router4', 0.1, ['--router-latency=4']),
          ('vnet2', 0.1, ['--inj-vnet=2']),
          ('dedicated', 0.1, ['--per-vnet-links'])]
for name, rate, extra in cases:
    run = out / name
    cmd = [str(binary), '-d', str(run), 'configs/example/garnet_synth_traffic.py',
           '--num-cpus=16', '--num-dirs=16', '--network=garnet',
           '--topology=Mesh_XY', '--mesh-rows=4', '--routing-algorithm=1',
           '--sim-cycles=50000000', '--synthetic=uniform_random',
           f'--injectionrate={rate}', *extra]
    run.mkdir()
    with (run / 'stdout.log').open('w') as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
    assert 'Network Tester completed simCycles' in (run / 'stdout.log').read_text()
    stats = {}
    for line in (run / 'stats.txt').read_text().splitlines():
        fields = line.split()
        if len(fields) >= 2:
            try:
                stats[fields[0]] = float(fields[1])
            except ValueError:
                pass
    cfg = configparser.ConfigParser(strict=False)
    cfg.read(run / 'config.ini')
    rec = dict(name=name, rate=rate, extra=extra, command=cmd,
               simTicks=stats['simTicks'], simFreq=stats['simFreq'],
               tester_clock_ticks=int(cfg['system.clk_domain']['clock']),
               ruby_clock_ticks=int(cfg['system.ruby.clk_domain']['clock']),
               internal_links=len(cfg['system.ruby.network']['int_links'].split()))
    for key in ['flits_injected::total', 'flits_received::total',
                'packets_injected::total', 'packets_received::total',
                'average_flit_latency', 'average_flit_network_latency',
                'average_flit_queueing_latency', 'average_packet_latency']:
        values = [v for k, v in stats.items() if k.endswith('.' + key)]
        assert len(values) == 1 and math.isfinite(values[0]), key
        rec[key] = values[0]
    assert rec['flits_injected::total'] >= rec['flits_received::total'] > 0
    records.append(rec)
    print(name, rec['average_flit_latency'], flush=True)
summary = dict(revision=revision, binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
               build_info=subprocess.check_output([str(binary), '--build-info'], text=True),
               runs=records)
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
