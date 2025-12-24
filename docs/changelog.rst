Changelog
=========

Version 0.1.0 (TBD)
-------------------

Initial release of asimov-pyomicron.

Features
~~~~~~~~

- PyOmicron pipeline class inheriting from asimov.pipeline.Pipeline
- Configuration file templating using Liquid
- HTCondor job submission support
- Automatic completion detection via trigger file monitoring
- Asset collection for trigger files and logs
- Support for both hyphenated (blueprint) and underscore (Python) parameter naming
- Comprehensive documentation with Sphinx
- Example blueprint files for common use cases
- Full test suite including end-to-end tests with GW150914 data

API
~~~

- ``PyOmicron`` class with methods:
  - ``detect_completion()``: Check for job completion
  - ``build_dag()``: Build omicron-process command
  - ``submit_dag()``: Submit job to HTCondor
  - ``collect_assets()``: Collect output files
  - ``collect_logs()``: Collect log files
  - ``check_progress()``: Get job progress
  - ``after_completion()``: Post-completion hook
  - ``read_ini()``: Read configuration file

Properties
~~~~~~~~~~

- ``channel_names``: Channel names for processing
- ``frametype``: Frame type for data
- ``chunk_duration``: PSD chunk duration
- ``segment_duration``: FFT segment duration
- ``overlap_duration``: Segment overlap
- ``frequency_range``: Frequency search range
- ``q_range``: Q-factor search range
- ``mismatch_max``: Maximum tile mismatch
- ``snr_threshold``: SNR threshold for triggers
- ``sample_frequency``: Data sample frequency
- ``state_flag``: Data quality flag
- ``state_channel``: State channel (alternative to flag)
- ``state_frametype``: State channel frame type
- ``state_bits``: State channel bit mask

Configuration
~~~~~~~~~~~~~

Supports configuration through:
- Blueprint YAML files
- Asimov ledger files
- Direct Python API

Documentation
~~~~~~~~~~~~~

- Complete user guide
- API reference
- Configuration guide
- Examples and tutorials
- Contributing guide
