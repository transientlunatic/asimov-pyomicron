# asimov-pyomicron

An Asimov plugin for running PyOmicron event trigger generation on HTCondor clusters.

## Overview

This plugin enables [Asimov](https://github.com/etive-io/asimov) to submit and manage `omicron-process` jobs for gravitational wave event trigger generation. It provides:

- **Configuration templating**: Generates `omicron-process` config files using Liquid templates with dynamic field population from analysis metadata
- **HTCondor integration**: Submits jobs to HTCondor schedulers with appropriate resource requests and output transfer
- **Status tracking**: Monitors job completion via output file detection
- **Asset management**: Collects trigger files, logs, and other artifacts

## Installation

You can install `asimov-pyomicron` using pip:

```bash
pip install asimov-pyomicron
```

Or install from source:

```bash
git clone https://github.com/transientlunatic/asimov-pyomicron.git
cd asimov-pyomicron
pip install .
```

## Usage

Once installed, the `pyomicron` pipeline will be automatically registered with Asimov through the entry point system.

### Configuration

In your Asimov ledger or production configuration, you can specify PyOmicron-specific settings in the metadata:

```yaml
productions:
  - name: omicron-analysis
    pipeline: pyomicron
    comment: Omicron event trigger generation
    meta:
      data:
        channel names:
          H1: "H1:GDS-CALIB_STRAIN"
          L1: "L1:GDS-CALIB_STRAIN"
        frametype: "H1_HOFT_C00"
        gps-start-time: 1234567890
        gps-end-time: 1234568890
      omicron:
        chunk_duration: 124
        segment_duration: 64
        overlap_duration: 4
        frequency_range: "4.0 8192.0"
        q_range: "3.3166 150"
        mismatch_max: 0.2
        snr_threshold: 5
        sample_frequency: 16384
        state_flag: "H1:DMT-CALIBRATED:1"
      scheduler:
        accounting group: "ligo.prod.o4.detchar.transient.omicron"
        cpus: 1
        memory: "4096MB"
        disk: "4096MB"
```

### Configuration Parameters

#### Data Parameters
- `channel names`: Dictionary mapping IFO codes to channel names (e.g., `{"H1": "H1:GDS-CALIB_STRAIN"}`)
- `frametype`: Frame type name for data files
- `gps-start-time`: GPS start time for processing
- `gps-end-time`: GPS end time for processing

#### Omicron Parameters
- `chunk_duration`: Duration of data (seconds) for PSD estimation (default: 124)
- `segment_duration`: Duration of data (seconds) for FFT (default: 64)
- `overlap_duration`: Overlap (seconds) between neighbouring segments and chunks (default: 4)
- `frequency_range`: Low and high frequency limits for the search (default: "4.0 8192.0")
- `q_range`: Low and high Q-factor limits for the search (default: "3.3166 150")
- `mismatch_max`: Maximum distance between (Q, f) tiles (optional)
- `snr_threshold`: Minimum SNR for recorded triggers (optional)
- `sample_frequency`: Sample frequency in Hz (optional)
- `state_flag`: Data-quality flag defining active state segments (optional)

Alternative state definition (if not using `state_flag`):
- `state_channel`: Name of data channel defining active state
- `state_frametype`: Frame type name for the state channel
- `state_bits`: Comma-separated list of bit numbers that define active state

## Dependencies

- `asimov>=0.5`
- `pyomicron>=2.0`
- `liquid>=4.0`
- Python >= 3.9

## Contributing

Contributions are welcome! Please submit issues or pull requests to the [repository](https://github.com/transientlunatic/asimov-pyomicron).

## Related Projects

- [Asimov](https://github.com/etive-io/asimov) - The main workflow management system
- [PyOmicron](https://github.com/gwpy/pyomicron) - Python utilities for the Omicron event trigger generator
- [asimov-pycbc](https://github.com/etive-io/asimov-pycbc) - Asimov plugin for PyCBC Inference
- [asimov-gwdata](https://github.com/etive-io/asimov-gwdata) - Asimov utilities for gravitational wave data management

## License

This project follows the licensing of the parent Asimov project.
