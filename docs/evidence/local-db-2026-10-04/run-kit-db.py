import base64, hashlib, hmac, json, os, pathlib, subprocess, time, sys
D='/usr/local/bin/docker'
evidence=pathlib.Path(__file__).parent
if len(sys.argv)!=4: raise SystemExit('Usage: run-kit-db.py label image disposable-checkout')
repo=pathlib.Path(sys.argv[3]).resolve()
inside=subprocess.run(['git','-C',str(evidence),'rev-parse','--is-inside-work-tree'],capture_output=True,text=True)
if inside.returncode==0: raise SystemExit('STOP: copy reproducer to a private directory outside Git')
label=sys.argv[1] if len(sys.argv)>1 else 'before'
image=sys.argv[2] if len(sys.argv)>2 else 'node:20.20.0-bookworm-slim'
network='sushii-backlog-kit-db-20261004'
pg='sushii-backlog-kit-pg-20261004'; rest='sushii-backlog-kit-rest-20261004'; runner='sushii-backlog-kit-test-20261004'
def run(args, **kw): return subprocess.run([D,*args],capture_output=True,text=True,timeout=kw.pop('timeout',60),**kw)
def require(args,**kw):
 r=run(args,**kw)
 if r.returncode: raise RuntimeError('Docker operation failed: '+args[0])
 return r
limits=['--cpus=0.5','--memory=512m','--memory-swap=512m','--pids-limit=128','--log-driver=local','--log-opt=max-size=5m','--log-opt=max-file=2']
secret=base64.urlsafe_b64encode(os.urandom(32)).decode()
def enc(x): return base64.urlsafe_b64encode(json.dumps(x,separators=(',',':')).encode()).rstrip(b'=')
body=enc({'alg':'HS256','typ':'JWT'})+b'.'+enc({'role':'service_role','exp':int(time.time())+900})
token=(body+b'.'+base64.urlsafe_b64encode(hmac.new(secret.encode(),body,hashlib.sha256).digest()).rstrip(b'=')).decode()
env_files=[]
def envfile(name, values):
 p=evidence/name; p.write_text('\n'.join(k+'='+v for k,v in values.items())+'\n');p.chmod(0o600);env_files.append(p);return str(p)
for name in [runner,rest,pg]:
 if run(['inspect',name]).returncode==0: raise SystemExit('STOP: reserved container namespace already exists')
if run(['network','inspect',network]).returncode==0: raise SystemExit('STOP: reserved network namespace already exists')
result={ 'scope':'disposable compatibility kit storage contract; not production RLS/cutover', 'source':subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),'network_internal':True,'host_ports':False,'database_tmpfs':True}
try:
 require(['network','create','--internal',network])
 pgenv=envfile('kit-pg-private.env',{'POSTGRES_PASSWORD':'synthetic-local-test-only'})
 require(['run','-d','--rm','--name',pg,'--network',network,*limits,'--env-file',pgenv,'--tmpfs','/var/lib/postgresql/data:rw,nosuid,size=256m','postgres:16.15-alpine'])
 for i in range(30):
  if run(['exec',pg,'pg_isready','-U','postgres']).returncode==0: break
  time.sleep(1)
 else: raise RuntimeError('disposable postgres did not become ready')
 migration=(repo/'supabase/migrations/0001_decks.sql').read_text()
 sql='CREATE ROLE service_role NOLOGIN BYPASSRLS;\n'+migration
 require(['exec','-i',pg,'psql','-U','postgres','-v','ON_ERROR_STOP=1'],input=sql)
 restenv=envfile('kit-rest-private.env',{'PGRST_DB_URI':'postgres://postgres:synthetic-local-test-only@'+pg+':5432/postgres','PGRST_DB_SCHEMAS':'public','PGRST_DB_ANON_ROLE':'service_role','PGRST_JWT_SECRET':secret,'PGRST_LOG_LEVEL':'crit'})
 require(['run','-d','--rm','--name',rest,'--network',network,*limits,'--env-file',restenv,'postgrest/postgrest:v12.2.3'])
 testenv=envfile('kit-test-private.env',{'SUSHI_TEST_SUPABASE_URL':'http://127.0.0.1:18081','SUSHI_TEST_SUPABASE_KEY':token})
 time.sleep(2)
 r=run(['run','--rm','--name',runner,'--network',network,'--cpus=1','--memory=1536m','--memory-swap=1536m','--pids-limit=256','--log-driver=local','--log-opt=max-size=5m','--log-opt=max-file=2','--env-file',testenv,'-v',str(repo)+':/work','-v',str(evidence/'kit-rest-gateway.mjs')+':/kit-rest-gateway.mjs:ro','-w','/work',image,'timeout','300','node','/kit-rest-gateway.mjs',rest],timeout=330)
 (evidence/('compat-kit-db-'+label+'.log')).write_text(r.stdout+r.stderr)
 result['test_exit_code']=r.returncode
 print('KIT DB TEST EXIT',r.returncode)
except Exception as exc:
 result['setup_error']=str(exc)
 print('STOP',str(exc))
finally:
 result['cleanup']={}
 for name in [runner,rest,pg]: result['cleanup'][name]=run(['rm','-f',name]).returncode
 result['cleanup']['network_remove']=run(['network','rm',network]).returncode
 for p in env_files: p.unlink(missing_ok=True)
 result['synthetic_credentials_removed']=True
 (evidence/('compat-kit-db-'+label+'-receipt.json')).write_text(json.dumps(result,indent=2))

raise SystemExit(result.get('test_exit_code',2))
