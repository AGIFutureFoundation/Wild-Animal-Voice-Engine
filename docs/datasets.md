# Datasets the Wild Animal Voice Engine can draw on

**Status:** Added to this repo 2026-11-07 by the AGI Future Foundation research-lab loop. Every archive below is a **public
resource, linked-not-owned** — WAVE holds no copy of any of them (the repo's
`data/` directory ships no datasets; see `docs/architecture.md` §1). Figures
carry as-of dates; where a figure comes from site copy rather than a primary
source it is marked as such. No archive listed here is a partnership: there is
no evidence of any contact or agreement between WAVE/the Foundation and
Cornell, the Earth Species Project, Project CETI, WHOI, Google, or the Wild
Dolphin Project.

## 1. The archives

| Archive | What it is | Settled figure (as of Nov 2026) | Licence / access | How WAVE would use it |
|---|---|---|---|---|
| **Xeno-canto** (xeno-canto.org) | Community-contributed bird sounds; the training backbone of BirdNET, Perch, and NatureLM-audio | **~1,111,111 recordings** (passed 1,111,111 in Nov 2026; dossier lit review §2.5) | Per-recording Creative Commons licences; public API | Species-classification training/evaluation data; BirdSet draws ~520,000 Xeno-canto recordings for training |
| **Macaulay Library** (Cornell Lab of Ornithology) | Audio (plus photo/video) archive; BirdNET training source | **3.2M+ audio recordings** (Nov 2026; dossier lit review §2.5) | Per-recording licences; access via Cornell | Same as Xeno-canto; the largest bird-audio collection |
| **Watkins Marine Mammal Sound Database** (WHOI) | Marine mammal vocalizations | ~2,000 unique recordings / **>15,000 annotated clips** (Sayigh et al. 2016) | Freely downloadable per the bioacoustics.cloud site copy; **official site was offline as of Sept 2026** (lit review §2.5) — re-check before citing access | The marine data WAVE actually needs; thin compared with the bird archives. The engine's `data/README.md` lists Watkins first for this reason |
| **iNaturalist Sounds** (iNaturalist) | Citizen-science multi-taxa audio | Site copy on bioacoustics.cloud says **230k+ audio files, 5,500+ species — site copy, unverified in this pass**. Independently verified: Perch 2.0 training used **571,698 iNaturalist recordings** (Perch 2.0 paper, arXiv:2508.04665) | Per-observation licences (mostly CC); public API | Multi-taxa training data; the broadest non-bird audio source in the Perch training mix |
| **Animal Sound Archive** (Tierstimmenarchiv, Museum für Naturkunde Berlin) | Bioacoustic collection, mostly birds + mammals | Site copy on bioacoustics.cloud says **120k+ recordings, ~1,800 bird + 580 mammal species — site copy, unverified in this pass**. Independently verified: Perch 2.0 training used **33,859 Tierstimmenarchiv recordings** | Varies per recording; archive access via the museum | Historical depth; a Perch training source |
| **GBIF** (gbif.org) | Species occurrence records — **not audio** | Billions of occurrence records (site copy) | Open data; public API | Context for where species occur; cannot train an audio model. Do not present GBIF as an audio archive |
| **Earth Species Library / BEANS** (earthspecies.org) | ML-ready bioacoustic datasets + the BEANS benchmark | **35+ datasets** united in ESP's `alp-data` shared data layer (July 2026, ESP blog); BEANS covers 12 datasets across birds, land/marine mammals, amphibians, bats, insects | Varies per dataset | Evaluation harness material; BEANS measures classification/detection only — never meaning |
| **Project CETI** (projectceti.org) | Sperm whale codas + behavioural context, Dominica | **8,719 codas from ~60 whales** analysed in Sharma et al. 2024 (*Nat. Commun.* 15:3617); repertoire rose from 21 to **156 distinct codas** | **No public bulk download of the coda corpus was located** (lit review §4.7) | Structure baseline only. CETI assigns no meanings to codas; neither can WAVE |

## 2. The models' training data (why the bird bias matters)

- **BirdNET v2.4** — **6,522 classes including 10 non-event classes**, trained on
  curated Xeno-canto + Macaulay recordings. The **V3.0 generation**
  ("BirdNET+", developer preview June 2026) covers **11,000+ species**. The
  6,522 and 11,000+ figures are different model generations, not a contradiction.
  BirdNET-Analyzer code is MIT; the models are **CC BY-NC-SA 4.0
  (non-commercial)**. There is no hosted API.
  - *Footnote discrepancy (unresolved):* the loop's settled figure dates v2.4 to
    **June 2023**; the dossier lit review §2.1 dates v2.4 (production) to
    **March 2025**. The class count (6,522 incl. 10 non-event) is consistent in
    both. Do not quote a v2.4 release date until the discrepancy is resolved
    against a primary source.
- **Perch 2.0** (Google Research, 7 Aug 2025) — **14,795 classes (14,597 species
  + 198 general sound-event classes)**, trained on **1,542,778 recordings**
  (Xeno-canto 896,255; iNaturalist 571,698; Tierstimmenarchiv 33,859; FSD50K
  40,966). Code Apache-2.0; models free via Kaggle. Key limitation stated in its
  own paper: almost no marine hydrophone training data (only a few dozen
  cetacean recordings).
- **NatureLM-audio** (Earth Species Project, arXiv:2411.07186, Nov 2024) —
  **>26 million (audio, text) pairs; >2 million audio files; 22,100 hours;
  44 bioacoustic tasks**, from Xeno-canto, iNaturalist, Watkins, the Animal
  Sound Archive, plus speech, music, and environmental sound. The paper itself
  says the model "can hallucinate"; its tasks are detection, classification,
  and captioning — not meaning. **Not connected to WAVE.**

## 3. The data gap, stated plainly

The classifiers are trained overwhelmingly on birds because the archives are
overwhelmingly birds. Marine data is thin (Watkins ~2,000 recordings; Perch's
few dozen cetacean recordings). Any claim about "talking to whales" built on
bird-trained models inherits this gap directly. The honest near-term research
product is a dataset, not a translator: a curated, openly licensed corpus of
*paired* call-and-response playback data (even small, even one species) would be
more scientifically valuable than another classifier — see the dossier lit
review §6 (the Playback-Prediction Test hypothesis). No such corpus is held by
WAVE today, and Phase 0 of that hypothesis depends on data access that is not
yet secured.

## 4. Benchmarks — what they measure (and do not)

| Benchmark | Measures | Scale / status |
|---|---|---|
| BEANS | Classification + detection, 12 datasets | Code: github.com/earthspecies/beans (Hagiwara et al. 2023) |
| BEANS-Zero | Zero-shot / cross-task generalisation | Companion to NatureLM-audio |
| BirdSet | Bird-sound classification in real soundscapes | ~520,000 Xeno-canto recordings for training; 400+ hours annotated test audio |
| BirdCLEF+ (2026) | Species ID in soundscapes, CPU-only | 234 multi-taxon classes, Pantanal, Mar–Jun 2026 |

All current benchmarks measure detection/classification/structure — never
meaning. A leaderboard win is never a decoding result.

## 5. Sources

- Dossier: `dossier/animal-voice-decoding-lit-review.md` (§2, §4.7, §5) and
  `dossier/bioacoustics-github-survey.md` (§2–§3), research-lab loop, 2026-11-07.
- Primary sources cited there: BirdNET (birdnet.cornell.edu/about), Perch 2.0
  (arXiv:2508.04665), NatureLM-audio (arXiv:2411.07186), Sharma et al. 2024
  (*Nat. Commun.* 15:3617), Sayigh et al. 2016 (Watkins).
- Figures marked "site copy" come from `bioacoustics-cloud/index.html`
  (Resources section) and were **not** verified against a primary source in
  this pass. Do not quote them to a funder, partner, or the press until checked.
