.. workshop.dipy.org documentation master file, created by
   sphinx-quickstart on Mon Jul 15 17:03:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#################
Workshop Homepage
#################

.. workshop-home::

.. workshop-about::

####################
Workshop Speakers
####################

.. workshop-speakers::
   :template: _templates/speaker_template.html

   .. workshop-speaker::
      :name: Eleftherios Garifallidis
      :image: garyfallidis.jpg

      This is the biography for John Doe. It can contain **RST markup**.

   .. workshop-speaker::
      :name: Ariel Rokem
      :image: rokem.jpg

      Jane Smith's bio.
      It can span multiple lines.

   # Add more speakers as needed

.. workshop-schedule::

   .. workshop-timeline::
      :title: Day 1
      :subtitle: Reconstruction theme
      :date: 2025-03-17
      :template: _templates/schedule_template.html

      .. workshop-timeline-item::
         :time: 09:00 - 09:45
         :title: Workshop Overview
         :speaker: Serge Koudoro
         :image: serge.png

      .. workshop-timeline-item::
         :time: 10:00 - 10:45
         :title: Reconstruction
         :speaker: Maharshi Gor
         :image: maharshi.jpeg

   .. workshop-timeline::
      :title: Day 2
      :subtitle: Segmentation theme
      :date: 2025-03-17
      :template: _templates/schedule_template.html

      .. workshop-timeline-item::
         :time: 09:00 - 09:45
         :title: Assembly
         :speaker: TBD
         :image: dipy-all.svg

      .. workshop-timeline-item::
         :time: 10:00 - 10:45
         :title: Tractography
         :speaker: Kaustav

.. Add other directives here as they are created
   (Why, Highlights, Registration, Contact)

.. Placeholders for other content if needed


.. Comment out or remove ToC tree and Indices/Tables section
.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:


.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

