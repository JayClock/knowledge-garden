import os, json, re, copy, subprocess, hashlib
from pathlib import Path
import xml.etree.ElementTree as E
os.environ['PYTHONIOENCODING']='utf-8'
base=Path('.pi/resume-refresh'); src=Path('.career/packages/general-projects-2-5/钟杰-通用简历.docx'); out=base/'resume.docx'
if not out.exists(): out.write_bytes(src.read_bytes())
w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; E.register_namespace('w',w); ns={'w':w}
root=E.parse(base/'document.xml'); boxes=root.findall('.//w:txbxContent',ns)
def call(*a):
 p=subprocess.run(['officecli',*map(str,a)],capture_output=True,encoding='utf-8');
 if p.returncode: raise RuntimeError(p.stdout+p.stderr)
 return p.stdout
def para(template,text,size=None,line=None):
 p=copy.deepcopy(template)
 for c in list(p):
  if c.tag!='{'+w+'}pPr':p.remove(c)
 r=E.SubElement(p,'{'+w+'}r'); rp=E.SubElement(r,'{'+w+'}rPr')
 old=template.find('w:r/w:rPr',ns)
 if old is not None:
  r.remove(rp);rp=copy.deepcopy(old);r.append(rp)
 if size:
  s=rp.find('w:sz',ns)
  if s is None:s=E.SubElement(rp,'{'+w+'}sz')
  s.set('{'+w+'}val',str(int(size*2)))
 if line:
  pp=p.find('w:pPr',ns)
  if pp is None: pp=E.Element('{'+w+'}pPr');p.insert(0,pp)
  sp=pp.find('w:spacing',ns)
  if sp is None:sp=E.SubElement(pp,'{'+w+'}spacing')
  sp.set('{'+w+'}line',str(int(line*20)));sp.set('{'+w+'}lineRule','exact')
 for j,t in enumerate(text.split('\n')):
  if j:E.SubElement(r,'{'+w+'}br')
  E.SubElement(r,'{'+w+'}t').text=t
 return p
def replace_box(index,paras):
 # DOM cannot resolve VML shape descendants; OfficeCLI raw-set is used for both branches.
 for n in (index,index+1):
  b=E.Element('{'+w+'}txbxContent');b.extend(copy.deepcopy(paras))
  call('raw-set',out,'/document','--xpath',f'(//w:txbxContent)[{n}]','--action','replace','--xml',E.tostring(b,encoding='unicode'))
md=Path('.career/packages/general-projects-2-5/resume.md').read_text(encoding='utf-8')
def clean(s):return s.replace('**','').replace('`','').strip()
projects=md.split('### ')[1:]
p=[]; template=list(boxes[0])
for section in projects[:2]:
 lines=[clean(re.sub(r'^\s*\*\s+','',x)) for x in section.strip().splitlines() if x.strip()]
 lines=[x for x in lines if x!='工作内容与成果：']
 p.append(para(template[0],lines[0],11,14))
 p.append(para(template[1],lines[1]+'\n'+lines[2],10,12))
 p.append(para(template[2],lines[3],10.5,14))
 for text in lines[4:]:
  q=para(template[3],text,10.5,14)
  # Paragraph template's first run is bold label; full replacement should be normal.
  for b in q.findall('w:r/w:rPr/w:b',ns): b.set('{'+w+'}val','0')
  p.append(q)
replace_box(1,p)
abilities=[
'5 年以上开发经验，以 React、TypeScript 为基本盘，具备全栈交付能力。',
'React Flow、Tiptap 复杂编辑器；DAG 调度、插件化节点与公式求值。',
'RESTful API、HATEOAS 资源与动作契约；SDK 请求去重、缓存及 React 适配。',
'Nx + pnpm 多包管理，GitHub Actions 检查、测试、构建及多阶段 Dockerfile。',
'跨框架监控 SDK：性能与异常采集、批量上报、失败重试及 Sourcemap 定位。',
'从业务约定澄清权责与履约流程，沉淀对象、关系、规则与 API 契约。',
'AI 研发 Harness：任务拆解、上下文组织、验证交接；参考实现与存量代码治理。',
'NestJS、PostgreSQL、Prisma 服务开发；Kafka 异步处理与 ClickHouse 存储查询。']
replace_box(13,[para(boxes[12][0],t,10.5,14) for t in abilities])
intro=md.split('## 个人概述\n')[1].split('## 核心能力')[0].strip().split('\n\n')
replace_box(25,[para(boxes[24][0],t,10.5,14) for t in intro])
replace_box(27,[para(boxes[26][0],'个人概述')])
call('save',out);call('close',out)
print('Built',out)
