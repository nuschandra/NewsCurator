class Countries():
    __countries = {}
    __countries['au'] = 'Australia'
    __countries['ca'] = 'Canada'
    __countries['in'] = 'India'
    __countries['ie'] = 'Ireland'
    __countries['my'] = 'Malaysia'
    __countries['nz'] = 'New Zealand'
    __countries['ng'] = 'Nigeria'
    __countries['ph'] = 'Philippines'
    __countries['sa'] = 'Saudi Arabia'
    __countries['sg'] = 'Singapore'
    __countries['za'] = 'South Africa'
    __countries['gb'] = 'United Kingdom'
    __countries['us'] = 'United States of America'
    
    def __init__(self): return;

    @staticmethod
    def getCountries() -> dict:
        return Countries.__countries
