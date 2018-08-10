from setuptools import setup  # Always prefer setuptools over distutils
import photon.__info__ as phot
print(phot.__dict__.keys())

setup(
   name = 'photon_plot',
   version = phot.__version__,
   author = phot.__author__,
   author_email = phot.__email__,
   packages = ['photon'],
   entry_points = {'gui_scripts': ['photon = photon.__main__:main',],},
   url = phot.__website__,
   license = phot.__license__,
   description = 'Python tool for easy data plotting',
   python_requires = '>=3.6',
   install_requires = [
      "PyQt5 >= v5.10.1",
      "scipy >= 1.0.1",
      "numpy >=1.14.2",
      "matplotlib >= 2.2.2",
      "astropy >= 3.0.2",
      "Pillow >=5.1.0",
   ],
   include_package_data=True,
)
