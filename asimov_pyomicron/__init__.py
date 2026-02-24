"""
Asimov integration for running PyOmicron.
"""

import os
from importlib import resources
import warnings

try:
    from asimov import config as asimov_config
except (ImportError, ModuleNotFoundError):
    asimov_config = None

try:
    from asimov.pipeline import Pipeline
except (ImportError, ModuleNotFoundError):
    # Create a minimal Pipeline placeholder if asimov is not installed
    # This allows the module to be imported for introspection
    class Pipeline:
        """Placeholder Pipeline class when asimov is not available."""
        @staticmethod
        def read_ini(path):
            import configparser
            parser = configparser.ConfigParser()
            parser.read(path)
            return parser

__version__ = "0.1.0"


class PyOmicron(Pipeline):
    """
    PyOmicron pipeline for Asimov.

    Provides config templating and scaffolding for submitting
    an Omicron event trigger generator job to an HTCondor scheduler.
    """

    # Path to the Liquid template used by Analysis.make_config
    try:
        _template_path = resources.files(__name__).joinpath("omicron.ini")
        config_template = str(_template_path)
    except (ImportError, AttributeError, FileNotFoundError):
        # Fallback: relative path within the package
        config_template = os.path.join(os.path.dirname(__file__), "omicron.ini")
    
    _pipeline_command = "omicron-process"
    name = "pyomicron"

    def __init__(self, production):
        # Asimov's Pipeline expects a Production/Analysis instance
        super().__init__(production)

    @property
    def channel_names(self):
        """Return PyOmicron channel-name string from production.meta.

        Supports either a single string at meta['data']['channel name'] or
        a mapping at meta['data']['channel names'] with keys of IFO codes.
        """
        data = self.production.meta.get("data", {})
        # Single string
        if isinstance(data.get("channel name"), str) and data.get("channel name").strip():
            return data.get("channel name")
        # Dict mapping: {"H1": "H1:STRAIN", "L1": "L1:STRAIN"}
        chan_map = data.get("channel names") or data.get("channels")
        if isinstance(chan_map, dict) and chan_map:
            parts = []
            for ifo, name in chan_map.items():
                # If value already includes IFO prefix, keep as-is
                if ":" in name:
                    parts.append(name)
                else:
                    parts.append(f"{ifo}:{name}")
            return "\n\t".join(parts)
        return ""

    def _get_channel_list(self):
        """Get a list of channel names from the channel_names property.
        
        Returns:
            list: List of non-empty channel names
        """
        channel_str = self.channel_names
        if not channel_str:
            return []
        channels = channel_str.split("\n\t")
        return [ch.strip() for ch in channels if ch.strip()]

    @property
    def frametype(self):
        """Return frame type from production.meta."""
        data = self.production.meta.get("data", {})
        return data.get("frametype", data.get("frame type", ""))

    def _get_omicron_param(self, key, default=None):
        """Helper to get omicron parameters supporting both hyphenated and underscore names.
        
        Args:
            key: Parameter name (will try both hyphenated and underscore versions)
            default: Default value if parameter not found
            
        Returns:
            Parameter value or default
        """
        omicron = self.production.meta.get("omicron", {})
        # Try hyphenated version first (blueprint style)
        hyphenated = key.replace("_", "-")
        if hyphenated in omicron:
            return omicron[hyphenated]
        # Try underscore version (Python style)
        if key in omicron:
            return omicron[key]
        return default

    @property
    def chunk_duration(self):
        """Get chunk duration parameter."""
        return self._get_omicron_param("chunk_duration", 124)

    @property
    def segment_duration(self):
        """Get segment duration parameter."""
        return self._get_omicron_param("segment_duration", 64)

    @property
    def overlap_duration(self):
        """Get overlap duration parameter."""
        return self._get_omicron_param("overlap_duration", 4)

    @property
    def frequency_range(self):
        """Get frequency range parameter."""
        return self._get_omicron_param("frequency_range", "4.0 8192.0")

    @property
    def q_range(self):
        """Get q-range parameter."""
        return self._get_omicron_param("q_range", "3.3166 150")

    @property
    def mismatch_max(self):
        """Get mismatch-max parameter."""
        return self._get_omicron_param("mismatch_max")

    @property
    def snr_threshold(self):
        """Get SNR threshold parameter."""
        return self._get_omicron_param("snr_threshold")

    @property
    def sample_frequency(self):
        """Get sample frequency parameter."""
        return self._get_omicron_param("sample_frequency")

    @property
    def state_flag(self):
        """Get state flag parameter."""
        return self._get_omicron_param("state_flag")

    @property
    def state_channel(self):
        """Get state channel parameter."""
        return self._get_omicron_param("state_channel")

    @property
    def state_frametype(self):
        """Get state frametype parameter."""
        return self._get_omicron_param("state_frametype")

    @property
    def state_bits(self):
        """Get state bits parameter."""
        return self._get_omicron_param("state_bits")

    def detect_completion(self):
        """
        Check for the production of trigger files to signal that a job has been completed.
        """
        rundir = getattr(self.production, "rundir", None)
        if not rundir:
            return False
        
        # Check for typical omicron output files
        channels = self._get_channel_list()
        for channel in channels:
            channel_dir = os.path.join(rundir, channel)
            if os.path.isdir(channel_dir):
                # Check for any trigger files
                for ext in [".root", ".xml", ".h5", ".hdf5"]:
                    trigger_files = [f for f in os.listdir(channel_dir) if f.endswith(ext)]
                    if trigger_files:
                        return True
        return False

    def build_dag(self):
        """
        Construct the command used to run ``omicron-process``.
        """
        # Build a basic command from the production context.
        ini = os.path.join(self.production.rundir or ".", f"{self.production.name}.ini")
        
        # Get GPS times
        gps_start = self.production.meta.get("data", {}).get("gps-start-time")
        gps_end = self.production.meta.get("data", {}).get("gps-end-time")
        
        command = [self._pipeline_command, ini]
        
        if gps_start and gps_end:
            command.extend(["--gps", f"{gps_start}-{gps_end}"])
        
        # Add other optional parameters from metadata
        condor_config = self.production.meta.get("omicron", {})
        
        if condor_config.get("online"):
            command.append("--online")
        
        if condor_config.get("skip-gps-checks"):
            command.append("--skip-gps-checks")
        
        self.logger.info(" ".join(command))
        return command

    def submit_dag(self):
        """
        Submit the DAG file to the cluster.
        """
        # Prefer HTCondor submission
        try:
            warnings.filterwarnings("ignore", module="htcondor2")
            import htcondor2 as htcondor
        except ImportError:
            warnings.filterwarnings("ignore", module="htcondor")
            import htcondor

        command = self.build_dag()
        rundir = getattr(self.production, "rundir", os.getcwd())
        out_base = os.path.join(rundir, self.production.name)

        # Build submit description
        submit_description = {
            "executable": command[0],
            "arguments": " ".join(command[1:]),
            "output": f"{out_base}.out",
            "error": f"{out_base}.err",
            "log": f"{out_base}.log",
            "request_cpus": str(self.production.meta.get("scheduler", {}).get("cpus", "1")),
            "environment": "HDF5_USE_FILE_LOCKING=FALSE OMP_NUM_THREADS=1 OMP_PROC_BIND=false",
            "getenv": "CONDA_EXE,USER,LAL*,PATH,HOME",
            "batch_name": f"PyOmicron/{self.production.event.name}/{self.production.name}",
            "request_memory": self.production.meta.get("scheduler", {}).get("memory", "4096MB"),
            "request_disk": self.production.meta.get("scheduler", {}).get("disk", "4096MB"),
            "+flock_local": "True",
            "+DESIRED_Sites": htcondor.classad.quote("nogrid"),
            "should_transfer_files": "YES",
            "when_to_transfer_output": "ON_EXIT_OR_EVICT",
        }

        # Optional accounting info
        accounting = self.production.meta.get("scheduler", {}).get("accounting group")
        if accounting:
            if asimov_config:
                submit_description["accounting_group_user"] = asimov_config.get("condor", "user")
            submit_description["accounting_group"] = accounting

        # Queue job
        hostname_job = htcondor.Submit(submit_description)

        try:
            # Use configured schedd if present
            if asimov_config:
                schedulers = htcondor.Collector().locate(
                    htcondor.DaemonTypes.Schedd, asimov_config.get("condor", "scheduler")
                )
                schedd = htcondor.Schedd(schedulers)
            else:
                raise RuntimeError("No asimov config available")
        except (RuntimeError, AttributeError, KeyError):
            schedd = htcondor.Schedd()

        with schedd.transaction() as txn:
            cluster_id = hostname_job.queue(txn)

        # Record job id
        self.production.job_id = cluster_id
        self.logger.info(f"Submitted PyOmicron job: {cluster_id}")
        return cluster_id

    def collect_assets(self):
        """
        Collect all of the output assets for this job.

        Returns a dict that includes a ``trigger list`` key mapping IFO codes
        (e.g. ``"H1"``, ``"L1"``) to lists of trigger file paths.  This is
        the standard key that downstream analyses (e.g. asimov-pastro) use to
        locate glitch trigger files.
        """
        assets = {}
        rundir = getattr(self.production, "rundir", None)
        if not rundir or not os.path.isdir(rundir):
            return assets

        trigger_extensions = {".root", ".xml", ".h5", ".hdf5"}

        # Collect trigger files from channel directories, grouped by IFO.
        # Channel names look like "H1:GDS-CALIB_STRAIN"; the IFO is the
        # two-character prefix before the colon.
        channels = self._get_channel_list()
        trigger_list = {}
        for channel in channels:
            ifo = channel.split(":")[0] if ":" in channel else channel[:2]
            channel_dir = os.path.join(rundir, channel)
            if not os.path.isdir(channel_dir):
                continue
            for fname in os.listdir(channel_dir):
                fpath = os.path.join(channel_dir, fname)
                if not os.path.isfile(fpath):
                    continue
                assets[f"{channel}/{fname}"] = fpath
                if os.path.splitext(fname)[1] in trigger_extensions:
                    trigger_list.setdefault(ifo, []).append(fpath)

        if trigger_list:
            assets["trigger list"] = trigger_list

        # Collect log files
        for fname in [
            f"{self.production.name}.log",
            f"{self.production.name}.out",
            f"{self.production.name}.err",
        ]:
            fpath = os.path.join(rundir, fname)
            if os.path.exists(fpath):
                assets[fname] = fpath

        return assets

    def after_completion(self):
        """
        A hook to be run after the pipeline is detected to have completed.
        """
        self.production.status = "finished"

    def collect_logs(self):
        """
        Collect all of the log files produced by this pipeline and return their contents as a dictionary.
        """
        logs = {}
        rundir = getattr(self.production, "rundir", None)
        if not rundir:
            return logs
        
        for fname in [
            f"{self.production.name}.out",
            f"{self.production.name}.err",
            f"{self.production.name}.log"
        ]:
            fpath = os.path.join(rundir, fname)
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r") as fh:
                        logs[fname] = fh.read()
                except (IOError, OSError, UnicodeDecodeError):
                    continue
        return logs

    def check_progress(self):
        """
        Return the progress of this job.
        """
        return {"completed": self.detect_completion()}

    def read_ini(self):
        """
        Read and parse a configuration file for this pipeline.
        """
        ini = os.path.join(self.production.rundir or ".", f"{self.production.name}.ini")
        parser = Pipeline.read_ini(ini)
        return parser
