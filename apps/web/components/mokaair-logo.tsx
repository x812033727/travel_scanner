type MokaairLogoProps = Readonly<{
  className?: string;
  compact?: boolean;
}>;

export function MokaairLogo({ className = "", compact = false }: MokaairLogoProps) {
  return (
    <span
      aria-label="Mokaair"
      className={`mokaair-wordmark ${compact ? "mokaair-wordmark-compact" : ""} ${className}`.trim()}
      role="img"
    >
      <span aria-hidden="true" className="mokaair-wordmark-moka">Moka</span>
      <span aria-hidden="true" className="mokaair-wordmark-air">air</span>
    </span>
  );
}
