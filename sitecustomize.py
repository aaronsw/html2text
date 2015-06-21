import os

import coverage


here = os.getcwd()
config_file = os.path.join(here, '.coveragerc')
os.environ['COVERAGE_PROCESS_START'] = config_file
coverage.process_startup()
