class DataCustomizationDTO:
    # TODO: Use this object to send data and replacements to frontend, then receive the same object with replacement modifications
    def __init__(self, data, replacements_map):
        self.data = data
        self.replacements_map = replacements_map
