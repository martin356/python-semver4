from __future__ import annotations
import re
from typing import Union, NewType, SupportsInt, Optional
from semver4.errors import InvalidVersionPartError, InvalidVersionError


__version__ = '0.0.1-beta'


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
                versionparts = dict(version)
            elif isinstance(version, str):
                if re.fullmatch(self._valid_version_regex, version) is None:
                    raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f')
                versionparts = version.split('.')
                versionparts = {
                    'major': int(versionparts[0]),
                    'minor': int(versionparts[1]),
                    'patch': int(versionparts[2]),
                    'fix': int(versionparts[3] if len(versionparts) == 4 else fix)
                }
                if len(versionparts) == 3:
                    versionparts.append(fix)
            else:
                raise InvalidVersionError(f'version must be of type str or Version but is "{type(version)}"')
        except ValueError:
            raise InvalidVersionPartError('Version part must not be non-numeric string')
        except (InvalidVersionPartError, InvalidVersionError) as err:
            raise err
        else:
            self._versionparts = versionparts

    @property
    def major(self) -> int:
        return self._versionparts['major']

    @property
    def minor(self) -> int:
        return self._versionparts['minor']

    @property
    def patch(self) -> int:
        return self._versionparts['patch']

    @property
    def fix(self) -> int:
        return self._versionparts['fix']

    def __iter__(self):
        for part, value in self._versionparts.items():
            yield part, value

    def __getitem__(self, key):
        return self._versionparts[key]

    # def __eq__(self, obj: Version) -> bool:
    #     for versionpart in ['major', 'minor', 'patch', 'fix']:
    #         if self[versionpart] == self
    #         return
