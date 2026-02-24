PyOmicron Pipeline API
======================

.. automodule:: asimov_pyomicron
   :members:
   :undoc-members:
   :show-inheritance:

PyOmicron Class
---------------

.. autoclass:: asimov_pyomicron.PyOmicron
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Properties
~~~~~~~~~~

.. autoproperty:: asimov_pyomicron.PyOmicron.channel_names
.. autoproperty:: asimov_pyomicron.PyOmicron.frametype
.. autoproperty:: asimov_pyomicron.PyOmicron.chunk_duration
.. autoproperty:: asimov_pyomicron.PyOmicron.segment_duration
.. autoproperty:: asimov_pyomicron.PyOmicron.overlap_duration
.. autoproperty:: asimov_pyomicron.PyOmicron.frequency_range
.. autoproperty:: asimov_pyomicron.PyOmicron.q_range
.. autoproperty:: asimov_pyomicron.PyOmicron.mismatch_max
.. autoproperty:: asimov_pyomicron.PyOmicron.snr_threshold
.. autoproperty:: asimov_pyomicron.PyOmicron.sample_frequency
.. autoproperty:: asimov_pyomicron.PyOmicron.state_flag
.. autoproperty:: asimov_pyomicron.PyOmicron.state_channel
.. autoproperty:: asimov_pyomicron.PyOmicron.state_frametype
.. autoproperty:: asimov_pyomicron.PyOmicron.state_bits

Methods
~~~~~~~

.. automethod:: asimov_pyomicron.PyOmicron.detect_completion
.. automethod:: asimov_pyomicron.PyOmicron.build_dag
.. automethod:: asimov_pyomicron.PyOmicron.submit_dag
.. automethod:: asimov_pyomicron.PyOmicron.collect_assets
.. automethod:: asimov_pyomicron.PyOmicron.collect_logs
.. automethod:: asimov_pyomicron.PyOmicron.check_progress
.. automethod:: asimov_pyomicron.PyOmicron.after_completion
.. automethod:: asimov_pyomicron.PyOmicron.read_ini
