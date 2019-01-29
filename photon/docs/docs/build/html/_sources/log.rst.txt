.. _log:

|python| |Python36|  |Licence|
|matplotlib| |PyQt5| |numpy| |scipy| 

.. |Licence| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
      :target: http://perso.crans.org/besson/LICENSE.html

.. |Opensource| image:: https://badges.frapsoft.com/os/v1/open-source.svg?v=103
      :target: https://github.com/ellerbrock/open-source-badges/

.. |python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
    :target: https://www.python.org/downloads/release/python-360/

.. |PyQt5| image:: https://img.shields.io/badge/poweredby-PyQt5-orange.svg
   :target: https://pypi.python.org/pypi/PyQt5

.. |matplotlib| image:: https://img.shields.io/badge/poweredby-matplotlib-orange.svg
   :target: https://matplotlib.org/

.. |Python36| image:: https://img.shields.io/badge/python-3.6-blue.svg
.. _Python36: https://www.python.org/downloads/release/python-360/

.. |numpy| image:: https://img.shields.io/badge/poweredby-numpy-orange.svg
   :target: http://www.numpy.org/

.. |scipy| image:: https://img.shields.io/badge/poweredby-scipy-orange.svg
   :target: https://www.scipy.org/



Change log
----------
----------


* **photon 0.2.2**:

  * modif: The file names are displayed now without the path.
  * bug fix: Straight line crashed photon when adding a straight line as first element
  * bug fix: zorder straight line was not taken into account
  * bug fix: Update the plot was modifying the style of the legend. Now it is fixed

* **photon 0.2.0**:

  * New **plot type**: band. This allows you to fill the space between two curves.
  * fitsio --> astropy: mainly because some people reported problem with installing fitsio on py3.6.4.

  


* **photon 0.1.8**: 

  * axis in error plot fixed (X and Y we reversed)
  * load of marker for error plot the marker that was saved in the plot configuration file was not extracted correclty
  * update Logo
  * update online and local documentation 

