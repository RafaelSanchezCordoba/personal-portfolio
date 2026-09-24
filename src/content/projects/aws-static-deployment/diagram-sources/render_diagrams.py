from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parent
P=ROOT.parent/'assets'
INK='#172B4D';MUT='#526581';LINE='#74859B';BLUE='#2563EB';GREEN='#15803D';RED='#B91C1C'
def tx(x,y,s,size=17,fill=INK,weight=400,anchor='start',mono=False):
 return f'<text x="{x}" y="{y}" font-family="{("ui-monospace, SFMono-Regular, Consolas, monospace" if mono else "Arial, Helvetica, sans-serif")}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{e(s)}</text>'
def rect(x,y,w,h,fill='white',stroke='#CBD5E1',r=0,dash=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def path(d,color=LINE,end=None,dash='',width=1.8):
 return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'+(f' marker-end="url(#{end})"' if end else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def label(x,y,s,fill=MUT,size=15,mono=False):return tx(x,y,s,size,fill,anchor='middle',mono=mono)
def title(k,t,sub):return tx(40,35,k,13,BLUE,700)+tx(40,73,t,29,INK,700)+tx(40,103,sub,17,MUT)
def zone(x,y,w,h,name,fill='#F8FAFC',stroke='#94A3B8',accent=INK):
 return rect(x,y,w,h,fill,stroke,0,'7 5')+tx(x+22,y+32,name,15,accent,700)
def node(x,y,w,name,sub=None,lines=(),accent=INK,stroke='#9AAABD',fill='white',dash='',nsize=19):
 h=26+(20 if name else 0)+(24 if sub else 0)+len(lines)*21
 s=rect(x,y,w,h,fill,stroke,0,dash);cy=y+34
 s+=tx(x+18,cy,name,nsize,accent,700)
 if sub:cy+=24;s+=tx(x+18,cy,sub,15,MUT)
 for ln in lines:cy+=21;s+=tx(x+18,cy,ln,13,INK,mono=True)
 return s,h
def save(name,title_,desc,body,w,h):
 defs='<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#74859B"/></marker><marker id="stop" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#B91C1C"/></marker></defs>'
 P.joinpath(name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{e(title_)}</title><desc id="desc">{e(desc)}</desc>{defs}<rect width="100%" height="100%" fill="white"/>{body}</svg>')
def foot(y,*rows):
 return ''.join(tx(40,y+i*28,r,15,MUT) for i,r in enumerate(rows))

# ---------------------------------------------------------------- architecture
b=title('ARCHITECTURE / SERVICE VIEW','Secure static site on AWS · build, delivery and DNS','Resources defined in infrastructure/*.tf. Arrows show requests or data flow.')
b+=zone(40,150,500,330,'GITHUB')
b+=node(68,198,220,'Developer','Local commit',('git push',))[0]
b+=node(312,198,220,'GitHub repository','personal-portfolio',('aws-deployment',))[0]
b+=path('M288 247 H304',end='arrow')
b+=node(68,340,464,'GitHub Actions · Deploy to AWS','ubuntu-latest · Node 22',('npm ci → npm run build → dist/',))[0]
b+=path('M420 296 V334',end='arrow')+tx(436,320,'push trigger',15,MUT)
b+=zone(760,150,500,330,'AWS ACCOUNT · IAM (GLOBAL)')
b+=node(788,198,444,'IAM OIDC provider','token.actions.githubusercontent.com',('aud: sts.amazonaws.com',))[0]
b+=node(788,340,444,'IAM role · github-actions-portfolio','Trust policy: aud + sub conditions',('s3:PutObject · s3:DeleteObject · s3:ListBucket','cloudfront:CreateInvalidation'))[0]
b+=path('M1010 296 V334',end='arrow')+tx(1026,320,'trusts',15,MUT)
b+=path('M532 380 H780',end='arrow')+label(656,368,'OIDC ID token')
b+=path('M780 416 H532',end='arrow',dash='5 4')+label(656,438,'Temporary credentials')
b+=zone(40,520,1220,310,'AWS ACCOUNT · CONTENT DELIVERY')
b+=zone(68,568,410,232,'REGION eu-north-1','#FBFDFF','#B6C4D6',MUT)
b+=node(96,610,354,'Amazon S3','personal-portfolio-aws-rsdev',('Public Access Block: all true','Bucket policy: CloudFront ARN only'))[0]
b+=node(520,610,290,'Amazon CloudFront','Distribution · global edge',('default_root_object: index.html','redirect-to-https · TLS 1.2_2021'))[0]
b+=zone(882,568,352,232,'REGION us-east-1','#FBFDFF','#B6C4D6',MUT)
b+=node(910,610,296,'ACM certificate','aws.rafasanchez.dev',('validation_method = DNS','Required here by CloudFront'))[0]
b+=path('M516 660 H458',end='arrow')+label(485,598,'OAC')
b+=path('M906 660 H818',end='arrow',dash='5 4')+label(846,598,'TLS cert')
b+=path('M300 450 V510')+path('M300 510 H690 V606',end='arrow')+path('M300 510 V606',end='arrow')
b+=tx(316,500,'aws s3 sync dist/ --delete',13,MUT,mono=True)
b+=tx(706,500,'aws cloudfront create-invalidation',13,MUT,mono=True)
b+=node(68,918,210,'Visitor','Browser request',('aws.rafasanchez.dev',))[0]
b+=zone(330,870,610,150,'CLOUDFLARE DNS')
b+=node(358,918,300,'CNAME aws','→ d3ay5auj3yddcp.cloudfront.net',nsize=18)[0]
b+=node(680,918,232,'ACM validation CNAME','→ acm-validations.aws',nsize=17)[0]
b+=path('M282 961 H350',end='arrow')+tx(326,900,'DNS lookup',15,MUT,anchor='end')
b+=path('M498 914 V770 H690 V726',end='arrow')+tx(700,862,'Resolves to the distribution',15,MUT)
b+=foot(1062,
 'S3 has no public endpoint: every Public Access Block setting is true and the bucket policy admits only the CloudFront distribution ARN.',
 'IAM and CloudFront are global. The bucket lives in eu-north-1; the certificate must be in us-east-1 to be usable by CloudFront.',
 'GitHub Actions stores no AWS access keys. It exchanges a short-lived OIDC token for temporary credentials scoped to this deployment.')
save('architecture.svg','Secure static site architecture on AWS','GitHub Actions builds the Astro site and authenticates to AWS through an IAM OIDC provider and role, then syncs to a private S3 bucket and invalidates a CloudFront distribution. CloudFront reads S3 through Origin Access Control, serves an ACM certificate from us-east-1, and is reached through a Cloudflare CNAME for aws.rafasanchez.dev.',b,1300,1160)

# ------------------------------------------------------------- deployment flow
b=title('CI/CD / DEPLOYMENT SEQUENCE','One push to aws-deployment','Steps and commands as written in .github/workflows/deploy-aws.yml.')
xs=[110,320,540,800,1030,1240];names=['Developer','GitHub','Actions runner','AWS STS','Amazon S3','CloudFront']
for x,n in zip(xs,names):
 b+=rect(x-85,142,170,46,'#EEF3FA','#94A3B8')+tx(x,171,n,17,INK,700,'middle')+path(f'M{x} 188 V1010',dash='6 5',color='#94A3B8')
b+=rect(534,296,12,660,'#DDE8FC','#7C9EC9')
def msg(a,c,y,s,dashed=False,mono=False):
 return path(f'M{a} {y} H{c}',end='arrow',dash='5 4' if dashed else '')+label((a+c)/2,y-12,s,mono=mono)
b+=msg(110,314,232,'git push origin aws-deployment',mono=True)
b+=msg(320,528,286,'on: push · branches: aws-deployment',mono=True)
b+=path('M552 318 H600 V352 H552',end='arrow')+tx(614,326,'actions/checkout@v4',15,INK,mono=True)+tx(614,350,'Checkout repository',14,MUT)
b+=msg(552,796,412,'OIDC ID token · aud sts.amazonaws.com')
b+=msg(796,552,462,'Temporary credentials for the role',True)
b+=rect(370,516,340,152,'none','#94A3B8',0,'7 5')+rect(370,516,148,30,'white','#94A3B8')+tx(384,537,'build on runner',14,INK,700)
b+=tx(392,582,'actions/setup-node@v4 (Node 22)',13,INK,mono=True)
b+=tx(392,610,'npm ci',13,INK,mono=True)
b+=tx(392,638,'npm run build → dist/',13,INK,mono=True)
b+=msg(552,1022,726,'aws s3 sync dist/ s3://$S3_BUCKET --delete',mono=True)
b+=msg(1022,552,782,'Objects uploaded · removed files deleted',True)
b+=msg(552,1232,856,'aws cloudfront create-invalidation --paths "/*"',mono=True)
b+=msg(1232,552,912,'Invalidation created',True)
b+=tx(40,1064,'Credentials are configured before the build step, exactly as ordered in the workflow file. They expire when the job ends.',15,MUT)
b+=tx(40,1092,'--delete removes objects that are no longer in dist/. The invalidation makes edge locations refetch on the next request.',15,MUT)
save('deployment-flow.svg','GitHub Actions deployment sequence','Sequence diagram: a push to the aws-deployment branch triggers the workflow, which checks out the repository, exchanges an OIDC token with AWS STS for temporary credentials, installs dependencies, builds the Astro site, syncs dist/ to S3 with --delete and creates a CloudFront invalidation.',b,1340,1130)

# ------------------------------------------------------------- security model
b=title('SECURITY / TRUST BOUNDARIES','What is trusted, and how far that trust reaches','Conditions and permissions as defined in infrastructure/iam.tf and infrastructure/s3.tf.')
b+=zone(40,150,470,300,'GITHUB · NO AWS CREDENTIALS STORED')
b+=node(68,198,414,'Deploy to AWS workflow','permissions: id-token: write',('No AWS keys in repository secrets',))[0]
b+=node(68,330,414,'Short-lived OIDC ID token','Issued per workflow run',('token.actions.githubusercontent.com',))[0]
b+=path('M275 296 V326',end='arrow')
b+=zone(760,150,500,300,'AWS · IDENTITY AND TRUST')
b+=node(788,198,444,'IAM OIDC provider','Validates issuer and token signature')[0]
b+=node(788,310,444,'Role trust policy',None,('StringEquals aud = sts.amazonaws.com','StringLike  sub = repo:RafaelSanchezCordoba','                   @53056368/personal-portfolio','                   @1362535609:*'))[0]
b+=path('M1010 282 V306',end='arrow')
b+=path('M486 380 H784',end='arrow')+label(635,368,'sts:AssumeRoleWithWebIdentity',mono=True,size=13)
b+=zone(40,490,1220,220,'AWS · LEAST-PRIVILEGE DEPLOY ROLE')
b+=node(68,540,380,'IAM role','github-actions-portfolio',('Temporary credentials','Expire with the job'))[0]
b+=node(490,540,360,'Allowed',None,('s3:ListBucket        bucket','s3:PutObject         bucket/*','s3:DeleteObject      bucket/*','cloudfront:CreateInvalidation'),accent=GREEN,stroke='#86B89A')[0]
b+=node(890,540,342,'Not granted',None,('No IAM or account actions','No other S3 buckets','No CloudFront config changes','No long-lived IAM user'),accent=RED,stroke='#E0B4B4',dash='5 4')[0]
b+=path('M452 620 H482',end='arrow')
b+=zone(40,760,1220,230,'AWS · CONTENT ACCESS')
b+=node(68,806,340,'Public internet','https://aws.rafasanchez.dev',('Reaches CloudFront only',))[0]
b+=node(490,806,360,'CloudFront distribution','ACM certificate · TLS 1.2_2021',('viewer_protocol_policy: https',))[0]
b+=node(930,806,302,'S3 bucket (private)','Public Access Block: all true',('Policy: AWS:SourceArn',))[0]
b+=path('M412 856 H482',end='arrow')+label(447,796,'HTTPS')
b+=path('M854 856 H922',end='arrow')+label(888,796,'OAC · SigV4')
b+=path('M238 910 V955 H1081 V910',color=RED,dash='6 5',end='stop')
b+=path('M648 945 L672 969 M672 945 L648 969',color=RED,width=2.4)
b+=label(660,935,'No public path from the internet to S3',RED)
b+=foot(1040,
 'The sub condition uses GitHub identifier form for owner and repository; the :* suffix matches any ref or environment in that repository.',
 'The bucket policy allows s3:GetObject to the CloudFront service principal only, conditioned on the distribution ARN.',
 'TLS terminates at CloudFront with the ACM certificate. Origin requests to S3 are signed with SigV4 through Origin Access Control.')
save('security-model.svg','Trust and security boundaries','GitHub stores no AWS keys and receives a short-lived OIDC token; AWS validates it against a trust policy with audience and subject conditions, grants a role limited to S3 object writes and CloudFront invalidation, and keeps the S3 bucket private behind CloudFront Origin Access Control.',b,1300,1130)
print('rendered:',*(p.name for p in sorted(P.glob('*.svg'))))
