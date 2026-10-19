# Pre-unseal precommitment record

Created: 2026-08-30T08:56:18Z

- Git tag: pre-unseal-v1
- HEAD commit: 7e75a61418eb366187d74a424753d8ccd0685017
- Canonical tree SHA-256 (git archive of the tag, repo-independent): 823a62b9dc13293514ecc3921b6b8a87e4d7583d7e70424ec75cbbc07b6ca3fa

At this state: the E2 wide-binary spec, calibration analysis (735 pairs),
triple-injection contamination model (f ~ 0), noise MC, and every frozen
analysis choice for the sealed bin exist and are committed. The sealed
region (g_N < 10 a0) has never been computed, counted, or examined.

## Verification recipe (anyone, later)
1. git verify the tag exists and points to 7e75a61418eb366187d74a424753d8ccd0685017.
2. git archive --format=tar pre-unseal-v1 | sha256sum  ==  823a62b9dc13293514ecc3921b6b8a87e4d7583d7e70424ec75cbbc07b6ca3fa
3. Check the external anchors below predate any sealed-bin result.

## External anchors (append proofs as they land)
- [x] GitHub push of repo + tag: [commit 7e75a61418eb366187d74a424753d8ccd0685017](https://github.com/ztodaro/causal-archipelago/commit/7e75a61418eb366187d74a424753d8ccd0685017), first pushed 2026-08-30T09:05:35Z (GitHub server `pushed_at`).
- [x] OpenTimestamps proof of 7e75a61418eb366187d74a424753d8ccd0685017: [`precommit.txt.ots`](https://github.com/ztodaro/causal-archipelago/blob/master/precommit.txt.ots). Calendar attestations stamped; Bitcoin attestation upgrade pending.
