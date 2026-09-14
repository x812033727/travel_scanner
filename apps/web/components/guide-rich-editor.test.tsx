import { useState } from "react";
import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { GuideRichEditor } from "./guide-rich-editor";
import { ContentBlocks } from "./content-blocks";
import type { CodeBlock, RichParagraphBlock } from "@/lib/content-blocks";

function Editor({ initial }: { initial: CodeBlock | RichParagraphBlock }) {
  const [block, setBlock] = useState(initial);
  return <><GuideRichEditor locale="zh-TW" block={block} onChange={setBlock} />
    <section aria-label="Preview"><ContentBlocks blocks={[block]} locale="zh-TW" articleLinks={[
      { kind: "life", slug: "visible", title: "Visible" },
    ]} /></section></>;
}

describe("guide rich editing and shared preview", () => {
  it("edits raw code without converting markup or whitespace", () => {
    render(<Editor initial={{ type: "code", language: "html", label: "index.html", code: "before" }} />);
    const code = '<p title="a&b">\n\tText <script>not executed</script>\n</p>\n';
    fireEvent.change(screen.getByLabelText("程式碼範例"), { target: { value: code } });
    fireEvent.change(screen.getByLabelText("輸入位置或檔名"), { target: { value: "sample.html" } });
    const preview = within(screen.getByRole("region", { name: "Preview" }));
    expect(preview.getByLabelText("sample.html").textContent).toBe(code);
    expect(document.querySelector("script")).toBeNull();
  });
  it("keeps article identity separate from display text and supports reordering", () => {
    render(<Editor initial={{ type: "rich_paragraph", inlines: [{ type: "text", text: "First " }] }} />);
    fireEvent.click(screen.getByRole("button", { name: "加入片段" }));
    fireEvent.change(screen.getByLabelText("文章類型 2"), { target: { value: "article" } });
    fireEvent.change(screen.getAllByLabelText("文字")[1], { target: { value: "相關教學" } });
    fireEvent.change(screen.getByLabelText("文章短網址"), { target: { value: "visible" } });
    const preview = within(screen.getByRole("region", { name: "Preview" }));
    expect(preview.getByRole("link", { name: "相關教學" }).getAttribute("href")).toBe("/zh-TW/life/visible");
    fireEvent.click(screen.getAllByRole("button", { name: "上移" })[1]);
    expect(screen.getByRole("region", { name: "Preview" }).textContent).toBe("相關教學First ");
    fireEvent.change(screen.getByLabelText("文章短網址"), { target: { value: "hidden" } });
    expect(preview.queryByRole("link")).toBeNull();
    expect(preview.getByText("相關教學")).toBeTruthy();
    fireEvent.click(screen.getAllByRole("button", { name: "移除" })[0]);
    expect(screen.getByRole("region", { name: "Preview" }).textContent).toBe("First ");
  });
});
