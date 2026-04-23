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

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint

How it works
------------

This plugin will add a reverse proxy statement to the lms matcher in the Caddyfile, so that
requests to *LMS_BASE*/scorm/ will be proxied to the S3 endpoint corresponding to the bucket.
This will cause that all SCORM assets will be served from the same origin url as the LMS.
The effect is that the scorm components will be able to access the api located at the parent window.

The same mechanism is also applied to *LMS_BASE*/h5pxblockmedia/ so that H5P content can be
served from the LMS origin when `h5pxblock` uses S3-backed storage.

To have the

Installation
------------

::

    pip install tutor-contrib-s3scorm

This release targets Tutor 21 / Open edX Ulmo.

Configuration
-------------

This plugin integrates with ``tutor-contrib-s3``. By default, ``S3SCORM_BUCKET``
inherits the value of ``S3_STORAGE_BUCKET`` if that setting is defined. You only
need to set ``S3SCORM_BUCKET`` explicitly when SCORM files live in a different bucket.

These parameters are used by the plugin:

- S3SCORM_BUCKET (optional): name of the bucket (e.g., *openedx-my-file-bucket*).
  Defaults to ``S3_STORAGE_BUCKET`` if that variable is defined.
- S3SCORM_ENDPOINT (optional): S3 endpoint. E.g., *s3.us-east-1.amazonaws.com*.
  If unset, the plugin falls back to ``S3_HOST`` and ``S3_PORT``, then ``s3.<S3_REGION>.amazonaws.com``.
- S3SCORM_PATH (optional): Path inside the bucket where the 'scorm' directory is located.
  Include a leading slash and no trailing slash (e.g. "/openedx/media"). Defaults to empty path (root of the bucket).
- S3SCORM_URL_STYLE (optional): How the upstream bucket is addressed. Use ``virtual`` for
  ``<bucket>.<endpoint>`` and ``path`` for ``<endpoint>/<bucket>``. Defaults to ``virtual``.

Optional parameters:

- S3SCORM_USE_SSL: Default true.

When ``S3SCORM_PATH`` is set, the proxy preserves the public ``/scorm/...`` URL and rewrites
the upstream request to ``<S3SCORM_PATH>/scorm/...`` inside the bucket.
The upstream endpoint is resolved in this order: ``S3SCORM_ENDPOINT``, ``S3_HOST`` plus
``S3_PORT`` if set, and finally ``s3.<S3_REGION>.amazonaws.com``.
When ``S3SCORM_URL_STYLE`` is set to ``path``, the bucket is placed in the upstream URI path
instead of the hostname.

Usage
-----

::

    tutor plugins enable s3scorm


License
-------

This software is licensed under the terms of the AGPLv3.
