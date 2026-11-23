import { fireEvent, render, screen } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { expect, it } from "vitest";
import { navGroups } from "@/lib/nav-links";
import { NavMenu } from "./nav-menu";

it("includes the group's destinations in its server-rendered markup", () => {
  const group = navGroups[0];
  const markup = renderToStaticMarkup(<NavMenu group={group} />);
  const fragment = document.createElement("template");
  fragment.innerHTML = markup;
  const paths = Array.from(fragment.content.querySelectorAll("li a"), (link) => link.getAttribute("href"));
  expect(paths).toEqual(group.items.map((item) => item.href));
});

it("returns keyboard focus to the toggle when Escape closes a submenu from a link", () => {
  render(<NavMenu group={navGroups[0]} />);
  const toggle = screen.getByRole("button", { name: "AI 應用選單" });
  fireEvent.click(toggle);
  const link = screen.getByRole("link", { name: "AI 新聞" });
  link.focus();
  fireEvent.keyDown(link, { key: "Escape" });
  expect(toggle.getAttribute("aria-expanded")).toBe("false");
  expect(document.activeElement).toBe(toggle);
});
