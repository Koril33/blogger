from pathlib import Path
import json,re
HERE=Path(__file__).parent
ROOT=Path('C:/Project/blog')
FILES=sorted(ROOT.rglob('*.md'),key=lambda p:str(p.relative_to(ROOT)).casefold())
findings=json.loads((HERE/'reviewed-draft.json').read_text(encoding='utf8'))
withdrawn={
70:'SQLite CLI接受.headers的无歧义前缀缩写，.header并非无效命令；完整拼法可以统一，但不应列作错误。',
98:'原教程展示的修改命令已有--permanent并要求reload，不能将其读成所有运行时命令都不生效。',
105:'SHA-512的速度取决于实现和硬件；原候选缺少直接对照数据，不列作确认的事实错误。',
155:'原文明确是特定静态BusyBox成功恢复的个人经历，并已列静态编译前提；没有声称实现完整rpm语义。'}
overrides={91:206,99:99,100:86,115:9,116:36,144:4,159:80,217:23,226:146,242:109,251:147,254:99,270:596}
source_map={
'https://www.mca.gov.cn/n156/n189/c1618736/content.html':'https://www.npc.gov.cn/c2/c30834/201905/t20190521_281393.html',
'https://uefi.org/specs/UEFI/2.10/13_Protocols_Media_Access.html':'https://tldp.org/HOWTO/html_single/Large-Disk-HOWTO/',
'https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/100581-duplex.html':'https://www.cisco.com/en/US/docs/internetworking/troubleshooting/guide/tr1904.html',
'https://man7.org/linux/man-pages/man3/time.3type.html':'https://man7.org/linux/man-pages/man3/time_t.3type.html',
'https://docs.gunicorn.org/en/stable/design.html':'https://github.com/benoitc/gunicorn/blob/23.0.0/docs/source/design.rst',
'https://docs.gunicorn.org/en/stable/design.html#how-many-workers':'https://github.com/benoitc/gunicorn/blob/23.0.0/docs/source/design.rst',
'https://docs.gunicorn.org/en/stable/index.html':'https://github.com/benoitc/gunicorn/blob/master/README.rst',
'https://openjdk.org/jeps/254':'https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java',
'https://openjdk.org/jeps/400':'https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/charset/Charset.html',
'https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html':'https://man7.org/linux/man-pages/man5/systemd.service.5.html',
'https://docs.python.org/3/library/reference/compound_stmts.html#the-with-statement':'https://docs.python.org/3/reference/compound_stmts.html#the-with-statement',
'https://docs.python.org/3/library/tutorial/modules.html#importing-from-a-package':'https://docs.python.org/3/tutorial/modules.html#importing-from-a-package',
'https://jakarta.ee/specifications/persistence/3.1/jakarta-persistence-spec-3.1.pdf':'https://jakarta.ee/specifications/persistence/3.1/',
'https://www.pi4j.com/1.2/pins/model-4b-rev1.html':'https://www.pi4j.com/1.2/apidocs/src-html/com/pi4j/io/gpio/RaspiPin.html',
}
def change(i,**kwargs):
    next(x for x in findings if x['draft_id']==i).update(kwargs)
change(2,type='版本信息补充',problem='支持MQTT 3.1的陈述本身没有错，但本文介绍Mosquitto协议支持范围时漏掉3.1.1及5.0；应与使用版本一致。')
change(38,type='版本条件',problem='四种GenerationType符合旧版javax.persistence/JPA；Jakarta Persistence 3.1新增UUID。应注明本文实际API版本，不能将新旧版本混为一谈。')
change(274,type='标准更新建议',problem='可以制定项目组合规则，本句不是语言层面的事实错误；如果希望对齐现行NIST指南，应更新策略：该指南不要求字符类别组合，单因素密码最低15字符，多因素可最低8字符。')
change(42,type='模型条件澄清',problem='三级树可作为教学简化模型，但不是中国全部行政区划的统一结构；直辖市、省直辖县级单位等有例外。')
change(56,type='业务模型条件',problem='当前用户/商品资料与历史交易快照是不同的数据语义。只有希望订单引用当前属性时才应随主数据更新，不能笼统要求更新历史订单成交价。',suggestion='注明本文只是演示关联当前实体信息；历史订单通常保存成交价、下单联系方式等快照，应按业务语义决定，不应自动批量改写。')
change(75,type='概念/适用条件',problem='集合图可以作有限教学类比，但不能表达SQL连接的行配对和重复语义；用UNION去重也不能通用模拟FULL JOIN。')
change(92,suggestion='290～292行表格应给出现代UTF-8合法首字节范围C2～DF、E0～EF、F0～F4，并补E0/ED/F0/F4后续字节限制；现表C0～DF、F0～F7会包含非法编码。')
change(95,type='算法适用条件',line=61,suggestion='说明插值需要两个已知的逻辑状态，常见做法是渲染落后一个逻辑步；若按图在16ms时预测33ms未来位置，应称外推并说明预测前提。61行“一上面的”改“以上面的”。')
change(99,quote='?、L、W、#的语法表',suggestion='将Linux五时间字段与Quartz六/七字段分开；Linux章节保留逗号、范围、星号和步长语法，Quartz专用符号另起小节。Linux星期通常支持0和7都表示周日；Quartz星期编号不同。')
change(100,quote='0 0 1 1 ?及其后的例子',problem='86～89行是五字段示例，但使用了Linux crontab不支持的?；99行另夹入六时间字段的Quartz示例。',suggestion='Linux例子改为0 0 1 1 *、59 6 15 5 *、30 15 * 9 0、30 19 * 12 6；99行的六时间字段示例移到Quartz小节。')
change(125,suggestion='交换110/114行位数：扇区6位，磁头8位；柱面编号0～1023对应1024个柱面。理论256磁头时容量512×63×1024×256=8,455,716,864字节；采用255头兼容几何时也必须用1024柱面，明确是哪一种限制。')
change(142,type='命令适用条件',suggestion='说明--nodeps只跳过依赖检查，不解决依赖。采用本地yum事务或按官方迁移流程安装MySQL兼容库，并检查最终依赖完整性。')
change(173,sources=['https://www.cisco.com/en/US/docs/internetworking/troubleshooting/guide/tr1904.html'])
change(188,type='实现/标准条件',suggestion='说明这些范围以CHAR_BIT=8、二补码有符号表示为前提。plain char、signed char、unsigned char是三个不同类型；plain char的符号性由实现决定。引用旧标准时保留其允许的表示差异。')
change(206,type='适用条件',suggestion='固定无夏令时偏移下、两端均为当天零点时可得到示例结果；任意systemDefault时区并不保证。日期差优先ChronoUnit.DAYS.between(LocalDate,LocalDate)或toEpochDay差值；区分日期差和持续时间。')
change(232,quote='及其耗时费心',problem='这里“及其”应为程度副词“极其”。',suggestion='21行改为“极其耗时费心”。')
change(265,type='用法边界澄清',problem='“与Python切片相似”可作为类比，但没有说明end包含这一关键差别；容易导致实际分页多取一项。')
change(297,suggestion='改为格式化/美化SQL，不等于字段化结构化日志。115行BasicBinder适用于Hibernate5；Hibernate6通常使用logging.level.org.hibernate.orm.jdbc.bind=TRACE，注明版本。')
change(50,sources=['https://xlinux.nist.gov/dads/HTML/binarytree.html','https://xlinux.nist.gov/dads/HTML/btree.html'])
for x in findings:
    if x['draft_id'] in overrides:x['line']=overrides[x['draft_id']]
    x['sources']=list(dict.fromkeys(source_map.get(u,u) for u in x['sources']))
findings=[x for x in findings if x['draft_id'] not in withdrawn]
def add(a,l,t,q,p,s,*urls):findings.append(dict(article=a,line=l,type=t,quote=q,problem=p,suggestion=s,sources=list(urls),draft_id=None))
add(65,174,'配置错误','root_url包含Grafana内部端口','示例公开地址是http://example.com/monitor/，但root_url使用内部http_port（通常3000），且未展示domain设置，可能生成错误链接和跳转。','直接设置root_url=http://example.com/monitor/，或正确配置公开domain/协议/端口；HTTPS终止时按公开HTTPS URL设置。','https://grafana.com/tutorials/run-grafana-behind-a-proxy/')
add(65,335,'代码错误','f.write(b"\\0" * target_disk)','先在内存中分配相当于目标磁盘大小的字节串，可能在写盘之前就MemoryError；目标文件大小也没有扣除已用磁盘空间。','分块写入固定大小缓冲区，按已用/可用空间计算需要增加的量，并用try/finally清理测试文件。','https://docs.python.org/3/library/stdtypes.html#bytes','https://docs.python.org/3/library/shutil.html#shutil.disk_usage')
add(77,510,'字词/条件遗漏','/etc/groups；newgrp必须是既有组成员','组数据库路径为/etc/group；某些实现允许非成员凭组密码切换，不能无条件说必须已是成员。','路径统一改/etc/group；newgrp说明成员/组密码及权限条件；新建文件属组还可能受父目录setgid位影响。','https://man7.org/linux/man-pages/man1/newgrp.1.html','https://man7.org/linux/man-pages/man5/group.5.html')
add(94,626,'配置错误','ExecReload通过SIGHUP重载Redis','本教程Redis5忽略SIGHUP，此ExecReload不会按预期重读redis.conf。','去掉该无效重载定义，按CONFIG SET支持的参数动态修改并按需CONFIG REWRITE；需重启的设置明确重启。','https://raw.githubusercontent.com/redis/redis/5.0/src/server.c','https://redis.io/docs/latest/commands/config-set/')
add(105,219,'配置复制错误','三个站点的try_files都指向第一份报告','foo和bar的HTML入口仍读取report-djhx.site.html，与各自ExecStart生成的报告名不一致。','219行改/report-foo.djhx.site.html；233行改/report-bar.djhx.site.html；逐一对应生成路径与HTML入口。','https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files')
add(118,19,'字词/版本条件','文档系统；Path.of','文件系统不应写成文档系统；Path.of实际从Java11引入，接口从Java8支持静态方法不等于该API在Java8已存在。','19、21行等文档系统/文档按语境改文件系统/文件；兼容性段明确Path.of要求Java11及以上。','https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Path.html#of(java.lang.String,java.lang.String...)')
add(134,37,'代码错误','import sys from pprint import pprint','两条import语句误拼成一行，无法通过Python语法解析。','拆为import sys和from pprint import pprint两行。','https://docs.python.org/3/reference/simple_stmts.html#the-import-statement')
add(143,49,'链接错误','URL目标混入中文或单引号','49行URL后含中文正文；164、168行链接目标末尾把引号带入了路径。','49行目标只保留https://korilweb.cn；164、168行从URL目标中移除末尾单引号，将正文引号放在链接外。')
add(149,426,'代码错误','len(sys.argv)<5却解包7个元素','传5或6个参数元素会通过检查，然后在432行解包时ValueError；用法提示也漏description和update_date。','检查len(sys.argv)==7，补完整用法：update.exe <app_path> <current_version> <exe_url> <new_version> <description> <update_date>；完整版重复代码同步修改。','https://docs.python.org/3/library/sys.html#sys.argv')
add(148,49,'命令错误','net user koril 123456 /active','/active选项需要yes或no值；原示例没有给出值。','激活账户写net user koril /active:yes；创建账户的命令与激活命令分开说明。','https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user')
add(153,98,'链接错误','本地演示URL包含中文正文','98、183行Markdown链接目标混入“可以看到以下页面”等中文。','分别只保留http://localhost:8080/static-demo/、http://localhost:8080/hello-servlet/hello。')
add(170,54,'链接错误','豆瓣和路径参数示例URL含中文','54、129行把链接后的解释句写入目标URL。','54行目标只保留https://movie.douban.com/top250?start=125&filter=；129行只保留http://myblog/post/123。')
add(174,78,'异常类型错误','把Timeout画成ConnectTimeout的子类','ConnectTimeout同时继承ConnectionError和Timeout，Timeout并非ConnectTimeout的子类；JSONDecodeError也存在兼容JSON异常的多继承。','将树图改为带多父类标注的关系图，或列类与直接父类表；至少更正78行的继承方向。','https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/')
add(175,57,'术语条件澄清','孤独症蔓延在社交网络之中','孤独症通常指自闭症谱系障碍，不是孤独感的同义词；此处若意指社交环境中的孤独情绪，用词会误导。','如意指loneliness，改为孤独感；如果确实讨论自闭症谱系障碍，应单独提供其流行病学证据，不能从社会感受推定。','https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders')
findings.sort(key=lambda x:(x['article'],x['line'],x['quote']))
for n,x in enumerate(findings,1):
    x['id']=f'R{n:03d}'
    x['path']=str(FILES[x['article']-1].relative_to(ROOT)).replace('\\','/')
    lines=FILES[x['article']-1].read_text(encoding='utf8').splitlines()
    assert 1<=x['line']<=len(lines),(x['id'],x['line'])
    x['actual_line']=lines[x['line']-1]
    x['category']='条件/版本澄清' if any(v in x['type'] for v in ('条件','边界','版本信息','标准更新')) or x['type'].startswith('适用') else '字词/链接' if any(v in x['type'] for v in ('字词','链接')) and not any(v in x['type'] for v in ('事实','对象','概念','代码','实现')) else '事实/技术错误'
    x['priority']='P3' if x['category']=='字词/链接' else 'P2'
    if x['article'] in (5,11,16,26,27,35,44,65,94,128,140,143,149,150,151,156) and ('代码' in x['type'] or '配置' in x['type'] or x['draft_id'] in (3,12,25,45,47,60,61,76,213,245,257,273)):
        x['priority']='P1'
(HERE/'findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding='utf8')
(HERE/'withdrawn.json').write_text(json.dumps(withdrawn,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(findings=len(findings),articles=len(set(x['article'] for x in findings)),categories={k:sum(x['category']==k for x in findings) for k in ('事实/技术错误','条件/版本澄清','字词/链接')}),ensure_ascii=False))
