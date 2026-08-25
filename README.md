# Jarvis Signed Releases

Public release channel for the Jarvis Android client.

This repository contains only public release artifacts and release metadata. The production signing keystore and passwords are intentionally never stored here, in the source repository, or in CI.

Installed Jarvis production builds trust the pinned release-certificate SHA-256 fingerprint:

`e2384592780978342912be64664d4ed53e392d8b0cb107d99a7b47b3423bc153`

The live updater reads `latest.json` from the `release-feed` branch. Versioned APKs are published before the mutable `latest.json` pointer is advanced.

Current production Android release: **v0.1.0** (`versionCode 1`).
