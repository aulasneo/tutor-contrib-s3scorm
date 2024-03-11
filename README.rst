s3scorm plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

Using SCORM modules in multi-server deployments offer a number of challenges.
A full list of scenarios and solutions can be found in
`this document <https://support.scorm.com/hc/en-us/article_attachments/201865846/ADL_CrossDomainScripting_1_0.pdf>`_.

Basically a SCORM component is a set of files packed in a ``zip`` file that includes
all assets to display and control its behaviour. This file is uploaded in Studio,
stored and unpacked in the default file storage and displayed in the LMS from there.

SCORM components are inserted in the LMS as an ``iframe`` by the
`SCORM Xblock plugin <https://github.com/overhangio/openedx-scorm-xblock>`_.
When the SCORM XBlock is configured as graded, it will call an API located at the parent window
to communicate the result of the activity to the LMS. When the SCORM assets are
served from an origin different than the url of the LMS, this will usually fail
due to cross-origin restrictions imposed by the browser.

Scalable LMS implementations require that the file storage is located outside of the
LMS and CMS workloads, typically in an object storage service like AWS S3.
In this scenario the standard configuration may allow SCORM blocks to be displayed,
but the grading function will certainly fail.

This plugin addresses this issue to make graded SCORM XBlocks work.

How it works
------------

This plugin will add a reverse proxy statement to the lms matcher in the Caddyfile, so that
requests to *LMS_BASE*/scorm/ will be proxied to the S3 endpoint corresponding to the bucket.
This will cause that all SCORM assets will be served from the same origin url as the LMS.
The effect is that the scorm components will be able to access the api located at the parent window.

To have the

Installation
------------

::

    pip install git+https://github.com/aulasneo/tutor-contrib-s3scorm

Configuration
-------------

This plugins require that you setup these two parameters. There are no defaults,
so leaving any of them not configured will cause an error.

- S3SCORM_BUCKET (mandatory): name of the bucket (e.g., *openedx-my-file-bucket*)
- S3SCORM_ENDPOINT (mandatory): S3 endpoint. E.g., *s3.us-east-1.amazonaws.com*.
- S3SCORM_PATH (optional): Path inside the bucket where the 'scorm' directory is located.
  Include a leading slash and no trailing slash (e.g. "/openedx/media"). Defaults to empty path (root of the bucket).

Optional parameters:

- S3SCORM_USE_SSL: Default true.

Usage
-----

::

    tutor plugins enable s3scorm


License
-------

This software is licensed under the terms of the AGPLv3.