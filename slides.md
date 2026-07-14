---
theme: default
background: '#ffffff'
colorSchema: 'light'
title: "Beyond Optional in Real-World Projects"
info: |
  EuroPython 2026 talk. Modeling missing keys, explicit None,
  and unset inputs with TypedDict, sentinels, and dataclasses.
layout: cover
class: cover
highlighter: shiki
lineNumbers: false
transition: fade
mdc: true
fonts:
  sans: 'Lato, "Noto Sans JP", sans-serif'
  mono: 'JetBrains Mono, monospace'
---

# Beyond Optional in Real-World Projects


### Missing, `None`, and Unset

<div class="cover-author">Koudai Aono</div>
<div class="cover-conf">EuroPython 2026</div>

<!--
Finish this slide by 00:15
-->
---
layout: default
---

## At the HTTP boundary


<div class="http-boundary-strip">
  <div class="http-node">Outside client</div>
  <div class="http-arrow">→</div>
  <div class="http-boundary-node">HTTP PATCH payload</div>
  <div class="http-arrow">→</div>
  <div class="http-node python">Python handler</div>
</div>

<div class="request-line">PATCH <code>/users/user_123</code></div>

<div class="payload-examples">
  <div class="payload-card" v-click>
    <div class="payload-label">Send value</div>
    <div class="payload-json">{"nickname": "Koudai"}</div>
    <div class="payload-meaning">replace nickname</div>
  </div>
  <div class="payload-card accent" v-click>
    <div class="payload-label">Send null</div>
    <div class="payload-json">{"nickname": null}</div>
    <div class="payload-meaning">clear nickname</div>
  </div>
  <div class="payload-card" v-click>
    <div class="payload-label">Omit nickname</div>
    <div class="payload-json">{"bio": "Python typing"}</div>
    <div class="payload-meaning">update bio, keep nickname</div>
  </div>
</div>

<!--
Finish this slide by 00:50
-->
---
layout: default
class: compact-code caller-type
---

## The boundary drops intent 🫥


<div class="payload-examples two">
  <div class="payload-card accent" v-click>
    <div class="payload-label">Request body</div>
    <div class="payload-json">{"nickname": null}</div>
    <div class="payload-meaning">clear nickname</div>
  </div>
  <div class="payload-card" v-click>
    <div class="payload-label">Request body</div>
    <div class="payload-json">{"bio": "Python typing"}</div>
    <div class="payload-meaning">update bio, keep nickname</div>
  </div>
</div>

```python {none|2-3|4}
def patch_endpoint(payload: dict) -> None:
    nickname = payload.get("nickname")
    bio = payload.get("bio")
    patch_user(nickname=nickname, bio=bio)
```

<div v-click class="collapse-result">
  Both requests: nickname is None
</div>

<!--
Finish this slide by 01:15
-->
---
layout: default
---

## About Me 👋


<div class="about-layout">
<div class="about-left">

<v-clicks>

- Python developer tools / **OSS maintainer**
- OSS: **datamodel-code-generator**, pydantic / ruff PyCharm plugins
- This talk comes from schema → Python gaps seen in real projects
- **PEP 750 (t-strings)** co-author; created **t-linter**
- Speaker: PyCon US 2024 / 2025 / 2026
- Speaker: EuroPython 2024 / 2025
- Invited speaker: PyCon JP 2025
- GitHub: [@koxudaxi](https://github.com/koxudaxi)

</v-clicks>

</div>
<div class="about-right">
  <div class="about-photo-stack">
    <img src="./assets/koudai-aono-1200.jpg" alt="Koudai Aono" class="about-photo" />
    <img src="./assets/rabbit.jpg" alt="GitHub icon" class="about-rabbit" />
  </div>
  <div class="about-name">Koudai Aono</div>
  <div class="about-handle">@koxudaxi</div>
  <div class="about-qr-row">
    <img src="./assets/qr-github.png" alt="GitHub QR" class="qr-img about-qr" />
    <div class="qr-label">github.com/<br/>koxudaxi</div>
  </div>
</div>
</div>

<!--
Finish this slide by 01:35
-->
---
layout: default
class: compact-code
---

## Goal 🎯


<v-clicks>

- Stop conflating **missing**, **`None`**, and **unset**
- Model boundary **shape** before domain **meaning**
- Narrow raw input before business logic uses it
- Use sentinels for safe **partial updates**
- Build the pattern with **typing** and **dataclasses**

</v-clicks>

<div class="red-box" style="margin-top: 0.8rem; font-size: 0.9em; font-weight: 900;">
typing + dataclasses: payload → normalized update → domain model
</div>

<!--
Finish this slide by 01:50
-->
---
layout: default
class: agenda
---

## Agenda 📋


<div class="about-layout">
<div class="about-left">

1. The real bug 🐛
2. Boundary models with `TypedDict` 📦
3. Unset inputs 🚫
4. Safe extraction 🔍
5. Domain model with `dataclasses` 🏛️
6. Recap ✅

</div>
<div class="about-right">
  <img src="./assets/qr-repo.png" alt="Repo QR" class="qr-img" />
  <div class="qr-label">github.com/koxudaxi/<br/>europython_2026</div>
</div>
</div>

<!--
Finish this slide by 02:00
-->
---
layout: section
class: section
---

<div class="section-num">1.</div>
<div class="section-title">The Real Bug 🐛</div>

<!--
Finish this slide by 02:10
-->
---
layout: default
---

## "No value" changes by layer 🎭


<table class="focus-table">
  <thead>
    <tr><th>Layer</th><th>Example</th><th>Python sees</th><th>Intent</th></tr>
  </thead>
  <tbody>
    <tr v-click><td>HTTP payload</td><td><code>{"nickname": null}</code></td><td>value is <code>None</code></td><td>clear the value</td></tr>
    <tr v-click><td>HTTP payload</td><td><code>{"bio": "Python typing"}</code></td><td><code>nickname</code> key is absent</td><td>leave nickname unchanged</td></tr>
    <tr v-click><td>Python call</td><td>argument omitted</td><td>argument not provided</td><td>keep current value</td></tr>
  </tbody>
</table>

<!--
Finish this slide by 02:45
-->
---
layout: default
---

## Why `T | None` is not enough ❌


```python {none|4|6}
def update_user(
    user_id: str,
    *,
    nickname: str | None = None,
) -> None:
    user.nickname = nickname
```

<v-click>

<div class="question-callout">
  Did the caller omit <code>nickname</code>, or pass <code>nickname=None</code>?
</div>

</v-click>

<!--
Finish this slide by 03:25
-->
---
layout: default
---

## Recap: what broke 🧭


<table class="focus-table">
  <thead>
    <tr><th>Where</th><th>Two meanings became one</th><th>What got lost</th></tr>
  </thead>
  <tbody>
    <tr v-click><td>HTTP payload</td><td>missing key + <code>null</code></td><td>whether the client sent the field</td></tr>
    <tr v-click><td>Python argument</td><td>omitted arg + <code>None</code></td><td>whether the caller meant clear</td></tr>
  </tbody>
</table>

<div v-click class="red-box section-next-note">
One <code>None</code>, several decisions. We fix this next.
</div>

<!--
Finish this slide by 04:30
-->
---
layout: section
class: section
---

<div class="section-num">2.</div>
<div class="section-title">Boundary models with <code>TypedDict</code> 📦</div>

<!--
Finish this slide by 04:40
-->
---
layout: default
---

## Where the bug starts 🚪


<div class="boundary-flow">
  <div class="boundary-zone outside">
    <div class="boundary-zone-title">Outside world</div>
    <div class="boundary-chip">HTTP request</div>
    <div class="boundary-chip">JSON payload</div>
    <div class="boundary-note">untyped at runtime</div>
  </div>
  <div class="boundary-crossing">
    <div class="boundary-line"></div>
    <div class="boundary-label">boundary</div>
    <div class="boundary-arrow">→</div>
  </div>
  <div class="boundary-zone python">
    <div class="boundary-zone-title">Python world</div>
    <div class="boundary-chip">TypedDict contract</div>
    <div class="boundary-chip">domain code</div>
    <div class="boundary-note">checked by tools</div>
  </div>
</div>

<v-clicks>

- Data arrives as **runtime JSON**, not Python types
- First, name the expected **payload shape**
- Keep that shape separate from **domain meaning**

</v-clicks>

<!--
Finish this slide by 05:20
-->
---
layout: default
---

## `TypedDict` is a static contract


```python {none|3|4-7}
from typing import TypedDict

class UserPayload(TypedDict):
    id: str
    email: str
    nickname: str | None
    bio: str
```

<v-clicks>

- Static only: runtime value is still a **plain `dict`**
- Plain keys are **required by default**

</v-clicks>

<!--
Finish this slide by 06:05
-->
---
layout: default
---

## `total=False`: every key may be omitted


```python {none|1|2-5}
class UserPayload(TypedDict, total=False):
    id: str
    email: str
    nickname: str | None
    bio: str
```

<v-clicks>

- **Every** key may be omitted, including `id` and `email`
- Values are still non-null `str`
- Real payloads mix **required** and **omittable** keys

</v-clicks>

<!--
Finish this slide by 06:50
-->
---
layout: default
---

## Required by default, omittable by name 🎯


<div class="note">PEP 655 — <code>typing</code> 3.11+ / <code>typing_extensions</code> 4.0+</div>

```python {none|1|4-5|6-7}
from typing import TypedDict, NotRequired

class UserPayload(TypedDict):
    id: str
    email: str
    nickname: NotRequired[str | None]
    bio: NotRequired[str]
```

<!--
Finish this slide by 07:40
-->
---
layout: default
class: compact-code
---

## When `Required` helps


```python {none|1|3|4-5|6-7}
from typing import Required, TypedDict

class UserPayload(TypedDict, total=False):
    id: Required[str]
    email: Required[str]
    nickname: str | None
    bio: str
```

<v-clicks>

- In <code>total=False</code>, unmarked keys are **omittable**
- Use <code>Required[T]</code> when required keys are the **minority**

</v-clicks>

<!--
Finish this slide by 08:25
-->
---
layout: default
class: dense
---

## Missing keys vs `None` values 🔍


<table class="focus-table">
  <thead>
    <tr><th>Field type</th><th>Can omit key?</th><th>Allows <code>None</code>?</th><th>Meaning</th></tr>
  </thead>
  <tbody>
    <tr v-click><td><code>id: str</code></td><td>No</td><td>No</td><td>required value</td></tr>
    <tr v-click><td><code>nickname: str | None</code></td><td>No</td><td>Yes</td><td>required nullable value</td></tr>
    <tr v-click><td><code>bio: NotRequired[str]</code></td><td>Yes</td><td>No</td><td>omittable key, non-null value</td></tr>
    <tr v-click><td><code>nickname: NotRequired[str | None]</code></td><td>Yes</td><td>Yes</td><td>omittable key, nullable value</td></tr>
  </tbody>
</table>

<!--
Finish this slide by 09:15
-->
---
layout: default
class: code-compare
---

## Before → After


<div class="two-cols">
<div>
<div class="col-label">Before — total=False</div>

```python {none|1-4|5-6|7-8}
class UserPayload(
    TypedDict,
    total=False,
):
    id: str
    email: str
    nickname: str | None
    bio: str
```

</div>
<div>
<div class="col-label">After — key presence</div>

```python {none|4-5|6-8|9}
class UserPayload(
    TypedDict,
):
    id: str
    email: str
    nickname: NotRequired[
        str | None
    ]
    bio: NotRequired[str]
```

</div>
</div>

<!--
Finish this slide by 10:30
-->
---
layout: default
---

## `ReadOnly` for boundary safety 🔒


<div class="note">PEP 705 — <code>typing</code> 3.13+ / <code>typing_extensions</code> 4.9+</div>

```python {none|4-5|6-7}
from typing import TypedDict, NotRequired, ReadOnly

class UserPayload(TypedDict):
    id: ReadOnly[str]
    email: ReadOnly[str]
    nickname: NotRequired[ReadOnly[str | None]]
    bio: NotRequired[ReadOnly[str]]
```

<div class="note">
  <strong>Boundary rule:</strong> assigning to a <code>ReadOnly</code> key is a type error.
</div>

<!--
Finish this slide by 11:20
-->
---
layout: default
---

## Recap: boundary fixed 📦


<v-clicks>

- `TypedDict` is a **static contract**, not runtime validation
- `NotRequired[T]` models **missing keys**
- `T | None` models **nullable values**
- `ReadOnly` makes payload mutation a **type error**
- Normalize boundary payloads before domain logic

</v-clicks>

<!--
Finish this slide by 12:00
-->
---
layout: section
class: section
---

<div class="section-num">3.</div>
<div class="section-title">Unset inputs 🚫</div>

<!--
Finish this slide by 12:10
-->
---
layout: default
class: compact-code
---

## A PATCH request has three intents


<div class="patch-intent-row">
  <div class="patch-intent-card">
    <div class="patch-intent-label">Omit field</div>
    <div class="patch-intent-meaning">leave current value</div>
  </div>
  <div class="patch-intent-card accent">
    <div class="patch-intent-label">Send <code>null</code></div>
    <div class="patch-intent-meaning">clear the value</div>
  </div>
  <div class="patch-intent-card">
    <div class="patch-intent-label">Send a value</div>
    <div class="patch-intent-meaning">replace the value</div>
  </div>
</div>

```python {none|2-3|5-6}
def patch_user(user: User, *,
               nickname: str | None = None,
               bio: str | None = None) -> User:
    user.nickname = nickname
    user.bio = bio
    return user
```

<div class="note">Example starts after boundary normalization.</div>

<!--
Finish this slide by 12:50
-->
---
layout: default
---

## Why default `None` fails ❌


<table class="focus-table">
  <thead>
    <tr><th>Caller wrote</th><th>Intended meaning</th><th><code>nickname</code> inside</th></tr>
  </thead>
  <tbody>
    <tr v-click><td><code>patch_user(user)</code></td><td>leave unchanged</td><td><code>None</code></td></tr>
    <tr v-click><td><code>..., nickname=None</code></td><td>clear value</td><td><code>None</code></td></tr>
    <tr v-click><td><code>..., nickname="Koudai"</code></td><td>replace value</td><td><code>"Koudai"</code></td></tr>
  </tbody>
</table>

<div class="comparison-takeaway">
  <strong>Problem:</strong> the first two rows collapse to the same inside value.
</div>

<!--
Finish this slide by 13:35
-->
---
layout: default
class: compact-code
---

## Fix #1: use an unset marker


```python {none|1|3-4|5|7}
UNSET = object()

def patch_user(user: User, *,
               nickname=UNSET,
               bio=UNSET) -> User:
    if nickname is not UNSET:
        user.nickname = nickname
    if bio is not UNSET:
        user.bio = bio
    return user
```

<div class="note"><code>object()</code> makes a unique marker; compare it with <code>is</code>.</div>

<!--
Finish this slide by 14:20
-->
---
layout: default
---

## Fix #2: give the marker a type


```python {none|3-4|6}
from typing import Final

class _UnsetType:
    pass

UNSET: Final = _UnsetType()
```

<v-clicks>

- `_UnsetType` gives the checker a **distinct type**
- `UNSET` means "not provided"; checks narrow back to `str | None`

</v-clicks>

<!--
Finish this slide by 15:00
-->
---
layout: default
class: compact-code
---

## Using the typed sentinel


```python {none|4-5|7-8|9-10}
def patch_user(
    user: User,
    *,
    nickname: str | None | _UnsetType = UNSET,
    bio: str | None | _UnsetType = UNSET,
) -> User:
    if not isinstance(nickname, _UnsetType):
        user.nickname = nickname
    if not isinstance(bio, _UnsetType):
        user.bio = bio
    return user
```

<!--
Finish this slide by 15:45
-->
---
layout: default
class: compact-code recommended-sentinel
---

## Recommended: `sentinel()`


<div class="note">Python 3.15 adds <code>builtins.sentinel</code>; <code>typing_extensions</code> 4.16+ provides the lowercase backport.</div>

```python {none|1|2|6-8}
from typing_extensions import sentinel
UNSET = sentinel("UNSET")
def patch_user(
    user: User,
    *,
    nickname: str | None | UNSET = UNSET,
    bio: str | None | UNSET = UNSET,
) -> User:
    ...
```

<div class="comparison-takeaway">
  <strong>Current API:</strong> import and call lowercase <code>sentinel</code>; <code>Sentinel</code> is only a soft-deprecated compatibility alias.
</div>

<!--
Finish this slide by 16:20
-->
---
layout: default
---

## Define `merge_patch_field()` once ♻️


```python {none|1-3|4}
def merge_patch_field[T](
    current: T, update: T | UNSET,
) -> T:
    return current if update is UNSET else update
```

<div class="note">PEP 661 lets a named sentinel appear in annotations; PEP 695 generic syntax is Python 3.12+.</div>

<div class="comparison-takeaway">
  <strong>Policy:</strong> this helper defines what "not provided" means for every field.
</div>

<!--
Finish this slide by 16:55
-->
---
layout: default
class: compact-code
---

## Resolve the PATCH update


```python {none|4-5|7-10}
def patch_user(
    user: User,
    *,
    nickname: str | None | UNSET = UNSET,
    bio: str | None | UNSET = UNSET,
) -> User:
    user.nickname = merge_patch_field(
        user.nickname, nickname
    )
    user.bio = merge_patch_field(user.bio, bio)
    return user
```

<!--
Finish this slide by 17:20
-->
---
layout: default
---

## Recap: updates fixed 🚫


<table class="focus-table">
  <thead>
    <tr><th>Problem</th><th>Section 3 answer</th><th>Why it matters</th></tr>
  </thead>
  <tbody>
    <tr v-click><td>default <code>None</code> collapses intent</td><td>use a sentinel for omitted input</td><td><code>null</code> stays meaningful</td></tr>
    <tr v-click><td><code>object()</code> is runtime-only</td><td>prefer a named sentinel</td><td>the checker sees a distinct type</td></tr>
    <tr v-click><td>field branches copy policy</td><td>centralize it in <code>merge_patch_field()</code></td><td>each field follows one rule</td></tr>
  </tbody>
</table>

<div class="comparison-takeaway">
  <strong>Rule:</strong> keep the update policy at the boundary, then reuse it for every field.
</div>

<!--
Finish this slide by 17:30
-->
---
layout: section
class: section
---

<div class="section-num">4.</div>
<div class="section-title">Safe extraction 🔍</div>

<!--
Finish this slide by 17:40
-->
---
layout: default
---

## Extraction turns raw dicts into meaning


<div class="extraction-flow">
  <div class="extraction-node raw">
    <div>queue message</div>
    <div class="extraction-example">decoded JSON dict</div>
  </div>
  <div class="extraction-arrow">→</div>
  <div class="extraction-node check">
    <div>shape check</div>
    <div class="extraction-example"><code>is_user_payload()</code></div>
  </div>
  <div class="extraction-arrow">→</div>
  <div class="extraction-node typed">
    <div><code>UserPayload</code></div>
    <div class="extraction-example">safe keys</div>
  </div>
</div>

<div class="comparison-takeaway">
  <strong>We named the boundary shape.</strong> Now we need to earn that type from a decoded payload.
</div>

<!--
Finish this slide by 18:15
-->
---
layout: default
class: compact-code payload-shapes
---

## Name payload shapes 🏷️


<div class="note">PEP 695 — <code>type</code> statement is Python 3.12+.</div>

```python {none|1-2|3-4|9-10}
type UserId = str
type EmailAddress = str
type NicknameUpdate = str | None
type BioUpdate = str

class UserPayload(TypedDict):
    id: UserId
    email: EmailAddress
    nickname: NotRequired[NicknameUpdate]
    bio: NotRequired[BioUpdate]
```

<!--
Finish this slide by 18:55
-->
---
layout: default
class: compact-code narrowing-typeis
---

## Narrowing with `TypeIs`


<div class="note">PEP 742 — <code>typing</code> 3.13+ / <code>typing_extensions</code> 4.10+</div>

```python {none|3-5}
from typing import TypeIs

def is_str_or_none(
    x: object,
) -> TypeIs[NicknameUpdate]:
    return x is None or isinstance(x, str)
```

<div class="comparison-takeaway">
  <strong>TypeIs says:</strong> if this returns true, the checked value can be treated as the target type.
</div>

<!--
Finish this slide by 19:35
-->
---
layout: default
class: compact-code shape-predicate
---

## One shape predicate


```python {none|1|2-4|5-10}
type DecodedPayload = Mapping[str, object]
def is_user_payload(
    p: DecodedPayload,
) -> TypeIs[UserPayload]:
    return (
        isinstance(p.get("id"), str)
        and isinstance(p.get("email"), str)
        and (
            "nickname" not in p
            or is_str_or_none(p["nickname"])
        )
        and ("bio" not in p or is_str(p["bio"]))
    )
```

<!--
Finish this slide by 20:25
-->
---
layout: default
class: compact-code caller-type
---

## And the caller gets a type


<div class="col-label">Before — <code>email</code> is still <code>object</code> <span class="type-error-inline">type error: expected <code>str</code></span> <span class="type-error-inline">runtime risk: missing key</span></div>

```python {none|1|2}
def handle(payload: Mapping[str, object]) -> None:
    send_email(payload["email"])
```

<div class="col-label" style="margin-top: 0.45rem;">After <code>TypeIs</code> — <code>email</code> is <code>str</code></div>

```python {none|1|2-3}
def handle(payload: Mapping[str, object]) -> None:
    if is_user_payload(payload):
        send_email(payload["email"])
```

<!--
Finish this slide by 21:30
-->
---
layout: default
---

## Recap: extraction fixed 🔍


<v-clicks>

- Name payload field shapes with `type` aliases
- Put decoded-dict checks in small `TypeIs` predicates
- After the predicate, application code sees typed payloads

</v-clicks>

<!--
Finish this slide by 22:00
-->
---
layout: section
class: section
---

<div class="section-num">5.</div>
<div class="section-title">Domain model with <code>dataclasses</code> 🏛️</div>

<!--
Finish this slide by 22:10
-->
---
layout: default
---

## Stop carrying boundary shapes


<div class="domain-flow">
  <div class="domain-node boundary">
    <div class="domain-node-title">Boundary</div>
    <div class="domain-node-main">TypedDict</div>
    <div class="domain-node-note">shape on the wire</div>
  </div>
  <div class="domain-arrow">→</div>
  <div class="domain-node normalize">
    <div class="domain-node-title">Normalize</div>
    <div class="domain-node-main">apply_<br>payload()</div>
    <div class="domain-node-note">one policy point</div>
  </div>
  <div class="domain-arrow">→</div>
  <div class="domain-node model">
    <div class="domain-node-title">Domain</div>
    <div class="domain-node-main">dataclass</div>
    <div class="domain-node-note">what it means</div>
  </div>
  <div class="domain-arrow">→</div>
  <div class="domain-node application">
    <div class="domain-node-title">Use</div>
    <div class="domain-node-main">Business / DB</div>
    <div class="domain-node-note">works with <code>User</code></div>
  </div>
</div>

<!--
Finish this slide by 22:45
-->
---
layout: default
---

## Why split 🪓


<table class="focus-table">
  <thead>
    <tr><th>Question</th><th>Boundary <code>TypedDict</code></th><th>Domain <code>dataclass</code></th></tr>
  </thead>
  <tbody>
    <tr v-click><td>What is it?</td><td>external payload shape</td><td>internal application value</td></tr>
    <tr v-click><td>Can keys be missing?</td><td>yes, with <code>NotRequired</code></td><td>no, fields exist</td></tr>
    <tr v-click><td>Omitted updates?</td><td>payload may omit keys</td><td>existing fields stay unchanged</td></tr>
    <tr v-click><td>Where is policy?</td><td>not in the dict shape</td><td>in <code>apply_payload()</code></td></tr>
  </tbody>
</table>

<div class="comparison-takeaway">
  <strong>Split because:</strong> wire shape and domain invariants are different contracts.
</div>

<!--
Finish this slide by 23:35
-->
---
layout: default
class: compact-code
---

## The domain dataclass


```python {none|3|5-8}
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    nickname: str | None
    bio: str | None
```

<div class="comparison-takeaway">
  <strong>After normalization:</strong> fields exist; no <code>NotRequired</code> or <code>UNSET</code> in the model.
</div>

<!--
Finish this slide by 24:20
-->
---
layout: default
class: compact-code
---

## Normalize updates at the boundary


```python {none|2-3|4-6|7-8}
def apply_payload(user: User, p: UserPayload):
    nickname = p.get("nickname", UNSET)
    bio = p.get("bio", UNSET)
    user.nickname = merge_patch_field(
        user.nickname, nickname
    )
    user.bio = merge_patch_field(user.bio, bio)
    return user
```

<div class="comparison-takeaway">
  <strong>Boundary rule:</strong> missing keys become <code>UNSET</code>; the helper keeps current values.
</div>

<!--
Finish this slide by 25:20
-->
---
layout: default
---

## One conversion point 🎯


<table class="focus-table">
  <thead>
    <tr><th>Before <code>apply_payload()</code></th><th>After <code>apply_payload()</code></th></tr>
  </thead>
  <tbody>
    <tr v-click><td>keys may be missing</td><td>fields exist</td></tr>
    <tr v-click><td><code>.get()</code> needs intent</td><td><code>UNSET</code> keeps intent</td></tr>
    <tr v-click><td>wire names are visible</td><td>business code uses <code>User</code></td></tr>
    <tr v-click><td>raw payload stops here</td><td>DB and rules use domain values</td></tr>
  </tbody>
</table>

<div class="comparison-takeaway">
  <strong>Normalization:</strong> one function absorbs boundary weirdness before domain code starts.
</div>

<!--
Finish this slide by 26:10
-->
---
layout: default
---

## Recap: model fixed 🏛️


<v-clicks>

- Keep `TypedDict` at the edge
- Apply updates into a dataclass
- Business logic sees meaning, not wire format
- Refactors touch the conversion point, not every caller

</v-clicks>

<!--
Finish this slide by 27:00
-->
---
layout: section
class: section
---

<div class="section-num">6.</div>
<div class="section-title">Recap ✅</div>

<!--
Finish this slide by 27:05
-->
---
layout: default
---

## Three takeaways 🎁


<table class="focus-table">
  <thead>
    <tr><th>Confusion</th><th>Use</th><th>Keep it</th></tr>
  </thead>
  <tbody>
    <tr v-click><td>missing key vs <code>None</code></td><td><code>NotRequired[T]</code></td><td>boundary payload</td></tr>
    <tr v-click><td>omitted argument vs <code>None</code></td><td><code>sentinel("UNSET")</code></td><td>update API</td></tr>
    <tr v-click><td>wire shape vs domain value</td><td><code>TypedDict</code> → <code>dataclass</code></td><td>conversion point</td></tr>
  </tbody>
</table>

<!--
Finish this slide by 27:40
-->
---
layout: default
class: dense
---

## Adoption checklist ✔️


<table class="focus-table">
  <thead>
    <tr><th>Step</th><th>Change</th><th>Done when</th></tr>
  </thead>
  <tbody>
    <tr v-click><td>1</td><td>pick one boundary crossing</td><td>endpoint / queue / file chosen</td></tr>
    <tr v-click><td>2</td><td>write its <code>TypedDict</code> contract</td><td>missing keys use <code>NotRequired</code></td></tr>
    <tr v-click><td>3</td><td>narrow raw input at the edge</td><td>raw <code>dict</code>/<code>object</code> stops there</td></tr>
    <tr v-click><td>4</td><td>add <code>UNSET</code> with <code>sentinel()</code></td><td>omit / null / value stay separate</td></tr>
    <tr v-click><td>5</td><td>apply into a <code>dataclass</code></td><td>business logic and DB use domain values</td></tr>
  </tbody>
</table>

<div class="comparison-takeaway">
  <strong>Start small:</strong> one boundary is enough to prove the pattern.
</div>

<!--
Finish this slide by 28:35
-->
---
layout: default
class: tools-version
---

## Tools by Python version 🐍


<table class="focus-table">
  <thead>
    <tr><th>Need</th><th>Feature</th><th>Python</th><th>typing ext.</th></tr>
  </thead>
  <tbody>
    <tr v-click><td>payload shapes</td><td><code>TypedDict</code></td><td>3.8+</td><td>yes</td></tr>
    <tr v-click><td>missing keys</td><td><code>Required</code> / <code>NotRequired</code></td><td>3.11+</td><td>4.0+</td></tr>
    <tr v-click><td>aliases</td><td><code>type</code> statement</td><td>3.12+</td><td>-</td></tr>
    <tr v-click><td>immutability</td><td><code>ReadOnly</code></td><td>3.13+</td><td>4.9+</td></tr>
    <tr v-click><td>narrowing</td><td><code>TypeIs</code></td><td>3.13+</td><td>4.10+</td></tr>
    <tr v-click><td>sentinels</td><td><code>sentinel()</code></td><td>3.15+</td><td>4.16+</td></tr>
  </tbody>
</table>

<!--
Finish this slide by 29:30
-->
---
layout: cover
class: cover thanks
---

# Thank you!! 🙏


### Beyond Optional in Real-World Projects

<div class="cover-author">Koudai Aono — @koxudaxi</div>

<div style="margin-top: 1.6rem; display: flex; justify-content: center; gap: 2rem; align-items: center;">
  <div style="text-align: center;">
    <img src="./assets/qr-repo.png" alt="Repo QR" class="qr-img" />
    <div class="qr-label">github.com/koxudaxi/<br/>europython_2026</div>
  </div>
</div>

<!--
Finish this slide by 30:00
-->
