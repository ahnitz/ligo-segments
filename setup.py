# Copyright (C) 2016 Duncan Macleod
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import os.path
import re
from setuptools import setup, Extension
import sys


# get version
def find_version(path):
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", open(path).read(), re.M)
	if not version_match:
		raise RuntimeError("'%s': unable to find __version__ string" % path)
	return version_match.group(1)

version = find_version(os.path.join('ligo', 'segments', '__init__.py'))

# transform ligo-segments.spec.in to ligo-segments.spec
open("ligo-segments.spec", "w").writelines([line.replace("@VERSION@", version) for line in open("ligo-segments.spec.in")])

# declare dependencies
setup_requires = ['setuptools']
cmdclass = {}

if {'pytest', 'test', 'prt'}.intersection(sys.argv):
	setup_requires.append('pytest_runner')

if {'build_sphinx'}.intersection(sys.argv):
	setup_requires.extend([
		'sphinx',
		'sphinx_rtd_theme',
	])
	from sphinx.setup_command import BuildDoc
	cmdclass['build_sphinx'] = BuildDoc


# run setup
setup(
	name = 'ligo-segments',
	version = version,
	description = 'Representations of semi-open intervals',
	author = 'Kipp Cannon',
	author_email = 'kipp.cannon@ligo.org',
	license = 'GPLv3',
	packages = ['ligo', 'ligo.segments'],
	namespace_packages = ['ligo'],
	cmdclass = cmdclass,
	setup_requires = setup_requires,
	install_requires = ['six'],
	ext_modules = [
		Extension(
			'ligo.segments.__segments',
			['src/segments.c', 'src/infinity.c', 'src/segment.c', 'src/segmentlist.c'],
			include_dirs = ['src'],
		),
	],
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Intended Audience :: Science/Research',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Astronomy',
		'Topic :: Scientific/Engineering :: Physics',
		'Operating System :: POSIX',
		'Operating System :: Unix',
		'Operating System :: MacOS',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	],
)
