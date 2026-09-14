const mode=process.argv[2];
if(mode==='exit'){console.error('Injected exit');process.exit(7);}
if(mode==='invalid'){process.stdout.write('not MCP JSON\n');}
if(!['exit','invalid','hang'].includes(mode)){console.error('Modes: exit, invalid, hang');process.exit(2);}
process.stdin.resume();
