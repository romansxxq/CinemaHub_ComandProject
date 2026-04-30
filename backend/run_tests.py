#!/usr/bin/env python
"""
Simple test runner script for CinemaHub
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True, keepdb=False)
    
    # Run tests
    failures = test_runner.run_tests(["api"])
    sys.exit(bool(failures))
