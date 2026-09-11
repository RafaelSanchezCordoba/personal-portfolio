from pathlib import Path
from html import escape as e
import re
ROOT=Path(__file__).resolve().parent
P=ROOT.parent/'assets'; I=ROOT/'icons'
INK='#172B4D';MUT='#526581';LINE='#74859B';BLUE='#2563EB';BG='#FFFFFF';PURPLE='#7C3AED'
def tx(x,y,s,size=17,fill=INK,weight=400,anchor='start',mono=False):
 return f'<text x="{x}" y="{y}" font-family="{("ui-monospace, SFMono-Regular, Consolas, monospace" if mono else "Arial, Helvetica, sans-serif")}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{e(s)}</text>'
def rect(x,y,w,h,fill='white',stroke='#CBD5E1',r=0,dash=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def path(d,color=LINE,end=None,dash='',start=None,width=1.8):
 return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'+(f' marker-end="url(#{end})"' if end else '')+(f' marker-start="url(#{start})"' if start else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def label(x,y,s):return tx(x,y,s,15,MUT,anchor='middle')
def icon(name,x,y,color='#172B4D',size=52):
 svg=(I/(name+'.svg')).read_text();d=re.search(r'<path d="([^"]+)"',svg).group(1)
 return f'<g transform="translate({x} {y}) scale({size/24})"><path d="{d}" fill="{color}"/></g>'
def service(name,x,y,title,sub,color=INK):return icon(name,x-26,y,color)+tx(x,y+80,title,20,INK,700,'middle')+tx(x,y+105,sub,15,MUT,anchor='middle')
def title(k,t,sub):return tx(40,35,k,13,BLUE,700)+tx(40,73,t,29,INK,700)+tx(40,103,sub,17,MUT)
def save(name,title_,desc,body,w,h):
 defs='<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#74859B"/></marker><marker id="one" viewBox="0 0 20 20" refX="19" refY="10" markerWidth="16" markerHeight="16" orient="auto-start-reverse"><path d="M4 2 V18 M10 2 V18" fill="none" stroke="#74859B" stroke-width="1.4"/></marker><marker id="many" viewBox="0 0 30 20" refX="29" refY="10" markerWidth="24" markerHeight="16" orient="auto-start-reverse"><path d="M29 2 L15 10 L29 18" fill="none" stroke="#74859B" stroke-width="1.4"/><circle cx="6" cy="10" r="4" fill="white" stroke="#74859B" stroke-width="1.4"/></marker></defs>'
 P.joinpath(name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{e(title_)}</title><desc id="desc">{e(desc)}</desc>{defs}<rect width="100%" height="100%" fill="white"/>{body}</svg>')
# Deployment / container view: branded service nodes and explicit boundaries.
b=title('ARCHITECTURE / SERVICE VIEW','Maitecrafts · application and managed services','Deployment model documented in the repository. Arrows show requests or data flow.')
b+=rect(315,150,510,490,'#F8FAFC','#94A3B8',0,'7 5')+icon('vercel',335,167,size=23)+tx(372,187,'VERCEL · APPLICATION',15,INK,700)
b+=rect(865,150,375,250,'#F7FCFC','#94A3B8',0,'7 5')+tx(887,182,'NEON · MANAGED DATABASE',15,INK,700)
b+=service('react',125,230,'Workshop browser','React · TanStack Query','#149ECA')
b+=service('nextdotjs',480,230,'Next.js','UI + Server Actions')+service('prisma',725,230,'Prisma','Database access','#2D3748')
b+=service('postgresql',1052,230,'PostgreSQL','Orders · configuration · history','#336791')
b+=path('M170 260 H432',end='arrow')+label(300,242,'HTTPS · poll every 4s')
b+=path('M525 260 H675',end='arrow')+label(603,242,'Queries')
b+=path('M765 260 H1004',end='arrow')+label(898,242,'PostgreSQL connection')
b+=service('google',125,465,'Google','OAuth sign-in','#4285F4')
b+=service('vercel',715,475,'Vercel Blob','Product and design photos')
# Object storage pictogram alongside the brand.

b+=path('M455 355 V495 H183',end='arrow')+label(301,480,'Auth.js · OAuth')
b+=path('M505 355 V447 H715 V468',end='arrow')+label(626,432,'Authenticated upload')
b+=service('woocommerce',125,735,'WooCommerce','Online shop','#96588A')
b+=path('M175 760 H265 V585 H455 V350',end='arrow')+label(323,571,'Webhook · HMAC-SHA256')
b+=rect(353,666,456,182,'#FAFAFF','#C4B5FD',0,'7 5')+tx(374,695,'NOTIFICATION INTEGRATION',14,PURPLE,700)
b+=tx(481,738,'Notification rules',19,INK,700,'middle')+tx(481,764,'Server-side evaluation',15,MUT,anchor='middle')
b+=tx(711,738,'CallMeBot',19,INK,700,'middle')+tx(711,764,'Provider adapter',15,MUT,anchor='middle')
b+=path('M480 355 V663',dash='5 4',end='arrow')+label(568,621,'After saving changes')
b+=path('M565 745 H637',end='arrow')
b+=service('whatsapp',1052,708,'WhatsApp','Workshop notifications','#159B52')+path('M778 744 H1002',end='arrow')+label(891,724,'HTTPS request')
b+=tx(40,922,'Scope: application services, not a network topology. Blob requires storage configuration; local uploads have a filesystem fallback.',15,MUT)
b+=tx(40,949,'Brand icons identify technologies. Generic boundaries indicate hosting and integration responsibilities.',15,MUT)
save('architecture.svg','Maitecrafts service architecture','Service diagram with React browser, a Vercel Next.js application and Prisma, Neon PostgreSQL, Google OAuth, Vercel Blob, WooCommerce and CallMeBot WhatsApp notifications.',b,1280,980)
# Crow's foot ERD. Selected real Prisma columns, no fictional foreign keys.
b=title('DATABASE / ENTITY–RELATIONSHIP DIAGRAM','Production domain · PostgreSQL','Selected columns from the Prisma schema. Crow’s-foot notation; authentication tables omitted.')
def table(x,y,name,rows,w=300):
 h=44+len(rows)*30
 s=rect(x,y,w,h,'white','#9AAABD')+rect(x,y,w,44,'#EAF0F8','#9AAABD')+tx(x+14,y+29,name,19,INK,700,mono=True)
 for n,(key,col,typ) in enumerate(rows):
  yy=y+44+n*30
  if n:s+=path(f'M{x} {yy} H{x+w}',color='#E2E8F0',width=1)
  s+=tx(x+12,yy+21,key,12,BLUE,700,mono=True)+tx(x+51,yy+21,col,14,INK,mono=True)+tx(x+w-12,yy+21,typ,12,MUT,anchor='end',mono=True)
 return s
# connect behind tables using PK side → optional many side
b+=path('M340 310 H440',start='one',end='many')
b+=path('M600 544 V619',start='one',end='many')
b+=path('M940 295 H860 V327 H760',start='one',end='many')
b+=path('M940 641 H835 V444 H760',start='one',end='many')
b+=path('M190 464 V507 H390 V696 H440',start='one',end='many')
b+=path('M190 464 V568 H300 V815 H440',start='one',end='many')
b+=path('M340 760 H389 V897 H940',start='many',end='many')
# Entity positions
b+=table(40,150,'User',[('PK','id','String'),('UQ','email','String?'),('','name','String?'),('','role','Role')])
# User relationships routed separately top across to Order and bottom history (only show to history? order line need explicit)
b+=path('M190 314 V353',start='one',end='many')
b+=table(40,355,'Order',[('PK','id','String'),('UQ','serialNumber','String'),('FK','createdById','String'),('','data','Json'),('','dueDate','DateTime?'),('','deliveredAt','DateTime?')])
# correction Order to item at y430, not first earlier user->item line
# remove earlier horizontal line User → item (y310), use Order relation.
b=b.replace(path('M340 310 H440',start='one',end='many'),path('M340 430 H440',start='one',end='many'))
# clear incorrect starts from mid Order y464 routes and replace with real User relation to history via far left route
b=b.replace(path('M190 464 V507 H390 V696 H440',start='one',end='many'),'')
b=b.replace(path('M190 464 V568 H300 V815 H440',start='one',end='many'),path('M40 233 H20 V930 H420 V810 H440',start='one',end='many'))
b+=table(440,230,'OrderItem',[('PK','id','String'),('FK','orderId','String'),('FK','stageId','String'),('FK','productTypeId','String'),('FK','createdById','String'),('','quantity','Int'),('','design','String?'),('','data','Json'),('','designPhotoUrl','String?')],320)
b+=table(940,200,'ProductionStage',[('PK','id','String'),('UQ','key','String'),('UQ','order','Int'),('','label','String'),('','skipForPrintTypes','String[]'),('','archiveAfterHours','Int?')])
b+=table(940,545,'ProductType',[('PK','id','String'),('UQ','key','String'),('','label','String'),('','isActive','Boolean'),('','showQuantityOnKanban','Boolean')])
b+=table(40,660,'FieldDefinition',[('PK','id','String'),('UQ*','group + key',''),('','fieldType','FieldType'),('','required','Boolean'),('','options','Json?'),('','isActive','Boolean')])
b+=table(440,620,'OrderItemStatusHistory',[('PK','id','String'),('FK','orderItemId','String'),('FK','changedById','String'),('','fromStageId','String?'),('','toStageId','String'),('','changedAt','DateTime')],380)
# end N:M at ProductType bottom (y739)
b=b.replace(path('M340 760 H389 V897 H940',start='many',end='many'),path('M340 760 H389 V899 H1090 V739',start='many',end='many'))
b+=label(697,887,'Implicit Prisma join table · many-to-many')
b+=tx(40,997,'PK  Primary key       FK  Declared foreign key       UQ  Unique       UQ*  Composite unique constraint',15,MUT)
b+=tx(40,1028,'||—○<  One to zero-or-many. Historical stage IDs are stored strings, not declared stage foreign keys.',15,MUT)
b+=tx(40,1059,'FieldDefinition describes JSON values; there is no FK from a JSON key to its definition. Other relations are omitted.',15,MUT)
save('data-model.svg','Crow’s-foot ER diagram for Maitecrafts','Selected Prisma entities shown as database tables with primary keys, foreign keys, unique constraints and crow’s-foot relationships. Historical stage identifiers are not foreign keys.',b,1280,1095)
# UML sequence diagram, transaction frame and sync post-commit boundaries.
b=title('BEHAVIOUR / UML SEQUENCE DIAGRAM','Move a product to its next applicable stage','Normal success path for one item. Commit precedes notification checks and order timestamp updates.')
xs=[115,365,665,965,1220];names=['Browser','Server Action','PostgreSQL','Notification rules','CallMeBot']
for x,n in zip(xs,names):
 b+=rect(x-85,142,170,46,'#EEF3FA','#94A3B8')+tx(x,171,n,17,INK,700,'middle')+path(f'M{x} 188 V1070',dash='6 5',color='#94A3B8')
b+=rect(359,221,12,763,'#DDE8FC','#7C9EC9')+rect(659,414,12,217,'#DDE8FC','#7C9EC9')
def msg(a,c,y,s,dashed=False):return path(f'M{a} {y} H{c}',end='arrow',dash='5 4' if dashed else '')+label((a+c)/2,y-12,s)
b+=msg(115,359,226,'advance(itemId)')
b+=path('M371 267 H403 V301 H371',end='arrow')+tx(417,276,'requireUser()',16,INK)+tx(417,300,'Validate session',15,MUT)
b+=msg(371,665,347,'Read item + ordered stages')+msg(665,371,389,'Current state + stage configuration',True)
b+=rect(305,411,440,239,'none','#526581')+rect(305,411,115,30,'white','#526581')+tx(319,432,'transaction',14,INK,700)
b+=tx(432,443,'Target resolved from stage rules',13,MUT)
b+=msg(371,659,478,'UPDATE OrderItem.stageId')+msg(371,659,541,'INSERT status history')+msg(659,371,609,'COMMIT',True)
b+=msg(371,965,698,'checkStageNotifications(...)')
b+=msg(965,1220,753,'Matching rule: send')
b+=msg(1220,965,813,'Delivery result / caught error',True)
b+=msg(965,371,859,'Notification check finished',True)
b+=msg(371,665,921,'Synchronise order timestamps')+msg(665,371,964,'Updated order state',True)
b+=msg(359,115,1022,'Return + invalidate Kanban query',True)
b+=tx(40,1121,'A caught message-delivery error does not roll back the saved movement. Requests still await notification attempts.',16,MUT)
b+=tx(40,1152,'The transaction covers one item and its history. Group movements call the item logic repeatedly; they are not one batch transaction.',16,MUT)
save('state-change.svg','UML sequence diagram for changing a product stage','Lifelines for browser, server action, PostgreSQL, notification rules and CallMeBot. The item update and history insert share a transaction; notifications and order timestamps follow the commit.',b,1340,1190)
