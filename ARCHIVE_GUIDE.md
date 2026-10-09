# Archive Selection and Navigation

This is an offline, repository-ready file bundle. It does not create a Git repository, publish to a hosting service, or establish a public release date.

## Preserved selection

The package contains 51 original ZIPs, one recovery tarball, and eight standalone early files. One ZIP is the separate October 7 external review. The other 59 original files belong to the historical research selection. Their original filenames and bytes are unchanged; public relative paths, sizes, and SHA-256 hashes are in publication_manifest.json.

The source inventory had 82 local originals. Seventeen ZIP snapshots had their complete recursively inspected file payloads represented by retained archives, and five loose files were already represented inside retained archives. Those 22 originals are not recopied. This is payload preservation, not a promise to preserve every historical outer ZIP byte or filename as a separate file.

- v54–v59 are represented within v60's exact baseline chain
- v45–v46 payloads are represented within v47
- Eight 20F/D16 family certificate payloads (81, 82, 86, 87, 88, 89, 90, 91) are represented within the 20F/D16 complete bundle
- v32 is represented within v33
- Five duplicated loose early-source files are represented in retained archives

v48–v53 have distinct payloads and remain separate. The original v44 archive is also retained because its original contents.sha256 is not present in the v47 expanded copy. Separate earlier bounded-class archives remain necessary; v43 does not embed the full v33 proof package.

## Browsable latest snapshot

latest/v61/ contains the 15 files copied directly from the original v61 ZIP, without edits. Its manifest.json covers 12 payload files; its stored replay log and replay output are also preserved. The original ZIP remains in originals/mahler/. The public package manifest records the source archive entry for each browsable file.

To understand or later reproduce a snapshot, first read its report and README, including assumptions, dependencies, failure records, and remaining gaps. Installing dependencies or running a verifier is a separate activity. No historical research code was executed to assemble this package.

## Integrity files

publication_manifest.json describes original and browsable-source provenance without private storage identifiers. FILES.tsv lists every packaged file except FILES.tsv and SHA256SUMS, avoiding self-reference. SHA256SUMS covers every packaged file except SHA256SUMS itself, including FILES.tsv. A matching hash establishes the checked bytes, not the truth of a mathematical claim.

中文：本包是可离线审阅、可用于仓库的文件集合，未创建 Git 仓库或公开发布。重复原包的有效载荷由保留归档表示，因此并非每个历史外层 ZIP 都单独保留。latest/v61/ 是原 ZIP 的 15 个文件的原字节展开副本；原 ZIP 仍保留。完整性清单用于核对字节，不用于认证数学正确性。缺失材料见 STATUS.md。
