# PyOmicron Blueprint Examples

This directory contains example blueprint files for using the PyOmicron pipeline with Asimov.

## Available Blueprints

### gw150914-omicron.yaml
Event trigger generation for the GW150914 gravitational wave event. Demonstrates:
- Multi-detector configuration (H1, L1)
- GPS time window specification
- Standard omicron parameters
- HTCondor scheduler settings

### continuous-monitoring.yaml
Continuous omicron monitoring for detector characterization. Demonstrates:
- Three-detector setup (H1, L1, V1)
- Online processing mode
- Extended frequency range
- Production-level resource requests

### custom-dq.yaml
Omicron with custom data quality flags. Demonstrates:
- Single detector processing
- Custom state flags
- Adjusted frequency and Q ranges
- Minimal resource configuration

## Using Blueprints

To use a blueprint with Asimov:

```bash
asimov apply blueprints/gw150914-omicron.yaml
```

Or include it in your ledger file:

```yaml
kind: ledger
productions:
  - !include blueprints/gw150914-omicron.yaml
```

## Blueprint Structure

All PyOmicron blueprints follow this structure:

```yaml
kind: analysis
name: <analysis-name>
pipeline: pyomicron
comment: <description>
data:
  gps-start-time: <start-gps>     # Optional for continuous
  gps-end-time: <end-gps>         # Optional for continuous
  channels:                        # Dict of IFO: channel-name
    H1: H1:GDS-CALIB_STRAIN
  frametype: <frame-type>
omicron:
  chunk-duration: 124              # PSD estimation window
  segment-duration: 64             # FFT segment length
  overlap-duration: 4              # Segment overlap
  frequency-range: 4.0 8192.0      # Search frequency range
  q-range: 3.3166 150              # Q-factor range
  snr-threshold: 5.0               # Optional SNR threshold
  sample-frequency: 16384          # Optional sample rate
  state-flag: <dq-flag>            # Optional DQ flag
  online: true                     # Optional online mode
scheduler:
  accounting-group: <group>        # Optional HTCondor accounting
  cpus: 1
  memory: 4096MB
  disk: 4096MB
```

## Parameter Naming

PyOmicron supports both hyphenated (blueprint-style) and underscore (Python-style) parameter names:

- `chunk-duration` or `chunk_duration`
- `segment-duration` or `segment_duration`
- `frequency-range` or `frequency_range`

Hyphenated names are preferred in YAML blueprints for consistency with other Asimov pipelines.
