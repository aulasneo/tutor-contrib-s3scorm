# Change log

## Unreleased
- Fix cache routing scorm path, and not error pages.

## Version 21.1.0 (2026-08-17)
- feat: add `S3SCORM_CACHE_MAX_AGE` to send a `Cache-Control` header on proxied SCORM assets so browsers stop re-downloading unchanged assets on every page load (default 1 day; set to `0` to disable)
- feat: add `S3SCORM_COMPRESS` to have Caddy transparently compress text-based SCORM assets (default enabled)
- feat: add `S3SCORM_CLOUDFRONT_DOMAIN` to proxy `/scorm/*` through a CDN distribution in front of the bucket instead of talking to S3 directly, while keeping assets same-origin with the LMS/CMS so SCORM grading `postMessage` still works
- fix: when `S3SCORM_CLOUDFRONT_DOMAIN` is set, also set `XBLOCK_SETTINGS["ScormXBlock"]["PROXY_ASSETS_LMS"] = False` in the LMS/CMS settings patches — without this, the xblock keeps linking to its own `assets_proxy` Django handler regardless of storage backend, so the `/scorm/*` Caddy route (and the caching/compression settings above) was never actually reached by real asset requests. `PROXY_ASSETS_LMS` is left untouched (default `True`) when no CDN domain is configured.
- fix: only add the `Cache-Control` header to successful (2xx) SCORM asset responses, using a `handle_response`/`copy_response` block instead of an unconditional `header` directive. Previously the header was applied to every response regardless of status, so a transient origin failure (e.g. a misconfigured CloudFront behavior or an S3 permissions error) would get cached client-side for the full `S3SCORM_CACHE_MAX_AGE` duration, making the failure "sticky" for anyone who hit it. Verified against real `caddy` binaries (v2.6.2 and v2.7.4, the version Tutor 21 actually ships) that: the config validates and adapts correctly, a 2xx response gets the header with its body passed through intact, and a non-2xx response passes through unmodified with no `Cache-Control` added.

## Version 21.0.0 (2026-04-21)
- fix: default `S3SCORM_BUCKET` to `S3_STORAGE_BUCKET` from `tutor-contrib-s3` when not set explicitly
- feat: make `S3SCORM_ENDPOINT` optional with `S3_HOST`/`S3_PORT` and `S3_REGION` fallbacks, and add `S3SCORM_URL_STYLE` for virtual-hosted or path-style upstreams
- feat: add branding-aligned local development automation with a full `Makefile` and pinned dev requirements files
- feat: replace the older CI/release automation with `test.yml` and tag-driven `publish.yml` workflows
- ref: adopt a minimal `pyproject.toml` for modern builds while keeping existing package behavior intact
- breaking: require Python 3.11 or newer in package metadata
- chore: ignore generated Tutor `config.yml` and `env/` artifacts from local test runs
- Upgrade Tutor compatibility to 21.x for Open edX Ulmo.
- Refresh development requirements and package metadata for Tutor 21.

## Version 20.0.0 (2026-03-17)
- Upgrade to Teak / Tutor 20.
- Fix `S3SCORM_PATH` by rewriting the upstream URI instead of embedding a path in the proxy upstream.
- Preserve existing `ScormXBlock` settings when injecting the storage hook.
- Ignore dotfiles when loading Tutor environment patches.

## Version 19.0.0 (2025-04-28)
- Upgrade to Sumac

## Version 18.0.0 (2024-07-26)
- Upgrade to Redwood

## Version 17.0.0 (2024-07-25)
- Upgrade to Quince

## Version 16.1.1 (2024-03-12)
- Fixed SCORM in Studio

## Version 16.1.0 (2024-03-11)
- Patch also the CMS to allow the SCORM to find the API in Studio.
- Add `S3SCORM_PATH` to specify where is the `scorm` folder located.

## Version 16.0.0 (2023-11-17)
- Upgrade to Palm

## Version 15.0.0 (2023-10-05)
- Update dependency Tutor 15 / Olive

## Version 14.0.1 (2023-10-05)
- Update dependency Tutor 14 / Nutmeg

## Version 14.0.0
- Initial version
