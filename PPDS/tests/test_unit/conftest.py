# this allows tests to import the source-directories
import sys
import os
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "../..")

sys.path.extend([
    os.path.join(PROJECT_ROOT, "tests", '../test_helpers'),
    os.path.join(PROJECT_ROOT, "src")
    ])

print(sys.path)