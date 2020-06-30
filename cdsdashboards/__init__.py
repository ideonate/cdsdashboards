import pluggy

hookimpl = pluggy.HookimplMarker("cdsdashboards")
"""Marker to be imported and used in plugins (and for own implementations)"""

from .version import __version__

