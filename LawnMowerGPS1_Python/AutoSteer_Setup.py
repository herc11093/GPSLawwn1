import csv





# Start Serial GPS
# or
# Start simulator

#Loadconfig file
def Loadconfigfile():
    #https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3
    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # ver. < 3.0

    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read('Config.py')
    # read values from a section
    string_val = config.get('section_a', 'string_val')
    bool_val = config.getboolean('section_a', 'bool_val')
    int_val = config.getint('section_a', 'int_val')
    float_val = config.getfloat('section_a', 'pi_val')


