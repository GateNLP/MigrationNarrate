# MigrationNarrate

**MigrationNarrate: A Dataset for Detection of Migration Narratives in YouTube Videos**

MigrationNarrate is a dataset for studying **migration narratives in UK-related YouTube videos**. It contains **1,115 human-annotated videos** labelled using a hierarchical taxonomy of migration narratives, together with a larger set of **4,425 automatically filtered unlabelled videos**.

The taxonomy consists of **12 super-narratives and 53 fine-grained narrative labels**. Of these, 51 fine-grained narratives are represented in the human-annotated dataset.

The dataset was introduced in:

> Fatima Haouari, Carolina Scarton, and Kalina Bontcheva.
> **MigrationNarrate: A Dataset for Detection of Migration Narratives in YouTube Videos.**
> Accepted to the Main Conference of EMNLP 2026.
> [arXiv:2608.20984](https://arxiv.org/abs/2608.20984)

---

## Dataset Overview

MigrationNarrate was created to support research on the detection and analysis of migration narratives in video-based online discourse.

The original collection contains short YouTube videos related to migration in the UK, published between **1 January 2024 and 30 September 2025**. Videos longer than three minutes were excluded.

The collection and filtering pipeline resulted in:

| Dataset                 | Videos | Unique channels | Avg. duration |
| ----------------------- | -----: | --------------: | ------------: |
| Filtered corpus         |  5,540 |           2,081 |     90.46 sec |
| Human-annotated dataset |  1,115 |             684 |     79.73 sec |
| Unlabelled subset       |  4,425 |               — |             — |

The 1,115 annotated videos are divided into:

| Split       |    Videos |
| ----------- | --------: |
| Train       |       774 |
| Development |       117 |
| Test        |       224 |
| **Total**   | **1,115** |

---

```text
MigrationNarrate/
│
├── data/
│   ├── labelled_data.tsv
│   └── unlabelled_data.tsv
│
├── taxonomy/
│   └── migration_narratives_taxonomy.tsv
│
├── scripts/
│   ├── download_videos.py
│   └── extract_transcripts.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

### `data/labelled_data.tsv`

Contains the identifiers and human annotations for the **1,115 annotated YouTube videos**.

### `data/unlabelled_data.tsv`

Contains the identifiers of the **4,425 migration-related videos** retained by the automatic filtering pipeline but not selected for human annotation.

### `taxonomy/migration_narratives_taxonomy.tsv`

Contains the hierarchical migration narrative taxonomy used for annotation, including the **12 super-narratives and 53 narrative labels** and their definitions.

Contains the identifiers and human annotations for the **1,115 annotated YouTube videos**.

The released dataset does **not** contain video files, audio, or transcripts.

Recommended fields include:

| Field             | Description                            |
| ----------------- | -------------------------------------- |
| `video_id`        | YouTube video identifier               |
| `super_narrative` | Human-annotated super-narrative        |
| `narrative`       | Human-annotated fine-grained narrative |
| `split`           | `train`, `dev`, or `test`              |

The annotation `None` indicates that, after human annotation/adjudication, no migration narrative was explicitly stated or strongly implied in the video.

### `data/unlabelled_data.tsv`

Contains the identifiers of the **4,425 migration-related videos** retained by the automatic filtering pipeline but not selected for human annotation.

These data can be useful for, for example, weakly supervised, semi-supervised, or further manual annotation experiments.

### `taxonomy/migration_narratives_taxonomy.tsv`

Contains the hierarchical migration narrative taxonomy used for annotation, including the **12 super-narratives and 53 narrative labels** and their definitions.

The taxonomy is based on the migration narrative taxonomy introduced by the European Commission's Joint Research Centre (JRC). Narrative definitions used during annotation were developed for this study and manually reviewed by the authors.

---

## Data Collection

Videos were collected using two complementary strategies:

**Channel- and playlist-based collection.** Videos were collected from migration-related and broader political/news channels and playlists using the YouTube Data API v3.

**Search-based collection.** Additional videos were retrieved using migration-related search phrases in order to increase the diversity of sources represented in the corpus.

The initial collection was subsequently filtered to retain videos:

* published between **1 January 2024 and 30 September 2025**;
* with a duration of **three minutes or less**;
* for which a transcript could be generated; and
* identified as migration-related using semantic similarity filtering.

After this process, **5,540 videos** remained in the filtered corpus.

A diverse subset of **1,115 videos** was then selected for human annotation.

For full details of the collection, filtering, sampling, and annotation procedures, please refer to the paper.

---

## Annotations

MigrationNarrate uses a hierarchical annotation scheme.

Each video is first assigned a **super-narrative** and then, where applicable, a corresponding **fine-grained narrative**.

The annotation taxonomy contains:

* **12 super-narratives**
* **53 fine-grained narratives**

The human-annotated dataset contains instances belonging to **51 of the 53 fine-grained narrative categories**, in addition to examples labelled `None`.

Each annotation batch was independently annotated by two annotators, with disagreements resolved through adjudication.

---

## Obtaining the Videos

To comply with YouTube's Terms of Service and copyright requirements, **we do not redistribute the original YouTube videos or audio files**.

Instead, the dataset provides YouTube video identifiers.

A script for downloading videos that remain publicly available on YouTube is provided in:

```text
scripts/download_videos.py
```

Please note that YouTube content can be removed, made private, or otherwise become unavailable over time. Consequently, it may not always be possible to reconstruct the complete original dataset.

Users are responsible for ensuring that their use of YouTube content complies with the applicable YouTube Terms of Service and relevant copyright requirements.

---

## Obtaining the Transcripts

We **do not redistribute the generated video transcripts**.

The transcripts used in the paper were generated from the downloaded videos using **faster-whisper**.

We provide scripts to:

* download available transcripts directly from YouTube; and
* generate transcripts from downloaded videos using **faster-whisper** when needed.

```text
scripts/download_transcripts.py
scripts/extract_transcripts.py
```

Please note that some videos may not have transcripts available directly from YouTube. In such cases, transcripts can be generated from the downloaded video using the provided transcription script.

Exact reconstructed transcripts may differ slightly from those used in the original experiments depending on video availability, transcript availability, software/model versions, and decoding configuration.

---

## Citation

If you use MigrationNarrate in your research, please cite:

```bibtex
@article{haouari2026migrationnarrate,
  title     = {MigrationNarrate: A Dataset for Detection of Migration Narratives in YouTube Videos},
  author    = {Haouari, Fatima and Scarton, Carolina and Bontcheva, Kalina},
  journal   = {arXiv preprint arXiv:2608.20984},
  year      = {2026}
}
```

The paper was accepted to the **Main Conference of EMNLP 2026**. The citation will be updated with the official ACL Anthology proceedings information when available.

---

## License

The **MigrationNarrate dataset and annotations** are released under the **CC BY-NC-SA 4.0** license for non-commercial research use.

The license applies to the released metadata and annotations and does not grant rights to the underlying YouTube content. Original videos remain subject to the rights and terms of their respective creators and YouTube.

See `LICENSE` for details.

---

## Contact

For questions about the dataset, please open an issue in this repository or contact the authors of the paper.

---

## Acknowledgements



