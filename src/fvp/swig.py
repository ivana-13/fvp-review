"""SWiG annotations and the VALSE -> SWiG join.

VALSE action items (actant-swap.json, action-replacement.json) reference SWiG images by
filename and record the two words involved in the foil ('classes', 'classes_foil').
SWiG gives, per image, the verb, the roles with WordNet noun ids, and one box per role.
imsitu_space.json gives glosses per noun id and a natural-language definition per role.

The join maps a caption word to a SWiG role by matching it against the glosses of the
noun filling that role, and returns the role's box and definition.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path

from .geometry import is_valid_box

UNGROUNDED = [-1, -1, -1, -1]


def _singular_forms(word: str) -> set[str]:
    w = word.lower().strip()
    forms = {w}
    if w.endswith("ies"):
        forms.add(w[:-3] + "y")
    if w.endswith("es"):
        forms.add(w[:-2])
    if w.endswith("s"):
        forms.add(w[:-1])
    return forms


@dataclass
class SwigSpace:
    nouns: dict[str, dict]
    verbs: dict[str, dict]

    @classmethod
    def load(cls, path: Path) -> "SwigSpace":
        d = json.load(open(path, encoding="utf-8"))
        return cls(nouns=d["nouns"], verbs=d["verbs"])

    def glosses(self, noun_id: str) -> list[str]:
        if noun_id in self.nouns:
            return [g.lower() for g in self.nouns[noun_id].get("gloss", [])]
        return []

    def role_def(self, verb: str, role: str) -> str:
        try:
            return self.verbs[verb]["roles"][role]["def"]
        except KeyError:
            return role


@dataclass
class SwigImage:
    image_file: str
    split: str
    verb: str
    width: int
    height: int
    bb: dict[str, list[int]]
    frames: list[dict[str, str]]

    def role_nouns(self, role: str) -> list[str]:
        """All noun ids any of the three annotators used for this role (non-empty)."""
        out = []
        for fr in self.frames:
            n = fr.get(role, "")
            if n and n not in out:
                out.append(n)
        return out


def load_swig_annotations(swig_dir: Path, splits=("test", "dev", "train")) -> dict[str, SwigImage]:
    images: dict[str, SwigImage] = {}
    for split in splits:
        d = json.load(open(swig_dir / f"{split}.json", encoding="utf-8"))
        for fname, rec in d.items():
            images[fname] = SwigImage(
                image_file=fname,
                split=split,
                verb=rec["verb"],
                width=rec["width"],
                height=rec["height"],
                bb=rec["bb"],
                frames=rec["frames"],
            )
    return images


def match_word_to_role(word: str, img: SwigImage, space: SwigSpace) -> str | None:
    """Return the SWiG role whose noun glosses contain the word (or its singular), else None.

    Prefers roles other than 'place' when several match, because captions usually
    name participants, not locations. Multi-word glosses match on any token.
    """
    forms = _singular_forms(word)
    candidates: list[str] = []
    for role in img.bb.keys():
        for noun_id in img.role_nouns(role):
            for g in space.glosses(noun_id):
                tokens = set(g.split()) | {g}
                if forms & tokens:
                    candidates.append(role)
                    break
            if candidates and candidates[-1] == role:
                break
    if not candidates:
        return None
    non_place = [r for r in candidates if r != "place"]
    return (non_place or candidates)[0]


@dataclass
class JoinedItem:
    valse_id: str
    subset: str  # 'actant-swap' or 'action-replacement'
    image_file: str
    split: str
    verb: str
    width: int
    height: int
    caption: str
    foil: str
    classes: str
    classes_foil: str
    mturk: dict
    roles: dict[str, dict] = field(default_factory=dict)  # role -> {noun_ids, glosses, bbox, def}
    targets: dict[str, dict] = field(default_factory=dict)  # word -> {role, bbox, def}

    def to_json(self) -> dict:
        return self.__dict__


def join_valse_with_swig(
    valse_path: Path, subset: str, swig: dict[str, SwigImage], space: SwigSpace
) -> list[JoinedItem]:
    d = json.load(open(valse_path, encoding="utf-8"))
    out: list[JoinedItem] = []
    for vid, v in d.items():
        img = swig.get(v["image_file"])
        if img is None:
            continue
        mturk = v.get("mturk", {})
        if isinstance(mturk, str):
            try:
                mturk = ast.literal_eval(mturk)
            except Exception:
                mturk = {}
        roles = {}
        for role, box in img.bb.items():
            nouns = img.role_nouns(role)
            roles[role] = {
                "noun_ids": nouns,
                "glosses": sorted({g for n in nouns for g in space.glosses(n)}),
                "bbox": box,
                "grounded": is_valid_box(box),
                "def": space.role_def(img.verb, role),
            }
        item = JoinedItem(
            valse_id=vid,
            subset=subset,
            image_file=img.image_file,
            split=img.split,
            verb=img.verb,
            width=img.width,
            height=img.height,
            caption=v["caption"],
            foil=v["foil"],
            classes=v.get("classes", ""),
            classes_foil=v.get("classes_foil", ""),
            mturk=mturk,
            roles=roles,
        )
        if subset == "actant-swap":
            words = [v.get("classes", ""), v.get("classes_foil", "")]
        else:
            words = []  # the swapped word is the verb; the pointing target is the agent
        for w in words:
            role = match_word_to_role(w, img, space)
            if role is not None:
                item.targets[w] = {"role": role, "bbox": img.bb[role], "def": space.role_def(img.verb, role)}
        if "agent" in img.bb:
            item.targets.setdefault("__agent__", {"role": "agent", "bbox": img.bb["agent"], "def": space.role_def(img.verb, "agent")})
        out.append(item)
    return out


def mturk_valid(item: JoinedItem, min_caption_votes: int = 2) -> bool:
    return int(item.mturk.get("caption", 0)) >= min_caption_votes
