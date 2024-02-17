from __future__ import annotations
import re
import operator
from typing import Union, SupportsInt, Optional
from semver4.errors import (
    InvalidVersionPartError,
    InvalidVersionError,
    NotComparableError,
    DecreaseVersionError
)


class BaseVersion:

    _valid_version_regex = None

    @classmethod
    def validate(cls, version, raise_err=False):
        if re.fullmatch(cls._valid_version_regex, version) is None:
            if raise_err:
                raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f-prerelease+buildmetadata')
            return False
        return True

    def __init__(
        self,
        version: Union[str, BaseVersion] = None,
        major: Union[str, SupportsInt] = None,
        minor: Union[str, SupportsInt] = None,
        patch: Union[str, SupportsInt] = None,
        fix: Optional[Union[str, SupportsInt, None]] = 0,
        prerelease: Optional[Union[str, SupportsInt]] = None,
        build: Optional[Union[str, SupportsInt]] = None,
    ):
        try:
            if version is None:
                if fix is None:
                    version = f'{major}.{minor}.{patch}{"-"+prerelease if prerelease else ""}{"+"+build if build else ""}'
                else:
                    version = f'{major}.{minor}.{patch}.{fix}{"-"+prerelease if prerelease else ""}{"+"+build if build else ""}'

            if isinstance(version, BaseVersion):
                versionparts = dict(version)
            elif isinstance(version, str):
                version = self._parse_str_version(version)
                versionparts = {
                    'major': int(version['major']),
                    'minor': int(version['minor']),
                    'patch': int(version['patch']),
                    'prerelease': version['prerelease'] if version['prerelease'] else prerelease,
                    'build': version['buildmetadata'] if version['buildmetadata'] else build
                }
                if fix is not None:
                    versionparts['fix'] = int(version['fix']) if version['fix'] else fix
            else:
                raise InvalidVersionError(f'version must be of type str or Version but is "{type(version)}"')
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

    def _inc_dec_version_part(self, part: str, op: 'operator') -> BaseVersion:
        if op is operator.sub and self[part] == 0:
            raise DecreaseVersionError(f'Can not decrease {part} version. It is already 0')
        self._versionparts[part] = op(self._versionparts[part], 1)
        return self

    def inc_major(self) -> BaseVersion:
        return self._inc_dec_version_part('major', operator.add)

    def inc_minor(self) -> BaseVersion:
        return self._inc_dec_version_part('minor', operator.add)

    def inc_patch(self) -> BaseVersion:
        return self._inc_dec_version_part('patch', operator.add)

    def inc_fix(self) -> BaseVersion:
        return self._inc_dec_version_part('fix', operator.add)

    def dec_major(self) -> BaseVersion:
        return self._inc_dec_version_part('major', operator.sub)

    def dec_minor(self) -> BaseVersion:
        return self._inc_dec_version_part('minor', operator.sub)

    def dec_patch(self) -> BaseVersion:
        return self._inc_dec_version_part('patch', operator.sub)

    def dec_fix(self) -> BaseVersion:
        return self._inc_dec_version_part('fix', operator.sub)

    def _parse_str_version(self, version):
        if (version := re.fullmatch(self._valid_version_regex, version)) is None:
            raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f-prerelease+buildmetadata')
        return version

    def _compare(self, obj: BaseVersion, op: 'operator', can_equal: bool) -> bool:
        if not isinstance(obj, BaseVersion):
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

    def __eq__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.eq, can_equal=True)

    def __ne__(self, obj: BaseVersion) -> bool:
        return not self.__eq__(obj)

    def __ge__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.gt, can_equal=True)

    def __le__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.lt, can_equal=True)

    def __gt__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.gt, can_equal=False)

    def __lt__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.lt, can_equal=False)
