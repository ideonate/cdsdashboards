import pluggy

hookimpl = pluggy.HookimplMarker("cdsdashboards")
"""Marker to be imported and used in plugins (and for own implementations)"""

__version__ = '0.0.20'
