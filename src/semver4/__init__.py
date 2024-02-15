from __future__ import annotations
import re
import operator
from typing import Union, NewType, SupportsInt, Optional
from semver4.errors import (
    InvalidVersionPartError,
    InvalidVersionError,
    NotComparableError
)


__version__ = '0.0.1-beta.2'


class Version:

    _valid_version_regex = '^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<fix>0|[1-9]\d*))?(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'

    def __init__(
        self,
        version: Union[str, Version] = None,
        major: Union[str, SupportsInt] = None,
        minor: Union[str, SupportsInt] = None,
        patch: Union[str, SupportsInt] = None,
        fix: Optional[Union[str, SupportsInt]] = 0,
        prerelease: Optional[Union[str, SupportsInt]] = None,
        build: Optional[Union[str, SupportsInt]] = None
    ):
        try:
            if version is None:
                version = f'{major}.{minor}.{patch}.{fix}{"-"+prerelease if prerelease else ""}{"+"+build if build else ""}'

            if isinstance(version, Version):
                versionparts = dict(version)
            elif isinstance(version, str):
                if re.fullmatch(self._valid_version_regex, version) is None:
                    raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f')
                versionparts, prerelease_build = version.split('-') if '-' in version else (version.split('.'), None)
                if prerelease_build:
                    versionparts = versionparts.split('.')
                    prerelease, build = prerelease_build.split('+') if '+' in prerelease_build else (prerelease_build, None)
                versionparts = {
                    'major': int(versionparts[0]),
                    'minor': int(versionparts[1]),
                    'patch': int(versionparts[2]),
                    'fix': int(versionparts[3] if len(versionparts) == 4 else fix),
                    'prerelease': prerelease,
                    'build': build
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

    @property
    def prerelease(self) -> int:
        return self._versionparts['prerelease']

    @property
    def build(self) -> int:
        return self._versionparts['build']

    def _compare(self, obj: Version, op: 'operator', can_equal: bool) -> bool:
        if not isinstance(obj, Version):
            raise NotComparableError(f'Can not compare Version type and {type(obj)}')
        for versionpart in ['major', 'minor', 'patch', 'fix']:
            if self[versionpart] != obj[versionpart]:
                return op(self[versionpart], obj[versionpart])
        return can_equal

    def __iter__(self):
        for part, value in self._versionparts.items():
            yield part, value

    def __getitem__(self, key):
        return self._versionparts[key]

    def __eq__(self, obj: Version) -> bool:
        return self._compare(obj, operator.eq, can_equal=True)

    def __ne__(self, obj: Version) -> bool:
        return not self.__eq__(obj)

    def __ge__(self, obj: Version) -> bool:
        return self._compare(obj, operator.gt, can_equal=True)

    def __le__(self, obj: Version) -> bool:
        return self._compare(obj, operator.lt, can_equal=True)

    def __gt__(self, obj: Version) -> bool:
        return self._compare(obj, operator.gt, can_equal=False)

    def __lt__(self, obj: Version) -> bool:
        return self._compare(obj, operator.lt, can_equal=False)
