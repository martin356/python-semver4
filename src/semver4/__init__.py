from __future__ import annotations
from typing import Union, NewType, SupportsInt, Optional
import semver4.errors as errors


class Version:

    def __init__(
        self,
        version: Union[str, Version] = None,
        major: Union[str, SupportsInt] = None,
        minor: Union[str, SupportsInt] = None,
        patch: Union[str, SupportsInt] = None,
        fix: Optional[Union[str, SupportsInt]] = 0
    ):
        if version:
            versionparts = tuple(version)
        else:
            try:
                for vp in (versionparts := (int(major), int(minor), int(patch), int(fix))):
                    if vp < 0:
                        raise errors.WrongVersionPart('Version part must be positive integer or zero')
            except ValueError:
                raise errors.WrongVersionPart('Version part must not be non-numeric string')
            except errors.WrongVersionPart as err:
                raise err

        self._major, self._minor, self._patch, self._fix = versionparts

    def __iter__(self):
        for part in [self.major, self.minor, self.patch, self.fix]:
            yield part

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def patch(self) -> int:
        return self._patch

    @property
    def fix(self) -> int:
        return self._fix
