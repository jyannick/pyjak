from pyjak.toolbox import lazy_property


class Component(object):
    def __init__(self, source_files):
        self.source_files = source_files

    @lazy_property
    def internal_imports(self):
        imports_inside_module = {source.qualified_name: 0 for source in self.source_files}
        for source in self.source_files:
            for import_ in source.imports:
                if import_ in imports_inside_module.keys():
                    imports_inside_module[import_] += 1
        return imports_inside_module

