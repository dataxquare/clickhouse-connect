from setuptools import Extension
from setuptools.command.build_ext import build_ext
import os
import sys

# Custom build_ext command to handle Cython compilation
class CustomBuildExt(build_ext):
    def run(self):
        try:
            from Cython.Build import cythonize
            self.extensions = cythonize(self.extensions, language_level='3str')
        except ImportError as ex:
            print('Cython Install Failed, Not Building C Extensions: ', ex)
            sys.exit(1)
        except Exception as ex:
            print('Cython Build Failed, Not Building C Extensions: ', ex)
            sys.exit(1)
        super().run()

# Define Cython extensions
def get_extensions():
    return [
        Extension(
            name="clickhouse_connect.driverc.module", # Adjust the name according to your package structure
            sources=["clickhouse_connect/driverc/*.pyx"],
            # Include additional compile arguments if necessary
        )
    ]

# Function required by Poetry to handle the build process
def build(setup_kwargs):
    setup_kwargs.update({
        'ext_modules': get_extensions(),
        'cmdclass': {'build_ext': CustomBuildExt},
    })
