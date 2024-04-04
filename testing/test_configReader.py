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


def test_invalid_input_port():
    config = ConfigReader()
    invalidConfigFile = {'router-id': '1', 'input-ports': '1, 6001, 6002', 'outputs': '6003-1-2, 6004-8-7, '
                                                                                      '6005-5-6'}
    config.config = invalidConfigFile
    try:
        config.validateConfig()
    except SystemExit:
        assert True
    else:
        assert False


def test_invalid_output_port():
    config = ConfigReader()
    invalidConfigFile = {'router-id': '1', 'input-ports': '6000, 6001, 6002', 'outputs': '1-1-2, 6004-8-7, '
                                                                                         '6005-5-6'}
    config.config = invalidConfigFile
    try:
        config.validateConfig()
    except SystemExit:
        assert True
    else:
        assert False


def test_invalid_param_number():
    config = ConfigReader()
    invalidConfigFile = {'router-id': '1', 'input-ports': '6000, 6001, 6002'}
    config.config = invalidConfigFile
    try:
        config.validateConfig()
    except SystemExit:
        assert True
    else:
        assert False


def test_invalid_router_id():
    config = ConfigReader()
    invalidConfigFile = {'router-id': '64001', 'input-ports': '6000, 6001, 6002', 'outputs': '6003-1-2, 6004-8-7, '
                                                                                             '6005-5-6'}
    config.config = invalidConfigFile
    try:
        config.validateConfig()
    except SystemExit:
        assert True
    else:
        assert False


def test_invalid_output_router_id():
    config = ConfigReader()
    invalidConfigFile = {'router-id': '1', 'input-ports': '6000, 6001, 6002', 'outputs': '6003-1-64001, 6004-8-7, '
                                                                                         '6005-5-6'}
    config.config = invalidConfigFile
    try:
        config.validateConfig()
    except SystemExit:
        assert True
    else:
        assert False


def test_correct_router_id():
    config = ConfigReader()
    config.parseConfigFile('../configFile/config1.txt')
    config.validateConfig()
    assert config.getRouterId() == 1


def test_correct_input_ports():
    config = ConfigReader()
    config.parseConfigFile('../configFile/config1.txt')
    config.validateConfig()
    assert config.getInputPorts() == [6000, 6001, 6002]


def test_correct_outputs():
    config = ConfigReader()
    config.parseConfigFile('../configFile/config1.txt')
    config.validateConfig()
    assert config.getOutputs() == [(6003, 1, 2), (6004, 8, 7), (6005, 5, 6)]


def test_get_router_id():
    config = ConfigReader()
    config.parseConfigFile('../configFile/config1.txt')
    config.validateConfig()
    assert config.getRouterId() == 1

