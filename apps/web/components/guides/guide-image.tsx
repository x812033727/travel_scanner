"use client";

import { useCallback, useEffect, useRef, useState, type ComponentProps } from "react";

type GuideImageProps = Pick<ComponentProps<"img">,
  "alt" | "width" | "height" | "loading" | "fetchPriority" | "decoding" | "className" | "style"
> & { src: string };

/** Keep the original image in server HTML; only transient failures need client work. */
export function GuideImage(props: GuideImageProps) {
  return <RetryingImage key={props.src} {...props} />;
}

function RetryingImage({ src, alt, ...props }: GuideImageProps) {
  const image = useRef<HTMLImageElement>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [attempt, setAttempt] = useState(0);
  const clearRetry = useCallback(() => {
    if (timer.current !== null) clearTimeout(timer.current);
    timer.current = null;
  }, []);
  const retry = useCallback(() => {
    if (attempt >= 2 || timer.current !== null) return;
    // Back off and spread a row of failed covers over time instead of retrying in a burst.
    timer.current = setTimeout(() => {
      timer.current = null;
      setAttempt((value) => value + 1);
    }, (attempt === 0 ? 2000 : 5000) + Math.random() * 500);
  }, [attempt]);

  useEffect(() => {
    // An SSR image can fail before hydration attaches onError. Pending lazy images have
    // complete=false and must retain their native loading behavior.
    if (image.current?.complete && image.current.naturalWidth === 0) retry();
    return clearRetry;
  }, [retry, clearRetry]);

  const requestSrc = attempt === 0 ? src : `${src}${src.includes("?") ? "&" : "?"}image_retry=${attempt}`;
  // eslint-disable-next-line @next/next/no-img-element
  return <img {...props} ref={image} src={requestSrc} alt={alt} onError={retry} onLoad={clearRetry} />;
}
