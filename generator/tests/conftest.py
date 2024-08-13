import pytest

import json


@pytest.fixture
def schemas():
    import os
    print('CURRRR', os.getcwd())
    with open('./generator/tests/schemas.json') as f:
        schemas = json.load(f)
    return schemas
