"use client";

import { useLocale, useMessages } from "next-intl";
import { useEffect, useMemo } from "react";

const originalText = new WeakMap<Text, string>();
const originalAttributes = new WeakMap<Element, Map<string, string>>();
const attributes = ["aria-label", "placeholder", "title"] as const;

export function LegacyUiLocalizer() {
  const locale = useLocale();
  const messages = useMessages() as Record<string, unknown>;
  const catalog = useMemo(() => (messages.legacy || {}) as Record<string, string>, [messages]);

  useEffect(() => {
    function translatedText(original: string) {
      const trimmed = original.trim();
      const translated = catalog[trimmed];
      return translated ? original.replace(trimmed, translated) : original;
    }

    function translateText(node: Text) {
      const original = originalText.get(node) || node.data;
      if (!originalText.has(node)) originalText.set(node, original);
      const next = translatedText(original);
      if (node.data !== next) node.data = next;
    }

    function translateElement(element: Element) {
      if (element.closest("[data-i18n-preserve]")) return;
      let originals = originalAttributes.get(element);
      if (!originals) {
        originals = new Map();
        originalAttributes.set(element, originals);
      }
      for (const attribute of attributes) {
        const value = element.getAttribute(attribute);
        if (!value) continue;
        const original = originals.get(attribute) || value;
        if (!originals.has(attribute)) originals.set(attribute, original);
        const next = catalog[original] || original;
        if (value !== next) element.setAttribute(attribute, next);
      }
      for (const child of element.childNodes) {
        if (child.nodeType === Node.TEXT_NODE) translateText(child as Text);
        else if (child instanceof Element) translateElement(child);
      }
    }

    const apply = () => translateElement(document.body);
    apply();
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === "characterData") {
          const node = mutation.target as Text;
          const previousOriginal = originalText.get(node);
          if (previousOriginal && node.data !== translatedText(previousOriginal)) {
            originalText.set(node, node.data);
          }
          translateText(node);
          continue;
        }

        if (mutation.type === "attributes") {
          const element = mutation.target as Element;
          const attribute = mutation.attributeName;
          if (!attribute || !attributes.includes(attribute as (typeof attributes)[number])) continue;
          const value = element.getAttribute(attribute);
          const originals = originalAttributes.get(element);
          const previousOriginal = originals?.get(attribute);
          const previousTranslation = previousOriginal ? catalog[previousOriginal] || previousOriginal : null;
          if (value && previousOriginal && value !== previousTranslation) originals?.set(attribute, value);
          translateElement(element);
          continue;
        }

        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.TEXT_NODE) translateText(node as Text);
          else if (node instanceof Element) translateElement(node);
        }
      }
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: [...attributes],
    });
    return () => observer.disconnect();
  }, [catalog, locale]);

  return null;
}
