## 0.0.1-beta.7 (0.0.1b7)
- #### Added
    - make Version object comparable to string
- #### Fixed
    - core property: fix version is ignored if equals to 0
    - increase and decrease a version part: prerelase and build metadata are cut
## 0.0.1-beta.6 (0.0.1b6)
- #### Added
    - core property: return core of a version
- #### Fixed
    - increase and decrease a version part
## 0.0.1-beta.5 (0.0.1b5)
- #### Added
    - comparison of pre-release part of a version
    - make pre-release and build metadata parts of a version mutable
    - functions for json serialization
    - loader and dumper for yaml serialization using pyyaml
- #### Changed
    - \_\_repr\_\_ returns same value as \_\_str\_\_