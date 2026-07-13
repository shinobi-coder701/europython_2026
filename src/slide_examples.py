from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# Type checkers do not all understand the lowercase backport yet.
from typing_extensions import NotRequired, Sentinel as sentinel, TypeIs, TypedDict


UNSET = sentinel("UNSET")

type UserId = str
type EmailAddress = str
type NicknameUpdate = str | None
type BioUpdate = str
type DecodedPayload = Mapping[str, object]


class UserPayload(TypedDict):
    id: UserId
    email: EmailAddress
    nickname: NotRequired[NicknameUpdate]
    bio: NotRequired[BioUpdate]


@dataclass
class User:
    id: UserId
    email: EmailAddress
    nickname: str | None
    bio: str | None


def is_str(x: object) -> TypeIs[str]:
    return isinstance(x, str)


def is_str_or_none(x: object) -> TypeIs[NicknameUpdate]:
    return x is None or isinstance(x, str)


def is_user_payload(payload: DecodedPayload) -> TypeIs[UserPayload]:
    return (
        isinstance(payload.get("id"), str)
        and isinstance(payload.get("email"), str)
        and (
            "nickname" not in payload
            or is_str_or_none(payload["nickname"])
        )
        and ("bio" not in payload or is_str(payload["bio"]))
    )


def merge_patch_field[T](current: T, update: T | UNSET) -> T:
    return current if update is UNSET else update


def patch_user(
    user: User,
    *,
    nickname: str | None | UNSET = UNSET,
    bio: str | None | UNSET = UNSET,
) -> User:
    user.nickname = merge_patch_field(user.nickname, nickname)
    user.bio = merge_patch_field(user.bio, bio)
    return user


def apply_payload(user: User, p: UserPayload) -> User:
    nickname = p.get("nickname", UNSET)
    bio = p.get("bio", UNSET)
    return patch_user(user, nickname=nickname, bio=bio)
