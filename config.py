#
# Product configuration. This contents of this module will be imported into
# __init__.py and every content type module.
#
# If you wish to perform custom configuration, you may put a file AppConfig.py
# in your product's root directory. This will be included in this file if
# found.
#

HAS_PLONEPAS = False
try:
    from Products import PlonePAS
    HAS_PLONEPAS = True
except ImportError:
    pass

product_globals=globals()