======================================
APT-Notes Report Parser and Downloader
======================================

Parses **AptNotes** data and downloads files from Box. `APTnotes <https://github.com/kbadla/aptnotes/>`_ is a repository of publicly-available papers and blogs related to malicious campaigns/activity/software that have been associated with vendor-defined APT (Advanced Persistent Threat) groups and/or tool-sets.

************************************
Download APTNotes Report Information
************************************

::

  from aptnotes import AptNotes

  for report in AptNotes.get_reports():
    print(report)  # Report object
    ...

*****************************
Download Reports from Box.com
*****************************

::

  from aptnotes import AptNotes
  from tempfile import TemporaryFile

  for report in AptNotes.get_reports():
    with TemporaryFile() as tempfile:
      tempfile.write(report.get_file_content())   # Get file contents from Box.com
      ...



