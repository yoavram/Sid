#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Sid.
# https://github.com/yoavram/Sid

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>
from unittest import TestCase, main
import pkg_resources
import shutil
import tempfile
import os
import glob
import csv
import matplotlib
from click.testing import CliRunner # See reference on testing Click applications: http://click.pocoo.org/5/testing/
import Sid

CI = os.environ.get('CI', 'false').lower() == 'true'


class MplTestCase(TestCase):
	def test_mpl(self):
		if CI:
			self.assertEquals(matplotlib.rcParams['backend'].lower(), 'agg')


class SimpleTestCase(TestCase):
	_multiprocess_can_split_ = True

	def setUp(self):
		self.runner = CliRunner()


	def tearDown(self):
		pass


	def test_help(self):
		result = self.runner.invoke(Sid.take_cover.main, ['--help'])
		self.assertEquals(result.exit_code, 0)


	def test_version(self):
		result = self.runner.invoke(Sid.take_cover.main, ['--version'])
		self.assertEquals(result.exit_code, 0)
		self.assertIn(Sid.__version__, result.output)


	def test_where(self):
		result = self.runner.invoke(Sid.take_cover.main, ['--where'])
		self.assertEquals(result.exit_code, 0)
		self.assertIn("sid", result.output.lower())
		path = result.output.strip()
		self.assertTrue(os.path.exists(path), msg=path)


class MainTestCase(TestCase):
	_multiprocess_can_split_ = True


	def setup_with_context_manager(self, cm):
	    """Use a contextmanager to setUp a test case.
	    See http://nedbatchelder.com/blog/201508/using_context_managers_in_test_setup.html
	    """
	    val = cm.__enter__()
	    self.addCleanup(cm.__exit__, None, None, None)
	    return 


	def setUp(self):
		self.files = pkg_resources.resource_listdir('Sid.images', '')
		self.files = [fn for fn in self.files if os.path.splitext(fn)[-1] == Sid.take_cover.EXTENSION]
		self.files.sort()
		self.runner = CliRunner()
		self.ctx = self.setup_with_context_manager(self.runner.isolated_filesystem())
		self.dirpath = os.getcwd()
		self.assertTrue(os.path.exists(self.dirpath))
		self.assertTrue(os.path.isdir(self.dirpath))

		for fn in self.files:
			src = pkg_resources.resource_filename('Sid.images', fn)
			shutil.copy(src, '.')
			self.assertTrue(os.path.exists(os.path.join(self.dirpath, fn)))
			self.assertTrue(os.path.isfile(os.path.join(self.dirpath, fn)))


	def tearDown(self):
		pass


	def test_run_once(self):
		num_files = len(self.files)
		result = self.runner.invoke(
			Sid.take_cover.main,
			['--verbose', '--path', self.dirpath, '--watch', 'n'],
		)
		self.assertFalse(result.exception)
		self.assertEquals(result.exit_code, 0, result.exit_code)
		self.assertTrue(os.path.exists(os.path.join(self.dirpath, 'stats.csv')))
		self.assertTrue(os.path.exists(os.path.join(self.dirpath, 'histograms.csv')))
		pngs = glob.glob(os.path.join(self.dirpath, '*.png'))
		self.assertEquals(len(pngs), num_files * 2)
		with open(os.path.join(self.dirpath, 'stats.csv'), 'r') as f:
			data = csv.DictReader(f)
			for row in data:
				fn = os.path.split(row['image_id'])[-1] + Sid.take_cover.EXTENSION
				self.assertIn(fn, self.files)


if __name__ == '__main__':
	main()
