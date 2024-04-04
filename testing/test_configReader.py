from src.configReader import ConfigReader


def test_parse_config_file():
    config = ConfigReader()
    config.parseConfigFile('../configFile/config1.txt')
    assert config.config == {'router-id': '1', 'input-ports': '6000, 6001, 6002', 'outputs': '6003-1-2, 6004-8-7, '

                                                                                             '6005-5-6'}


def test_validate_config():
    config = ConfigReader()
    config.parseConfigFile('../configFile/config1.txt')
    config.validateConfig()
    assert config.config == {'router-id': '1', 'input-ports': '6000, 6001, 6002', 'outputs': '6003-1-2, 6004-8-7, '
                
                                                                                             '6005-5-6'}


def test_invalid_config_name():
    config = ConfigReader()
    try:
        config.parseConfigFile('this is a test file name that does not exist')
    except SystemExit:
        assert True
    else:
        assert False
