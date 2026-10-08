"""Immutable course identities for two isolated four-season adult courses."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    key: str
    name_en: str
    name_zh: str
    season_names: tuple[str, ...]
    reading_range: tuple[int, int]
    writing_range: tuple[int, int]
    headline: str
    introduction: str

    @property
    def series_title(self) -> str:
        return f"Sunny & Pip: {self.name_en} English"

    @property
    def catalog_name(self) -> str:
        return f"{self.name_zh}英文48集課程目錄.csv"

    @property
    def archive_prefix(self) -> str:
        return f"Sunny_Pip_{self.name_en}"

    @property
    def all_archive_name(self) -> str:
        return f"{self.archive_prefix}_48_Episodes.zip"


COURSES = {
    "university": Course(
        "university", "University", "大學",
        ("學術學習與校園溝通", "閱讀研究與證據", "專題合作與探究", "成果表達與學術銜接"),
        (160, 200), (120, 160), "讀懂證據，<span>清楚參與學術交流。</span>",
        "從校園溝通到研究閱讀、合作探究與成果表達，練習有依據且有分寸的英文。"),
    "workplace": Course(
        "workplace", "Workplace", "職場",
        ("求職與入職", "日常職場溝通", "協作與問題處理", "提案簡報與職涯發展"),
        (140, 180), (100, 140), "說明需求，<span>完成有效的職場溝通。</span>",
        "從求職入職到協作、問題處理與提案簡報，練習明確、得體且可行的英文。"),
}


def get_course(key: str) -> Course:
    if not isinstance(key, str) or key not in COURSES:
        raise ValueError("Expected course university or workplace")
    return COURSES[key]


def course_for_episodes(episodes: list[dict]) -> Course:
    if not isinstance(episodes, list) or not episodes or not isinstance(episodes[0], dict):
        raise ValueError("Course needs a nonempty list of episodes")
    course = get_course(episodes[0].get("course"))
    for episode in episodes:
        if not isinstance(episode, dict) or episode.get("course") != course.key:
            raise ValueError("Episodes from different adult courses cannot be mixed")
        season = episode.get("season")
        if (type(season) is not int or not 1 <= season <= 4
                or type(episode.get("stage")) is not int or episode["stage"] != season
                or "grade" in episode):
            raise ValueError(f"{episode.get('id', '?')}: expected stage equal to season 1–4 and no grade")
    return course


def document_course(document: dict, expected: str | None = None, *, allow_empty: bool = False) -> Course:
    if not isinstance(document, dict):
        raise ValueError("Course source must be an object")
    course = get_course(document.get("course"))
    if expected is not None and course.key != get_course(expected).key:
        raise ValueError(f"Wrong course: expected {expected}, found {course.key}")
    if document.get("series_title") != course.series_title or document.get("version") != 4:
        raise ValueError(f"{course.key}: expected its series title and version 4")
    episodes = document.get("episodes")
    if allow_empty and episodes == []:
        return course
    if course_for_episodes(episodes) != course:
        raise ValueError("Top-level course differs from its episodes")
    return course
