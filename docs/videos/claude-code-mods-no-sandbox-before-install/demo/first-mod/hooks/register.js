// Teaching implementation based on the public Claude Code Mod API.
// Not validated or run in the local Claude runtime. See ../../README.md.
// The count records observed calls, including calls that may later fail.
let calls = 0;

export function register(on) {
  on("session.start", async ($, event, next) => {
    await $.command.register({
      name: "tally",
      description: "Show the number of tool-call events since this mod loaded",
    });
    return next(event);
  });

  on("tool.call", async ($, event, next) => {
    calls += 1;
    $.ui.invalidate("ui.render");
    return next(event);
  });

  on("command.run", { command: "tally" }, async () => ({
    text: `Tool calls since load: ${calls}`,
  }));

  on("ui.render", { component: "Spinner" }, async ($, event, next) =>
    next({
      ...event,
      props: { ...event.props, suffix: ` · tool calls: ${calls}…` },
    }),
  );
}
