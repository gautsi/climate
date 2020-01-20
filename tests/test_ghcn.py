import src.ghcn as ghcn


def test_get_ghcn_specs():
    assert ghcn.get_ghcn_specs()["file_type"] == "stations"
