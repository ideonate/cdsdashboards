import pluggy


pm = pluggy.PluginManager("cdsdashboards")
pm.load_setuptools_entrypoints("cdsdashboards")
