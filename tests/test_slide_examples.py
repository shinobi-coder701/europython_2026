from __future__ import annotations

import unittest

import typing_extensions

from src.slide_examples import (
    UNSET,
    User,
    apply_payload,
    is_user_payload,
    merge_patch_field,
    patch_user,
)


class SlideExamplesTest(unittest.TestCase):
    def test_typing_extensions_source_has_lowercase_sentinel(self) -> None:
        self.assertTrue(hasattr(typing_extensions, "sentinel"))
        self.assertIs(
            getattr(typing_extensions, "Sentinel"),
            getattr(typing_extensions, "sentinel"),
        )

    def test_merge_patch_field_keeps_current_value_for_unset(self) -> None:
        self.assertEqual(merge_patch_field("current", UNSET), "current")

    def test_merge_patch_field_accepts_none_as_real_update(self) -> None:
        self.assertIsNone(merge_patch_field("current", None))

    def test_patch_user_separates_omit_none_and_value(self) -> None:
        user = User(
            id="user_123",
            email="koudai@example.com",
            nickname="Koudai",
            bio="Python",
        )

        patch_user(user)
        self.assertEqual(user.nickname, "Koudai")
        self.assertEqual(user.bio, "Python")

        patch_user(user, nickname=None)
        self.assertIsNone(user.nickname)
        self.assertEqual(user.bio, "Python")

        patch_user(user, nickname="Aono", bio="Typing")
        self.assertEqual(user.nickname, "Aono")
        self.assertEqual(user.bio, "Typing")

    def test_user_payload_shape_keeps_missing_and_none_distinct(self) -> None:
        self.assertTrue(
            is_user_payload(
                {
                    "id": "user_123",
                    "email": "koudai@example.com",
                    "nickname": None,
                }
            )
        )
        self.assertTrue(
            is_user_payload(
                {
                    "id": "user_123",
                    "email": "koudai@example.com",
                    "bio": "Python typing",
                }
            )
        )
        self.assertFalse(
            is_user_payload(
                {
                    "id": "user_123",
                    "email": "koudai@example.com",
                    "bio": None,
                }
            )
        )

    def test_apply_payload_updates_only_present_fields(self) -> None:
        user = User(
            id="user_123",
            email="koudai@example.com",
            nickname="Koudai",
            bio="Python",
        )

        apply_payload(
            user,
            {
                "id": "user_123",
                "email": "koudai@example.com",
                "bio": "Python typing",
            },
        )
        self.assertEqual(user.nickname, "Koudai")
        self.assertEqual(user.bio, "Python typing")

        apply_payload(
            user,
            {
                "id": "user_123",
                "email": "koudai@example.com",
                "nickname": None,
            },
        )
        self.assertIsNone(user.nickname)
        self.assertEqual(user.bio, "Python typing")


if __name__ == "__main__":
    unittest.main()
