import os
from typing import Tuple, List

import pytest

from layer_linter.dependencies.scanner import PackageScanner
from layer_linter.module import Module, SafeFilenameModule


class TestPackageScanner:
    def test_success(self):
        package = SafeFilenameModule(
            name='scannersuccess',
            filename=os.path.join(self._get_package_directory('scannersuccess'), '__init__.py'),
        )

        scanner = PackageScanner(package)
        modules = scanner.scan_for_modules()

        expected_modules = self._build_modules(
            package_name='scannersuccess',
            tuples=(
                ('scannersuccess', '__init__.py'),
                ('scannersuccess.one', 'one/__init__.py'),
                ('scannersuccess.one.alpha', 'one/alpha.py'),
                ('scannersuccess.one.beta', 'one/beta.py'),
                ('scannersuccess.one.gamma', 'one/gamma.py'),
                ('scannersuccess.one.delta', 'one/delta/__init__.py'),
                ('scannersuccess.one.delta.green', 'one/delta/green.py'),
                ('scannersuccess.one.delta.red_blue', 'one/delta/red_blue.py'),
                ('scannersuccess.two', 'two/__init__.py'),
                ('scannersuccess.two.alpha', 'two/alpha.py'),
                ('scannersuccess.two.beta',  'two/beta.py'),
                ('scannersuccess.two.gamma',  'two/gamma.py'),
                ('scannersuccess.four', 'four.py'),
                # Also include invalid modules. To keep things simple, Layer Linter won't decide
                # what is and isn't allowed - but we don't want them to break things.
                ('scannersuccess.in', 'in/__init__.py'),
                ('scannersuccess.in.class', 'in/class.py'),
                ('scannersuccess.in.hyphenated-name', 'in/hyphenated-name.py'),

            ),
        )
        assert set(modules) == set(expected_modules)
        # Also check that the filenames are the same.
        sort_by_name = lambda m: m.name
        sorted_modules = sorted(modules, key=sort_by_name)
        sorted_expected_modules = sorted(expected_modules, key=sort_by_name)
        for index, module in enumerate(sorted_modules):
            assert module.filename == sorted_expected_modules[index].filename

    def _get_package_directory(self, package_name: str) -> str:
        """
        Return absolute path to the package directory.
        """
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'assets', package_name, package_name,
            )
        )

    def _build_modules(self,
                       package_name: str,
                       tuples: Tuple[Tuple[str, str]]) -> List[SafeFilenameModule]:
        package_directory = self._get_package_directory(package_name)
        modules = []
        for module_name, module_filename in tuples:
            modules.append(
                SafeFilenameModule(
                    name=module_name,
                    filename=os.path.join(package_directory, module_filename),
                )
            )
        return modules
