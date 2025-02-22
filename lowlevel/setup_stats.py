from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options
import numpy
# from Cython.Compiler.Options import directive_defaults
Cython.Compiler.Options.annotate = True
# directive_defaults['linetrace'] = True
# directive_defaults['binding'] = True

# Run with: python setup_stats.py build_ext -i

ext_modules = [
    Extension(name='CH_to_EKM_statistics',
              sources=['CH_to_EKM_statistics.pyx'],
              extra_compile_args=["-O2"],
              libraries=["gsl", "gslcblas", "m"],
              include_dirs=[numpy.get_include()]
              # define_macros=[('CYTHON_TRACE', '1')]
              ),
]

setup(
    name='CH_to_EKM_statistics',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
