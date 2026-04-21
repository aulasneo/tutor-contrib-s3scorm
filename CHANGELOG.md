# Change log

## Unreleased
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
