#!/usr/bin/env python3
#
# drive_check -- check for all zero'd out bytes on a drive
# Copyright (C) 2017  Jim Wyllie
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__doc__ = """
Checks for a drive to be nothing but zeroes, as established by dban and most
fast-drive cleaning tools.  If there's anything on the drive that isn't zeroes,
it will output what that is.
"""

import sys
import argparse
from tqdm import tqdm

from functools import partial

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--seek', type=int, default=0, required=False, help='If set, skips this many bytes in the input stream.  Useful for resuming.')
parser.add_argument('--size', required=True, type=int, help='If set, will output a progress bar using tqdm, and use the expected size to do it.')
parser.add_argument('--workers', required=False, type=int, default=1, help='Number of workers to process the input.  Defaults to %(default)s')
parser.add_argument('--readsize', required=False, type=int, default='4194304', help='If set, will output a progress bar using tqdm, and use the expected size to do it')
parser.add_argument('--max_bytes', default=1024 * 1024 * 1024 * 100, type=int, help="If set, will barf out once a number of max-bytes has been reached as it can't save the history any more.  Defaults to %(default)s bytes.")
parser.add_argument('--results', required=True, type=str, help='File to output the checking results.')
parser.add_argument('--target', default='/dev/stdin', required=False, help='Target for reading.  If not set, defaults to standard input')

options = parser.parse_args()

# Well, I haven't written the multiprocess model on this one yet.  If I need it, I will.
if options.workers != 1:
	raise NotImplementedError("This requires a multiprocessing model that I have not yet bothered to implement, as I'm worried about premature optimization.  Please try again with --workers 1 or omit the argument.")
	sys.exit(1)

nonzero_reads = bytearray()
total_read = 0
too_full = False

with tqdm(total=options.size) as pbar:
	with open(options.target, 'rb', buffering=options.readsize) as handle:

		# Seek if we're supposed to do that...
		if options.seek != 0:
			handle.seek(options.seek)

		# Read in a byte file that works with an iterable.  Had to hack from the below link.
		# http://stackoverflow.com/questions/15599639/whats-perfect-counterpart-in-python-for-while-not-eof
		for test_bytes in iter(partial(handle.read, options.readsize), b''):
			
			if test_bytes.count(0) != len(test_bytes):
				nonzero_reads.extend(test_bytes)

			pbar.update(len(test_bytes))
			total_read += len(test_bytes)

			# If we have too much non-zeroes, barf out
			if len(nonzero_reads) > options.max_bytes:
				too_full = True
				break

# Get around a divide-by-zero bug:
if total_read == 0:
	total_read = 1

# All done.  Let's see what happened.
print()
print('------ Statistics ---------')
print(   'Bytes read (bytes): {}'.format(total_read))
print('Nonzero blobs (bytes): {} ({}%)'.format(len(nonzero_reads), (len(nonzero_reads) * 100.0 / (total_read))))
print()

# Write out the file
with open(options.results, 'wb') as handle:
	handle.write(nonzero_reads)
