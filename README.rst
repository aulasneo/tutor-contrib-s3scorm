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

Performance: caching, compression and CDN
------------------------------------------

By default, every SCORM asset request is proxied by Caddy straight to S3 on each and every
request, with no caching or compression. For courses with SCORM packages containing video,
audio or many images, this adds up: assets are re-fetched in full on every page load, and
text assets (JS/HTML/JSON) are sent uncompressed. Three settings address this without
changing how access is controlled — the LMS/CMS still decide who ever reaches
``/scorm/...`` in the first place, since these XBlocks are only rendered on pages already
gated by the standard enrollment/authentication checks.

- **S3SCORM_CACHE_MAX_AGE** (optional, default ``86400``): adds a
  ``Cache-Control: public, max-age=<value>, immutable`` header to SCORM asset responses so
  browsers stop re-downloading unchanged assets on every visit. Set to ``0`` to disable the
  header entirely (previous behavior). Because SCORM asset paths are keyed by block usage id
  and are typically overwritten in place when a course team re-uploads a package, keep this
  conservative unless your asset paths are otherwise versioned; raise it (e.g. to
  ``31536000`` for a year) once you're confident republishing isn't a concern, or your
  pipeline invalidates/versions asset paths on republish.
- **S3SCORM_COMPRESS** (optional, default ``true``): has Caddy transparently compress
  (zstd/gzip) text-based SCORM assets (the SCORM package's own JS/HTML/CSS/JSON) on the fly.
  Binary assets such as video and images are left as-is. Set to ``false`` to disable.
- **S3SCORM_CLOUDFRONT_DOMAIN** (optional, default empty): the domain name of a CDN
  distribution (e.g. a CloudFront distribution) that has the SCORM bucket configured as its
  origin. When set, Caddy proxies ``/scorm/*`` to this domain instead of talking to S3
  directly, so requests benefit from edge caching, edge compression and reduced load on the
  origin bucket — while assets are still served from the same origin as the LMS/CMS, so the
  SCORM grading ``postMessage`` API continues to work exactly as described above. When this
  is set, ``S3SCORM_ENDPOINT``/``S3SCORM_URL_STYLE``/bucket-address settings are ignored for
  upstream addressing (``S3SCORM_PATH`` still applies if your distribution's origin path
  mirrors the bucket layout).

Example, adding a CDN and a one-year cache lifetime on top of the base configuration::

    tutor config save \
        --set S3SCORM_CLOUDFRONT_DOMAIN=d123456abcdef8.cloudfront.net \
        --set S3SCORM_CACHE_MAX_AGE=31536000

Usage
-----

::

    tutor plugins enable s3scorm


License
-------

This software is licensed under the terms of the AGPLv3.
