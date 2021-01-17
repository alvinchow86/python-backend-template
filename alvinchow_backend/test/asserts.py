def assert_keys_exist(obj, keys):
    assert set(keys) <= set(obj.keys())
