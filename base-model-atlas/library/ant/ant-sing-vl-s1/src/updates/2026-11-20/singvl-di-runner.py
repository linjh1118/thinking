"""Run the pinned Decision Index kit against this downloaded model snapshot."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--panel', required=True, choices=('text', 'vision'))
    parser.add_argument('--suite-dir', type=Path, required=True,
                        help='verified text-public-0.3 or vision suite directory')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--model', type=Path, default=Path(__file__).resolve().parent.parent,
                        help='local checkpoint directory; defaults to this model snapshot')
    parser.add_argument('--device', default='cuda:0')
    parser.add_argument('--limit', type=int, help='smoke test only; does not produce a complete public run')
    parser.add_argument('--fresh', action='store_true')
    parser.add_argument('--print-command', action='store_true', help='show the command without loading the model')
    args = parser.parse_args()
    model = args.model.resolve()
    code_root = Path(__file__).resolve().parent.parent
    if not (model/'config.json').is_file():
        parser.error('--model must be a downloaded local checkpoint containing config.json')
    if not args.suite_dir.is_dir():
        parser.error('--suite-dir must be an existing prepared suite directory')
    if args.limit is not None and args.limit < 1:
        parser.error('--limit must be positive')
    command = [sys.executable, '-m', 'decision_index']
    if args.panel == 'vision':
        command += ['vision', 'pipeline', '--dir', str(args.suite_dir.resolve()), '--workers', '1']
    else:
        command += ['pipeline', '--edition', '0.3', '--suite-dir', str(args.suite_dir.resolve())]
    command += ['--engine', 'inference.engine:D3Engine', '--model', str(model),
                '--option', 'device='+args.device, '--out', str(args.out.resolve())]
    if args.limit is not None:
        command += ['--limit', str(args.limit)]
    if args.fresh:
        command += ['--fresh']
    env = os.environ.copy()
    env['PYTHONPATH'] = str(code_root) + (os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    print(json.dumps({'code_root': str(code_root), 'model': str(model),
                      'command': shlex.join(command), 'partial_run': args.limit is not None}), flush=True)
    if not args.print_command:
        subprocess.run(command, env=env, check=True)


if __name__ == '__main__':
    main()
