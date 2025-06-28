import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notebooks import setup as nb_setup


def test_setup_paths(tmp_path):
    paths = nb_setup.setup_paths(project_root=str(tmp_path))
    assert paths["PROJECT_ROOT"] == str(tmp_path)
    assert os.path.basename(paths["ECHO_MEMORY_PATH"]) == "ECHO_MEMORY.yaml"


def test_append_yaml_list(tmp_path):
    test_file = tmp_path / "data.yaml"
    nb_setup.append_yaml_list(str(test_file), {"a": 1}, list_key="items")
    data = nb_setup.load_yaml(str(test_file))
    assert data["items"][0]["a"] == 1
