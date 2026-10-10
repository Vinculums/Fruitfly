"""Run unchanged tests with inherited ACLs on managed Windows workspaces.

Windows mkdir(mode=0o700) can remove the sandbox identity from temporary
fixtures. Only tempfile directory creation uses the inherited 0o777 mode here.
Test inputs/assertions and application file permissions are unchanged.
"""
import os
import sys
import unittest

original_mkdir = os.mkdir


def inherited_acl_mkdir(path, mode=0o777, *, dir_fd=None):
    if os.name == 'nt' and mode == 0o700:
        mode = 0o777
    return original_mkdir(path, mode, dir_fd=dir_fd)


if __name__ == '__main__':
    os.mkdir = inherited_acl_mkdir
    try:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.discover('tests'))
    finally:
        os.mkdir = original_mkdir
    sys.exit(not result.wasSuccessful())
