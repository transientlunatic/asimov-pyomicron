Quick Start
===========

This guide will help you get started with asimov-pyomicron quickly.

Basic Usage
-----------

Once installed, the PyOmicron pipeline is automatically registered with Asimov and can be used in your workflow configurations.

Creating a production
~~~~~~~~~~~~~~~~~~~~~

In your Asimov ledger or production configuration file, you can define a PyOmicron production:

.. code-block:: yaml

   productions:
     - name: omicron-H1
       pipeline: pyomicron
       comment: Omicron event trigger generation for H1
       interferometers: [H1]
       meta:
         data:
           channel names:
             H1: "H1:GDS-CALIB_STRAIN"
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

Configuration file generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asimov will automatically generate the PyOmicron configuration file using the Liquid template:

.. code-block:: python

   from asimov.event import Event
   from asimov.analysis import SimpleAnalysis

   event = Event(name="GW150914")
   analysis = SimpleAnalysis(
       subject=event,
       name="omicron-analysis",
       pipeline="pyomicron",
       interferometers=["H1", "L1"]
   )
   
   # Generate configuration file
   analysis.make_config("omicron-analysis.ini")

Job submission
~~~~~~~~~~~~~~

Submit the job to HTCondor:

.. code-block:: python

   # Submit to HTCondor
   cluster_id = analysis.pipeline.submit_dag()
   print(f"Submitted job {cluster_id}")

Monitoring progress
~~~~~~~~~~~~~~~~~~~

Check the status of your job:

.. code-block:: python

   # Check if completed
   if analysis.pipeline.detect_completion():
       print("Job completed!")
       
       # Collect output files
       assets = analysis.pipeline.collect_assets()
       print(f"Collected {len(assets)} output files")

Next steps
----------

- Read the :doc:`configuration` guide for detailed parameter descriptions
- See :doc:`examples` for more complete examples
- Check the :doc:`api/pipeline` reference for all available methods
