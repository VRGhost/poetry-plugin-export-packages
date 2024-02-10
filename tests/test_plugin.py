import pathlib

import pytest

import poetry_plugin_export_packages


class TestExportOutput:
    @pytest.fixture
    def test_file(self, tmp_path):
        my_file = tmp_path / "test.txt"
        with my_file.open("w") as fout:
            fout.write("hello")
        return my_file

    @pytest.fixture
    def export_output(self, tmp_path):
        my_root = pathlib.Path(tmp_path / "export_out")
        my_root.mkdir()
        out_dir = my_root / "d1" / "d2" / "d3" / "out"
        out_dir.mkdir(parents=True)
        return poetry_plugin_export_packages.plugin.ExportOutput(
            out_dir=out_dir, rel_root=my_root
        )

    def test_save_file(self, tmp_path, test_file, export_output):
        out_fname1 = export_output.save_file(test_file)
        assert str(out_fname1) == str(
            tmp_path / "export_out" / "d1" / "d2" / "d3" / "out" / "test.txt"
        )
        out_fname2 = export_output.save_file(test_file)
        assert str(out_fname2) == str(
            tmp_path / "export_out" / "d1" / "d2" / "d3" / "out" / "test_2.txt"
        )

    def test_rel_path(self, test_file, export_output):
        out_fname = export_output.save_file(test_file)
        rel_path = export_output.to_rel_path(out_fname)
        assert str(rel_path) == "d1/d2/d3/out/test.txt"

    def test_pip_cmd(self, export_output):
        export_output.add_pip_command(["c1", "a1"])
        export_output.add_pip_command(["c2", "a2"])

        assert export_output.get_pip_script("#! shebang").splitlines() == [
            "#! shebang",
            "",
            "pip c1 a1",
            "pip c2 a2",
            "",
        ]