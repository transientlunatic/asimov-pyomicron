Examples
========

This page provides complete examples of using asimov-pyomicron in various scenarios.

Example 1: GW150914 Event Triggers
-----------------------------------

This example shows how to generate event triggers for the GW150914 gravitational wave event.

Configuration file
~~~~~~~~~~~~~~~~~~

Create a configuration file ``gw150914_omicron.yaml``:

.. code-block:: yaml

   kind: analysis
   name: GW150914
   productions:
     - name: GW150914_omicron_H1L1
       pipeline: pyomicron
       comment: Omicron event triggers for GW150914
       interferometers: [H1, L1]
       meta:
         data:
           channel names:
             H1: "H1:GDS-CALIB_STRAIN"
             L1: "L1:GDS-CALIB_STRAIN"
           frametype: "H1_HOFT_C00"
           gps-start-time: 1126259446
           gps-end-time: 1126259478
         omicron:
           chunk_duration: 124
           segment_duration: 64
           overlap_duration: 4
           frequency_range: "4.0 2048.0"
           q_range: "3.3166 150"
           snr_threshold: 5.5
           sample_frequency: 4096

Python script
~~~~~~~~~~~~~

.. code-block:: python

   from asimov.event import Event
   from asimov.analysis import SimpleAnalysis

   # Create event
   event = Event(name="GW150914")

   # Create analysis
   analysis = SimpleAnalysis(
       subject=event,
       name="GW150914_omicron",
       pipeline="pyomicron",
       interferometers=["H1", "L1"],
       rundir="/path/to/run/directory",
       data={
           "gps-start-time": 1126259446,
           "gps-end-time": 1126259478,
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

   # Generate configuration
   analysis.make_config("GW150914_omicron.ini")

   # Submit to HTCondor
   cluster_id = analysis.pipeline.submit_dag()
   print(f"Submitted job: {cluster_id}")

   # Monitor progress
   import time
   while not analysis.pipeline.detect_completion():
       print("Job still running...")
       time.sleep(60)

   print("Job completed!")
   assets = analysis.pipeline.collect_assets()
   print(f"Collected {len(assets)} files")

Example 2: Continuous Monitoring
---------------------------------

This example shows how to set up continuous monitoring for detector characterization.

.. code-block:: python

   from asimov.event import Event
   from asimov.analysis import SimpleAnalysis
   import time

   # Create event for continuous run
   event = Event(name="O4_monitoring")

   # Create analysis for latest data
   analysis = SimpleAnalysis(
       subject=event,
       name="continuous_omicron",
       pipeline="pyomicron",
       interferometers=["H1", "L1", "V1"],
       rundir="/path/to/monitoring",
       data={
           "channel names": {
               "H1": "H1:GDS-CALIB_STRAIN",
               "L1": "L1:GDS-CALIB_STRAIN",
               "V1": "V1:Hrec_hoft_16384Hz"
           },
           "frametype": "H1_HOFT_C00"
       },
       omicron={
           "chunk_duration": 124,
           "segment_duration": 64,
           "overlap_duration": 4,
           "frequency_range": "4.0 8192.0",
           "q_range": "3.3166 150",
           "snr_threshold": 5.0,
           "sample_frequency": 16384,
           "online": True  # Use online mode
       }
   )

   # Generate and submit
   analysis.make_config("continuous_omicron.ini")
   cluster_id = analysis.pipeline.submit_dag()
   print(f"Monitoring job submitted: {cluster_id}")

Example 3: Custom State Flags
------------------------------

This example demonstrates using custom data quality flags.

.. code-block:: python

   from asimov.event import Event
   from asimov.analysis import SimpleAnalysis

   event = Event(name="CustomDQ_analysis")

   analysis = SimpleAnalysis(
       subject=event,
       name="custom_dq_omicron",
       pipeline="pyomicron",
       interferometers=["H1"],
       rundir="/path/to/output",
       data={
           "gps-start-time": 1234567890,
           "gps-end-time": 1234568890,
           "channel names": {"H1": "H1:GDS-CALIB_STRAIN"},
           "frametype": "H1_HOFT_C00"
       },
       omicron={
           "chunk_duration": 124,
           "segment_duration": 64,
           "overlap_duration": 4,
           "frequency_range": "10.0 2048.0",
           "q_range": "3.3166 100",
           "snr_threshold": 6.0,
           # Use custom state flag
           "state_flag": "H1:DMT-ANALYSIS_READY:1",
       }
   )

   analysis.make_config("custom_dq_omicron.ini")
   cluster_id = analysis.pipeline.submit_dag()

Example 4: Processing Multiple Channels
----------------------------------------

Process different channels independently.

.. code-block:: python

   from asimov.event import Event
   from asimov.analysis import SimpleAnalysis

   event = Event(name="MultiChannel")

   # Define channels to process
   channels = {
       "H1": "H1:GDS-CALIB_STRAIN",
       "H1_AUX": "H1:ASC-AS_B_RF45_Q_YAW_OUT_DQ",
       "L1": "L1:GDS-CALIB_STRAIN",
       "L1_AUX": "L1:ASC-AS_B_RF45_Q_YAW_OUT_DQ"
   }

   for name, channel in channels.items():
       analysis = SimpleAnalysis(
           subject=event,
           name=f"omicron_{name}",
           pipeline="pyomicron",
           interferometers=[name.split("_")[0]],
           rundir=f"/path/to/{name}",
           data={
               "gps-start-time": 1234567890,
               "gps-end-time": 1234568890,
               "channel name": channel,
               "frametype": "H1_R" if "AUX" in name else "H1_HOFT_C00"
           },
           omicron={
               "chunk_duration": 124,
               "segment_duration": 64,
               "overlap_duration": 4,
               "frequency_range": "4.0 2048.0",
               "q_range": "3.3166 150",
               "snr_threshold": 5.0,
           }
       )
       
       analysis.make_config(f"omicron_{name}.ini")
       cluster_id = analysis.pipeline.submit_dag()
       print(f"Submitted {name}: {cluster_id}")

Example 5: Collecting and Analyzing Results
--------------------------------------------

After jobs complete, collect and analyze the trigger files.

.. code-block:: python

   from asimov.event import Event
   from asimov.analysis import SimpleAnalysis
   import glob

   # Assuming analysis was already run
   event = Event(name="GW150914")
   analysis = SimpleAnalysis(
       subject=event,
       name="GW150914_omicron",
       pipeline="pyomicron",
       interferometers=["H1", "L1"],
       rundir="/path/to/run/directory"
   )

   # Check completion
   if analysis.pipeline.detect_completion():
       # Collect all assets
       assets = analysis.pipeline.collect_assets()
       
       print(f"Total files: {len(assets)}")
       
       # Filter for specific file types
       root_files = {k: v for k, v in assets.items() if k.endswith('.root')}
       xml_files = {k: v for k, v in assets.items() if k.endswith('.xml')}
       hdf5_files = {k: v for k, v in assets.items() if k.endswith('.h5')}
       
       print(f"ROOT files: {len(root_files)}")
       print(f"XML files: {len(xml_files)}")
       print(f"HDF5 files: {len(hdf5_files)}")
       
       # Read triggers from HDF5 files (example with gwpy)
       from gwpy.table import EventTable
       
       all_triggers = []
       for path in hdf5_files.values():
           triggers = EventTable.read(path, format='hdf5')
           all_triggers.append(triggers)
       
       if all_triggers:
           combined = EventTable.vstack(all_triggers)
           print(f"Total triggers: {len(combined)}")
           
           # Filter high SNR triggers
           high_snr = combined[combined['snr'] > 10]
           print(f"High SNR triggers: {len(high_snr)}")
