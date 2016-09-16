class Package:
    DEP_KEYS = ['Pre-Depends', 'Depends']
    OPTIONAL_DEP_KEYS = ['Recommends', 'Suggests']
    PROVIDES_KEY = 'Provides'
    SOURCE_KEY = 'Source'
    CONFLICT_KEY = 'Conflicts'

    def __init__(self, dict_pkg):
        self.pkg = dict_pkg

    def get_dict(self):
        return self.pkg

    def get_name(self):
        return self.pkg['Package']

    def get_optional_dependencies(self):
        return self._get_values_by_keys(self.OPTIONAL_DEP_KEYS)

    def get_required_dependencies(self):
        return self._get_values_by_keys(self.DEP_KEYS)

    def get_provides(self):
        if self.PROVIDES_KEY in self.pkg:
            return self.pkg[self.PROVIDES_KEY]
        return []

    def get_source(self):
        if self.SOURCE_KEY in self.pkg:
            return self.pkg[self.SOURCE_KEY]

    def get_conflicts(self):
        if self.CONFLICT_KEY in self.pkg:
            return self.pkg[self.CONFLICT_KEY]
        return []

    def is_info_exist(self, infokey):
        return infokey in self.pkg

    def _get_values_by_keys(self, keys):
        values = []
        for key in keys:
            if key in self.pkg:
                values += self.pkg[key]
        return values
