from __future__ import annotations
import re
from typing import Union, NewType, SupportsInt, Optional
from semver4.errors import InvalidVersionPartError, InvalidVersionError


__version__ = '0.0.1-beta.1'


class Version:

    _valid_version_regex = '^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<fix>0|[1-9]\d*))?$'

    def __init__(
        self,
        version: Union[str, Version] = None,
        major: Union[str, SupportsInt] = None,
        minor: Union[str, SupportsInt] = None,
        patch: Union[str, SupportsInt] = None,
        fix: Optional[Union[str, SupportsInt]] = 0
    ):
        try:
            if version is None:
                version = f'{major}.{minor}.{patch}.{fix}'
            if isinstance(version, Version):
                versionparts = tuple(version)
            elif isinstance(version, str):
                if re.fullmatch(self._valid_version_regex, version) is None:
                    raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f')
                versionparts = [int(vp) for vp in str(version).split('.')]
                if len(versionparts) == 3:
                    versionparts.append(fix)
            else:
                raise InvalidVersionError(f'version must be of type str or Version but is "{type(version)}"')
        except ValueError:
            raise InvalidVersionPartError('Version part must not be non-numeric string')
        except (InvalidVersionPartError, InvalidVersionError) as err:
            raise err
        else:
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
