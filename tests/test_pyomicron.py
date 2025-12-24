import unittest
import os

try:
    from asimov.event import Event
    from asimov.analysis import SimpleAnalysis
    from asimov.pipeline import Pipeline
    from asimov_pyomicron import PyOmicron
    ASIMOV_AVAILABLE = True
except ImportError:
    ASIMOV_AVAILABLE = False


@unittest.skipUnless(ASIMOV_AVAILABLE, "asimov not available")
class TestPyOmicronIntegration(unittest.TestCase):

    def test_make_config(self):
        """Check that asimov can make a config file for pyomicron."""
        subject = Event(name="GW150914")
        analysis = SimpleAnalysis(
            subject=subject,
            name="Test1",
            pipeline="pyomicron",
            interferometers=["L1", "H1"]
        )
        cfg_path = "test.ini"
        analysis.make_config(cfg_path)
        self.assertTrue(os.path.exists(cfg_path))
        # Parse config to ensure it is a valid INI
        parser = Pipeline.read_ini(cfg_path)
        self.assertTrue(parser.has_section("Test1"))
        os.remove(cfg_path)

    def test_submit_description(self):
        """Ensure submit description can be built and job submission invoked."""
        subject = Event(name="GW150914")
        analysis = SimpleAnalysis(
            subject=subject,
            name="TestSubmit",
            pipeline="pyomicron",
            interferometers=["L1", "H1"],
            rundir=".",
            data={"gps-start-time": 1126259462, "gps-end-time": 1126259562}
        )

        # Build command and ensure contains omicron-process and ini
        cmd = analysis.pipeline.build_dag()
        self.assertIn("omicron-process", cmd[0])
        self.assertTrue(cmd[1].endswith(".ini"))

    def test_completion_and_assets(self):
        """Test completion detection and asset collection."""
        subject = Event(name="GW150914")
        analysis = SimpleAnalysis(
            subject=subject,
            name="TestComplete",
            pipeline="pyomicron",
            interferometers=["L1", "H1"],
            rundir="."
        )
        
        # Initially should not be complete
        self.assertFalse(analysis.pipeline.detect_completion())
        
        # Create dummy output to simulate completion
        channel = "H1:GDS-CALIB_STRAIN"
        channel_dir = os.path.join(".", channel)
        os.makedirs(channel_dir, exist_ok=True)
        out_file = os.path.join(channel_dir, "H1_OMICRON-1126259462-100.root")
        with open(out_file, "w") as fh:
            fh.write("dummy")
        
        # Now should detect completion
        self.assertTrue(analysis.pipeline.detect_completion())
        
        # Check assets collection
        assets = analysis.pipeline.collect_assets()
        self.assertTrue(any("OMICRON" in key for key in assets.keys()))
        
        # Cleanup
        os.remove(out_file)
        os.rmdir(channel_dir)

    def test_channel_names_property(self):
        """Test channel_names property with different formats."""
        subject = Event(name="GW150914")
        
        # Test with single channel name
        analysis1 = SimpleAnalysis(
            subject=subject,
            name="TestChannel1",
            pipeline="pyomicron",
            interferometers=["H1"],
            data={"channel name": "H1:GDS-CALIB_STRAIN"}
        )
        channels1 = analysis1.pipeline.channel_names
        self.assertIn("H1:GDS-CALIB_STRAIN", channels1)
        
        # Test with channel names dict
        analysis2 = SimpleAnalysis(
            subject=subject,
            name="TestChannel2",
            pipeline="pyomicron",
            interferometers=["H1", "L1"],
            data={"channel names": {"H1": "H1:GDS-CALIB_STRAIN", "L1": "L1:GDS-CALIB_STRAIN"}}
        )
        channels2 = analysis2.pipeline.channel_names
        self.assertIn("H1:GDS-CALIB_STRAIN", channels2)
        self.assertIn("L1:GDS-CALIB_STRAIN", channels2)


class TestPyOmicronBasic(unittest.TestCase):
    """Basic tests that don't require asimov to be installed."""

    def test_import(self):
        """Test that the module can be imported."""
        try:
            from asimov_pyomicron import PyOmicron
            self.assertIsNotNone(PyOmicron)
        except ImportError as e:
            # If asimov is not installed, that's expected
            if "asimov" not in str(e):
                raise

    def test_config_template_exists(self):
        """Test that the config template file exists."""
        try:
            from asimov_pyomicron import PyOmicron
        except ImportError:
            self.skipTest("asimov not available")
        # The template path should be set
        self.assertTrue(hasattr(PyOmicron, 'config_template'))
        # Check that template file exists in the package
        template_path = PyOmicron.config_template
        # If it's a relative path, it should exist relative to the package
        if not os.path.isabs(template_path):
            import asimov_pyomicron
            package_dir = os.path.dirname(asimov_pyomicron.__file__)
            template_path = os.path.join(package_dir, os.path.basename(template_path))
        self.assertTrue(os.path.exists(template_path), f"Template not found at {template_path}")

    def test_pipeline_name(self):
        """Test that the pipeline has the correct name."""
        try:
            from asimov_pyomicron import PyOmicron
            self.assertEqual(PyOmicron.name, "pyomicron")
        except ImportError:
            self.skipTest("asimov not available")


if __name__ == '__main__':
    unittest.main()
