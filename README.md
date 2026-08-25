# Jarvis Signed Releases

Public release channel for the Jarvis Android client.

This repository contains only public release artifacts and release metadata. The production signing keystore and passwords are intentionally never stored here, in the private source repository, or in CI.

Installed Jarvis production builds trust the pinned release-certificate SHA-256 fingerprint:

`6d8527dcf2f64d402066dd7a6a222dc847c8f881d63a5d99c9810d20050b1fa2`

The live updater reads `latest.json` from the `release-feed` branch. Versioned APKs are published before the mutable `latest.json` pointer is advanced.
