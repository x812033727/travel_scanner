"""Display original text and cited UTF-8 byte ranges without inventing URLs."""
import html
from html.parser import HTMLParser

from .common import https_url, serialized, text_blocks


def byte_segment(text, start, end):
    raw = text.encode("utf-8")
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(raw):
        raise ValueError("invalid_citation_range")
    try:
        raw[:start].decode("utf-8")
        segment = raw[start:end].decode("utf-8")
        raw[end:].decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("citation_splits_utf8_character") from error
    return segment


def extract_urls(reply):
    result = []
    for block in text_blocks(reply):
        citations, rejected = [], []
        text = block.get("text", "")
        for annotation in block.get("annotations", []):
            if annotation.get("type") != "url_citation":
                continue
            try:
                url = https_url(annotation.get("url"))
                segment = byte_segment(text, annotation.get("start_index"), annotation.get("end_index"))
                citations.append({"url": url, "title": annotation.get("title") or url, "segment": segment})
            except ValueError as error:
                rejected.append(str(error))
        result.append({"text": text, "citations": citations, "rejected": rejected})
    return result


class Suggestions(HTMLParser):
    """Accept a narrow passive HTML subset; reject the whole widget on unsafe syntax.

    No rewriting or removal of individual links. Browser CSP is a second boundary.
    New Google widget markup requires review before it can be displayed.
    """
    tags = frozenset({"style", "div", "span", "a", "svg", "path", "g", "circle", "rect", "line", "polyline", "polygon", "p", "br"})

    def handle_starttag(self, tag, attrs):
        if tag not in self.tags:
            raise ValueError("unsupported_search_widget")
        for name, value in attrs:
            if name.lower().startswith("on") or name in {"src", "srcdoc", "action", "formaction", "xlink:href"}:
                raise ValueError("active_search_widget")
            if name == "href":
                https_url(value)
            if value and any(token in value.lower() for token in ["javascript:", "expression(", "@import", "url("]):
                raise ValueError("active_search_widget")

    def handle_data(self, data):
        if any(token in data.lower() for token in ["@import", "url(", "expression("]):
            raise ValueError("external_widget_styles")


def search_html(reply, *, fixture=False):
    data = serialized(reply)
    blocks = extract_urls(data)
    suggestions = [item["search_suggestions"] for step in data.get("steps", []) if step.get("type") == "google_search_result" for item in step.get("result", []) if isinstance(item, dict) and isinstance(item.get("search_suggestions"), str)]
    used_search = any(s.get("type") == "google_search_call" for s in data.get("steps", []))
    if not fixture and (not used_search or not suggestions or any(b["rejected"] for b in blocks)):
        raise ValueError("grounding_presentation_incomplete_do_not_display_answer")
    for widget in suggestions:
        parser = Suggestions(convert_charrefs=True)
        parser.feed(widget)
        parser.close()
    title = "作者合成回應・不是 Google 實測" if fixture else "本次搜尋回答"
    body = "<h1>" + title + "</h1>"
    for block in blocks:
        body += "<p class='answer'>" + html.escape(block["text"]) + "</p>"
        body += "<ul>" + "".join("<li><a href='" + html.escape(c["url"], quote=True) + "'>" + html.escape(c["title"]) + "</a><p>對應文字：" + html.escape(c["segment"]) + "</p></li>" for c in block["citations"]) + "</ul>"
        if not block["citations"]:
            body += "<p>本段未提供可追查引用，不能當作已核實。</p>"
    body += "".join(suggestions)  # Preserve Google-provided passive markup without modifying it.
    csp = "default-src 'none'; style-src 'unsafe-inline'; img-src 'none'; base-uri 'none'; form-action 'none'"
    return '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="' + csp + '"><title>搜尋引用練習</title><style>body{max-width:880px;margin:40px auto;padding:0 20px;font:18px/1.7 system-ui;color:#243449}a{overflow-wrap:anywhere}.answer{white-space:pre-wrap}li{margin:18px 0}</style>' + body + "</html>"


def file_answer(reply, documents):
    """Only expose citations mapped to one current local source and an exact quote.

    This verifies source identity and quotation presence, not entailment of the answer.
    """
    texts, citations = [], []
    for block in text_blocks(reply):
        texts.append(block.get("text", ""))
        for annotation in block.get("annotations", []):
            if annotation.get("type") != "file_citation":
                continue
            name = annotation.get("file_name")
            matches = [d for d in documents if d["display_name"] == name and d["status"] == "active"]
            if len(matches) != 1:
                continue
            source = annotation.get("source")
            if not isinstance(source, str) or not source.strip() or source not in matches[0]["text"]:
                continue
            citations.append({"document_id": matches[0]["id"], "version": matches[0]["version"], "file_name": name, "quote": source})
    if not citations:
        return {"status": "no_verified_evidence", "answer": "沒有能對到目前文件版本的引用，請查核來源。", "citations": []}
    return {"status": "needs_claim_review", "answer": "\n".join(texts), "citations": citations}
