"""
End-to-end test for PyOmicron pipeline using HTCondor and GW150914 data.

This test requires:
- asimov to be installed
- htcondor to be available
- Access to GW150914 data (or mock data)
"""

import os
import shutil
import tempfile
import time
import unittest

try:
    from asimov.event import Event
    from asimov.analysis import SimpleAnalysis
    from asimov_pyomicron import PyOmicron
    ASIMOV_AVAILABLE = True
except ImportError:
    ASIMOV_AVAILABLE = False

try:
    import htcondor2 as htcondor
except ImportError:
    try:
        import htcondor
    except ImportError:
        htcondor = None

# GW150914 parameters
GW150914_GPS_TIME = 1126259462
GW150914_DURATION = 32  # seconds around the event


@unittest.skipUnless(ASIMOV_AVAILABLE, "asimov not available")
@unittest.skipUnless(htcondor is not None, "htcondor not available")
class TestPyOmicronEndToEnd(unittest.TestCase):
    """
    End-to-end tests for PyOmicron pipeline with HTCondor submission.
    
    These tests create actual HTCondor job submissions and verify the
    pipeline works correctly. They are marked as integration tests and
    may require special permissions or infrastructure.
    """

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp(prefix="pyomicron_test_")
        self.rundir = os.path.join(self.test_dir, "run")
        os.makedirs(self.rundir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_config_generation_gw150914(self):
        """Test configuration file generation for GW150914."""
        event = Event(name="GW150914")
        
        analysis = SimpleAnalysis(
            subject=event,
            name="GW150914_Omicron",
            pipeline="pyomicron",
            interferometers=["H1", "L1"],
            rundir=self.rundir,
            data={
                "gps-start-time": GW150914_GPS_TIME - 16,
                "gps-end-time": GW150914_GPS_TIME + 16,
                "channel names": {
                    "H1": "H1:GDS-CALIB_STRAIN",
                    "L1": "L1:GDS-CALIB_STRAIN"
                },
                "frametype": "H1_HOFT_C00"
            },
            omicron={
                "chunk_duration": 124,
                "segment_duration": 64,
                "overlap_duration": 4,
                "frequency_range": "4.0 2048.0",
                "q_range": "3.3166 150",
                "snr_threshold": 5.5,
                "sample_frequency": 4096,
            }
        )
        
        # Generate config file
        cfg_path = os.path.join(self.rundir, "GW150914_Omicron.ini")
        analysis.make_config(cfg_path)
        
        # Verify config file exists
        self.assertTrue(os.path.exists(cfg_path))
        
        # Verify config contains expected sections and values
        from asimov.pipeline import Pipeline
        parser = Pipeline.read_ini(cfg_path)
        
        # Check section exists
        self.assertTrue(parser.has_section("GW150914_Omicron"))
        
        # Check critical parameters
        self.assertTrue(parser.has_option("GW150914_Omicron", "channels"))
        self.assertTrue(parser.has_option("GW150914_Omicron", "frametype"))
        self.assertTrue(parser.has_option("GW150914_Omicron", "chunk-duration"))
        
        # Verify channel names
        channels = parser.get("GW150914_Omicron", "channels")
        self.assertIn("H1:GDS-CALIB_STRAIN", channels)
        self.assertIn("L1:GDS-CALIB_STRAIN", channels)
        
        # Verify timing parameters
        self.assertEqual(parser.get("GW150914_Omicron", "chunk-duration"), "124")
        self.assertEqual(parser.get("GW150914_Omicron", "segment-duration"), "64")
        self.assertEqual(parser.get("GW150914_Omicron", "overlap-duration"), "4")

    def test_command_building_gw150914(self):
        """Test that the omicron-process command is built correctly."""
        event = Event(name="GW150914")
        
        analysis = SimpleAnalysis(
            subject=event,
            name="GW150914_Omicron",
            pipeline="pyomicron",
            interferometers=["H1", "L1"],
            rundir=self.rundir,
            data={
                "gps-start-time": GW150914_GPS_TIME - 16,
                "gps-end-time": GW150914_GPS_TIME + 16,
                "channel names": {
                    "H1": "H1:GDS-CALIB_STRAIN",
                    "L1": "L1:GDS-CALIB_STRAIN"
                },
                "frametype": "H1_HOFT_C00"
            }
        )
        
        # Build command
        cmd = analysis.pipeline.build_dag()
        
        # Verify command structure
        self.assertEqual(cmd[0], "omicron-process")
        self.assertTrue(cmd[1].endswith(".ini"))
        self.assertIn("--gps", cmd)
        
        # Find GPS argument
        gps_idx = cmd.index("--gps")
        gps_range = cmd[gps_idx + 1]
        self.assertIn(str(GW150914_GPS_TIME - 16), gps_range)
        self.assertIn(str(GW150914_GPS_TIME + 16), gps_range)

    @unittest.skipUnless(
        os.environ.get("ASIMOV_TEST_CONDOR") == "1",
        "Set ASIMOV_TEST_CONDOR=1 to enable HTCondor submission tests"
    )
    def test_htcondor_submission_gw150914(self):
        """
        Test actual HTCondor job submission for GW150914.
        
        This test is skipped by default. Set ASIMOV_TEST_CONDOR=1 to enable.
        Requires access to HTCondor scheduler and GW150914 data.
        """
        event = Event(name="GW150914")
        
        analysis = SimpleAnalysis(
            subject=event,
            name="GW150914_Omicron_Test",
            pipeline="pyomicron",
            interferometers=["H1", "L1"],
            rundir=self.rundir,
            data={
                "gps-start-time": GW150914_GPS_TIME - 16,
                "gps-end-time": GW150914_GPS_TIME + 16,
                "channel names": {
                    "H1": "H1:GDS-CALIB_STRAIN",
                    "L1": "L1:GDS-CALIB_STRAIN"
                },
                "frametype": "H1_HOFT_C00"
            },
            omicron={
                "chunk_duration": 124,
                "segment_duration": 64,
                "overlap_duration": 4,
                "frequency_range": "4.0 2048.0",
                "q_range": "3.3166 150",
            },
            scheduler={
                "cpus": 1,
                "memory": "2048MB",
                "disk": "2048MB"
            }
        )
        
        # Generate config
        cfg_path = os.path.join(self.rundir, "GW150914_Omicron_Test.ini")
        analysis.make_config(cfg_path)
        
        try:
            # Submit job
            cluster_id = analysis.pipeline.submit_dag()
            
            # Verify we got a cluster ID
            self.assertIsNotNone(cluster_id)
            self.assertIsInstance(cluster_id, int)
            
            # Verify job was recorded
            self.assertEqual(analysis.job_id, cluster_id)
            
            # Query HTCondor to verify job exists
            schedd = htcondor.Schedd()
            jobs = schedd.query(
                constraint=f"ClusterId == {cluster_id}",
                projection=["ClusterId", "JobStatus", "Cmd"]
            )
            
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0]["ClusterId"], cluster_id)
            
            # Optionally, wait a bit and check status
            # This is commented out to keep test fast
            # time.sleep(5)
            # progress = analysis.pipeline.check_progress()
            # self.assertIn("completed", progress)
            
        finally:
            # Clean up: remove the job if it was submitted
            if hasattr(analysis.pipeline, "production") and \
               hasattr(analysis.pipeline.production, "job_id") and \
               analysis.pipeline.production.job_id:
                try:
                    schedd = htcondor.Schedd()
                    schedd.act(
                        htcondor.JobAction.Remove,
                        f"ClusterId == {analysis.pipeline.production.job_id}"
                    )
                except Exception:
                    pass  # Best effort cleanup

    def test_completion_detection_with_mock_output(self):
        """Test completion detection with mock trigger files."""
        event = Event(name="GW150914")
        
        analysis = SimpleAnalysis(
            subject=event,
            name="GW150914_Mock",
            pipeline="pyomicron",
            interferometers=["H1"],
            rundir=self.rundir,
            data={
                "channel names": {"H1": "H1:GDS-CALIB_STRAIN"},
            }
        )
        
        # Initially should not be complete
        self.assertFalse(analysis.pipeline.detect_completion())
        
        # Create mock trigger output
        channel = "H1:GDS-CALIB_STRAIN"
        channel_dir = os.path.join(self.rundir, channel)
        os.makedirs(channel_dir, exist_ok=True)
        
        # Create mock ROOT file
        trigger_file = os.path.join(
            channel_dir,
            f"H1_GDS-CALIB_STRAIN_OMICRON-{GW150914_GPS_TIME}-32.root"
        )
        with open(trigger_file, "w") as f:
            f.write("mock trigger data")
        
        # Now should detect completion
        self.assertTrue(analysis.pipeline.detect_completion())
        
        # Test asset collection
        assets = analysis.pipeline.collect_assets()
        self.assertTrue(len(assets) > 0)
        self.assertTrue(any("OMICRON" in key for key in assets.keys()))

    def test_channel_list_helper(self):
        """Test the _get_channel_list helper method."""
        event = Event(name="GW150914")
        
        # Test with dict of channels
        analysis = SimpleAnalysis(
            subject=event,
            name="Test",
            pipeline="pyomicron",
            interferometers=["H1", "L1"],
            data={
                "channel names": {
                    "H1": "H1:GDS-CALIB_STRAIN",
                    "L1": "L1:GDS-CALIB_STRAIN"
                }
            }
        )
        
        channels = analysis.pipeline._get_channel_list()
        self.assertEqual(len(channels), 2)
        self.assertIn("H1:GDS-CALIB_STRAIN", channels)
        self.assertIn("L1:GDS-CALIB_STRAIN", channels)
        
        # Test with single channel name
        analysis2 = SimpleAnalysis(
            subject=event,
            name="Test2",
            pipeline="pyomicron",
            interferometers=["H1"],
            data={"channel name": "H1:GDS-CALIB_STRAIN"}
        )
        
        channels2 = analysis2.pipeline._get_channel_list()
        self.assertEqual(len(channels2), 1)
        self.assertEqual(channels2[0], "H1:GDS-CALIB_STRAIN")
        
        # Test with empty channels
        analysis3 = SimpleAnalysis(
            subject=event,
            name="Test3",
            pipeline="pyomicron",
            interferometers=["H1"],
            data={}
        )
        
        channels3 = analysis3.pipeline._get_channel_list()
        self.assertEqual(len(channels3), 0)


if __name__ == '__main__':
    unittest.main()
