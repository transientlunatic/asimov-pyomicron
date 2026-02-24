Configuration
=============

PyOmicron pipeline configuration is defined through the production metadata in your Asimov ledger or configuration file.

Configuration Structure
-----------------------

The configuration is organized into several sections under the ``meta`` key:

.. code-block:: yaml

   meta:
     data:
       # Data source parameters
     omicron:
       # PyOmicron-specific parameters
     scheduler:
       # HTCondor scheduler parameters

Data Parameters
---------------

These parameters define the data source and time range for processing.

channel names
~~~~~~~~~~~~~

**Type:** dict or string

Dictionary mapping IFO codes to channel names, or a single channel name string.

.. code-block:: yaml

   channel names:
     H1: "H1:GDS-CALIB_STRAIN"
     L1: "L1:GDS-CALIB_STRAIN"

Or:

.. code-block:: yaml

   channel name: "H1:GDS-CALIB_STRAIN"

frametype
~~~~~~~~~

**Type:** string

Frame type name for the data files containing the channels.

.. code-block:: yaml

   frametype: "H1_HOFT_C00"

gps-start-time
~~~~~~~~~~~~~~

**Type:** integer

GPS start time for processing.

.. code-block:: yaml

   gps-start-time: 1126259446

gps-end-time
~~~~~~~~~~~~

**Type:** integer

GPS end time for processing.

.. code-block:: yaml

   gps-end-time: 1126259478

Omicron Parameters
------------------

These parameters control the Omicron algorithm behavior.

Timing Parameters
~~~~~~~~~~~~~~~~~

chunk_duration
^^^^^^^^^^^^^^

**Type:** integer  
**Default:** 124

Duration of data (in seconds) for PSD estimation.

.. code-block:: yaml

   chunk_duration: 124

segment_duration
^^^^^^^^^^^^^^^^

**Type:** integer  
**Default:** 64

Duration of data (in seconds) for FFT.

.. code-block:: yaml

   segment_duration: 64

overlap_duration
^^^^^^^^^^^^^^^^

**Type:** integer  
**Default:** 4

Overlap (in seconds) between neighbouring segments and chunks.

.. code-block:: yaml

   overlap_duration: 4

Search Parameters
~~~~~~~~~~~~~~~~~

frequency_range
^^^^^^^^^^^^^^^

**Type:** string  
**Default:** "4.0 8192.0"

Low and high frequency limits (in Hz) for the search, space-separated.

.. code-block:: yaml

   frequency_range: "4.0 2048.0"

q_range
^^^^^^^

**Type:** string  
**Default:** "3.3166 150"

Low and high Q-factor limits for the search, space-separated.

.. code-block:: yaml

   q_range: "3.3166 150"

mismatch_max
^^^^^^^^^^^^

**Type:** float  
**Optional**

Maximum distance between (Q, f) tiles.

.. code-block:: yaml

   mismatch_max: 0.2

snr_threshold
^^^^^^^^^^^^^

**Type:** float  
**Optional**

Minimum SNR for recorded triggers.

.. code-block:: yaml

   snr_threshold: 5.5

sample_frequency
^^^^^^^^^^^^^^^^

**Type:** integer  
**Optional**

Sample frequency in Hz.

.. code-block:: yaml

   sample_frequency: 16384

State Parameters
~~~~~~~~~~~~~~~~

You can define the data quality state in two ways:

Option 1: Using state flag
^^^^^^^^^^^^^^^^^^^^^^^^^^^

state_flag
""""""""""

**Type:** string  
**Optional**

Data-quality flag name defining active state segments.

.. code-block:: yaml

   state_flag: "H1:DMT-CALIBRATED:1"

Option 2: Using state channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

state_channel
"""""""""""""

**Type:** string  
**Optional**

Name of data channel defining active state.

.. code-block:: yaml

   state_channel: "H1:DMT-ANALYSIS_READY:1"

state_frametype
"""""""""""""""

**Type:** string  
**Required if state_channel is used**

Frame type name for the state channel.

.. code-block:: yaml

   state_frametype: "H1_R"

state_bits
""""""""""

**Type:** string  
**Required if state_channel is used**

Comma-separated list of bit numbers that define active state in the state channel.

.. code-block:: yaml

   state_bits: "0,1,2"

Scheduler Parameters
--------------------

These parameters control HTCondor job submission.

accounting group
~~~~~~~~~~~~~~~~

**Type:** string  
**Optional**

HTCondor accounting group for the job.

.. code-block:: yaml

   accounting group: "ligo.prod.o4.detchar.transient.omicron"

cpus
~~~~

**Type:** integer  
**Default:** 1

Number of CPUs to request.

.. code-block:: yaml

   cpus: 1

memory
~~~~~~

**Type:** string  
**Default:** "4096MB"

Memory to request for the job.

.. code-block:: yaml

   memory: "8192MB"

disk
~~~~

**Type:** string  
**Default:** "4096MB"

Disk space to request for the job.

.. code-block:: yaml

   disk: "8192MB"

Complete Example
----------------

Here's a complete configuration example:

.. code-block:: yaml

   productions:
     - name: GW150914_omicron
       pipeline: pyomicron
       comment: Omicron triggers for GW150914
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
           mismatch_max: 0.2
           snr_threshold: 5.5
           sample_frequency: 16384
           state_flag: "H1:DMT-CALIBRATED:1"
         scheduler:
           accounting group: "ligo.prod.o4.detchar.transient.omicron"
           cpus: 1
           memory: "4096MB"
           disk: "4096MB"
