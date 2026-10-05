import http from 'node:http';
import { spawn } from 'node:child_process';
const host = process.argv[2];
if (host !== 'sushii-backlog-kit-rest-20261004') throw new Error('unexpected disposable target');
const server = http.createServer((req, res) => {
  if (!req.url.startsWith('/rest/v1/')) { res.writeHead(404); res.end(); return; }
  const upstream = http.request({ hostname: host, port: 3000,
    path: req.url.slice('/rest/v1'.length), method: req.method,
    headers: { ...req.headers, host: `${host}:3000` } }, reply => {
    res.writeHead(reply.statusCode, reply.headers); reply.pipe(res);
  });
  upstream.on('error', () => { res.writeHead(503); res.end('{"message":"disposable REST unavailable"}'); });
  req.pipe(upstream);
});
await new Promise(resolve => server.listen(18081, '127.0.0.1', resolve));
const probe = await fetch('http://127.0.0.1:18081/rest/v1/decks', {
  headers: { Authorization: `Bearer ${process.env.SUSHI_TEST_SUPABASE_KEY}` },
});
if (probe.status !== 200) {
  console.error(`STOP: disposable REST preflight status ${probe.status}`);
  server.close(); process.exit(2);
}
const child = spawn('sh', ['-c', 'npm run typecheck && npm test -- --maxWorkers=1 --minWorkers=1'], { stdio: 'inherit' });
child.on('error', () => { server.close(); process.exit(2); });
child.on('exit', code => { server.close(); process.exit(code ?? 2); });
