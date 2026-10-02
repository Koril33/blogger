"""Bounded, local checks of disputed claims; does not execute article programs."""
from pathlib import Path
import ast,copy,io,json,logging,logging.handlers,sqlite3,sys,tempfile,queue
from concurrent.futures import Future
from urllib.parse import parse_qs,urlsplit
from http.client import HTTPResponse
HERE=Path(__file__).parent
results=[]
def check(name,expected,actual):
    ok=actual==expected
    results.append(dict(name=name,expected=expected,actual=actual,passed=ok))
    if not ok: raise AssertionError(name)
c=sqlite3.connect(':memory:')
c.execute('CREATE TABLE pk (k TEXT PRIMARY KEY)')
c.execute('INSERT INTO pk VALUES (NULL)');c.execute('INSERT INTO pk VALUES (NULL)')
check('SQLite普通TEXT主键允许多个NULL',2,c.execute('SELECT COUNT(*) FROM pk').fetchone()[0])
c.execute('CREATE TABLE ai (id INTEGER PRIMARY KEY AUTOINCREMENT)')
check('sqlite_sequence建表时无对应行',[],c.execute('SELECT * FROM sqlite_sequence').fetchall())
c.execute('INSERT INTO ai DEFAULT VALUES')
check('首次插入后产生sequence行',[('ai',1)],c.execute('SELECT * FROM sqlite_sequence').fetchall())
c.execute('CREATE TABLE txt (v TEXT)');c.execute('INSERT INTO txt VALUES (123)')
check('TEXT亲和性把整数转为文本',('123','text'),c.execute('SELECT v,typeof(v) FROM txt').fetchone())
c.close()
root=logging.getLogger();root.handlers.clear();root.filters.clear();root.setLevel(logging.DEBUG)
stream=io.StringIO();handler=logging.StreamHandler(stream);root.addHandler(handler)
class Reject(logging.Filter):
    def filter(self,record): return False
root.addFilter(Reject());logging.getLogger('audit.child').warning('child record');root.warning('root record')
check('祖先Logger过滤器不处理子Logger传播记录','child record\n',stream.getvalue())
check('Handler默认级别NOTSET',logging.NOTSET,handler.level)
root.filters.clear();root.handlers.clear();handler.close()
qh=logging.handlers.QueueHandler(queue.Queue())
try: raise ValueError('sample')
except ValueError:
    record=logging.LogRecord('probe',logging.ERROR,__file__,1,'message %s',('arg',),sys.exc_info())
    check('浅复制保留exc_info',True,copy.copy(record).exc_info is record.exc_info)
    prepared=qh.prepare(record)
    check('QueueHandler.prepare清除exc_info',None,prepared.exc_info)
    check('QueueHandler.prepare已格式化消息和回溯',True,'message arg' in prepared.msg and 'ValueError: sample' in prepared.msg)
try: json.loads(json.dumps({'message':'abcdefgh'})[:10]); invalid=False
except json.JSONDecodeError: invalid=True
check('硬切序列化JSON会产生非法JSON',True,invalid)
with tempfile.TemporaryDirectory(prefix='audit-probe-',dir=HERE) as tmp:
    p=Path(tmp)/'utf8.log'
    logging.basicConfig(filename=p,encoding='utf-8',level=logging.INFO,force=True)
    logging.info('中文日志');logging.shutdown();root.handlers.clear()
    check('basicConfig支持encoding',True,'中文日志' in p.read_text(encoding='utf8'))
    package=Path(tmp)/'audit_package';package.mkdir();(package/'__init__.py').write_text('visible = 42\n_hidden = 9\n',encoding='utf8')
    sys.path.insert(0,tmp)
    ns={};exec('from audit_package import *',ns)
    check('没有__all__的包仍可star导入公开名称',42,ns['visible'])
    sys.path.pop(0);sys.modules.pop('audit_package',None)
f=Future();f.set_exception(ValueError('failed task'))
check('任务失败的Future也标记done',True,f.done())
try: f.result(); failed=False
except ValueError: failed=True
check('必须检查Future结果才能区分处理成功',True,failed)
try: ast.parse('import sys from pprint import pprint'); syntax=False
except SyntaxError: syntax=True
check('134篇import语句无法解析',True,syntax)
try:
    args=['update.exe','app.exe','v1','url','v2']
    if len(args)<5: bad=False
    else:
        _,app_path,current_version,exe_url,new_version,description,update_date=args
        bad=False
except ValueError: bad=True
check('更新器错误的参数个数检查放过5元素然后解包失败',True,bad)
check('未编码搜索词中的&改变参数',{'q':['a'],'b':['c']},parse_qs(urlsplit('https://example.com/search?q=a&b=c').query))
class FakeSocket:
    def makefile(self,*args): return io.BytesIO(b'HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\nabc')
response=HTTPResponse(FakeSocket());response.begin()
check('指定分块大小的HTTPResponse.read可能在声明长度前返回EOF',[b'abc',b''],[response.read(8192),response.read(8192)])
try:
    import requests
    status_results=[]
    for code in (200,301,304,400,404,500):
        r=requests.Response();r.status_code=code;r.url='https://example.invalid/';r.reason='probe'
        try:r.raise_for_status();raises=False
        except requests.HTTPError:raises=True
        status_results.append((code,raises))
    check('raise_for_status仅拒绝4xx/5xx',[(200,False),(301,False),(304,False),(400,True),(404,True),(500,True)],status_results)
except ImportError:
    results.append(dict(name='Requests行为检查',skipped='环境未安装requests'))
(HERE/'probe-results.json').write_text(json.dumps(dict(python=sys.version,sqlite=sqlite3.sqlite_version,results=results),ensure_ascii=False,indent=2,default=repr),encoding='utf8')
print(json.dumps(dict(passed=sum(x.get('passed',False) for x in results),skipped=sum('skipped' in x for x in results)),ensure_ascii=False))
