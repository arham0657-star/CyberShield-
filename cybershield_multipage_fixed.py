
from flask import Flask, request, redirect, session, render_template_string
from datetime import datetime
from urllib.parse import urlparse
import re, html, os

app=Flask(__name__)
app.secret_key=os.environ.get("CYBERSHIELD_SECRET","cybershield-session-key")
PAGES=[("dashboard","Dashboard","⌂"),("scam","Scam Checker","✉"),("job","Job Offer Checker","▣"),("link","Link Safety","↗"),("email","Email Phishing","▤"),("password","Password Safety","▣"),("account","Account Security","◈"),("device","Device Safety","▣"),("wifi","Wi-Fi Security","⌁"),("privacy","Privacy Checkup","◉"),("history","Assessment History","▤"),("guide","Security Guide","?")]
CSS=r"""
*{box-sizing:border-box}body{margin:0;background:#f5faf6;color:#203b2c;font-family:Arial,sans-serif}:root{--g:#16834a;--d:#11663a;--p:#eaf7ef;--l:#dcebe1;--m:#6c8274}
.side{position:fixed;inset:0 auto 0 0;width:245px;background:white;border-right:1px solid var(--l);padding:18px 13px;overflow:auto;display:flex;flex-direction:column}
.brand{display:flex;gap:10px;align-items:center;padding:8px 8px 20px;border-bottom:1px solid #edf3ee;margin-bottom:14px;text-decoration:none}.brand h1{font-size:21px;color:var(--d);margin:0}.brand small{color:var(--m);font-size:10px;letter-spacing:1px}.logo{width:45px;height:45px}
.navlabel{font-size:10px;color:#91a397;font-weight:bold;letter-spacing:1.4px;padding:9px}nav a{display:flex;gap:12px;align-items:center;padding:11px 12px;margin:3px 0;border-radius:10px;color:#476252;text-decoration:none;font-size:13px;font-weight:bold}nav a:hover,nav a.active{background:var(--p);color:var(--d)}nav a.active{box-shadow:inset 3px 0 var(--g)}.ico{width:20px;color:var(--g);font-size:17px;text-align:center}.sidefoot{margin-top:auto;border-top:1px solid #edf3ee;padding:13px 8px;color:var(--m);font-size:11px;line-height:1.7}
.main{margin-left:245px;min-height:100vh}.top{height:68px;background:#fff;border-bottom:1px solid var(--l);display:flex;justify-content:space-between;align-items:center;padding:0 32px;position:sticky;top:0;z-index:2;font-size:13px;color:var(--m)}.status{background:var(--p);color:var(--g);padding:8px 12px;border-radius:25px;font-size:11px;font-weight:bold}.content{max-width:1200px;margin:auto;padding:30px}
.eyebrow{font-size:11px;color:var(--g);font-weight:bold;letter-spacing:1.3px}.heading{margin-bottom:22px}.heading h2{font-size:29px;color:#174c30;margin:7px 0}.heading p{color:var(--m);font-size:14px;line-height:1.6;margin:0}
.hero{display:grid;grid-template-columns:1.3fr .7fr;align-items:center;background:linear-gradient(110deg,#fff,#eff9f2);border:1px solid var(--l);border-radius:20px;padding:25px;margin-bottom:20px}.hero h2{font-size:28px;color:#145d35;margin:8px 0}.hero p{color:var(--m);font-size:14px;line-height:1.7}.art{display:flex;justify-content:center}.art svg{width:220px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:13px}.metric,.card,.tool{background:#fff;border:1px solid var(--l);border-radius:15px;padding:18px}.metric span{font-size:12px;color:var(--m)}.metric b{display:block;font-size:29px;color:var(--d);margin-top:8px}.toolgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.tool{display:block;text-decoration:none;transition:.15s}.tool:hover{border-color:#a9d6b8;transform:translateY(-2px)}.tool i{display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:var(--p);color:var(--g);font-style:normal;font-size:19px;margin-bottom:10px}.tool b{color:#24553a;font-size:14px}.tool small{display:block;color:var(--m);font-size:12px;line-height:1.5;margin-top:6px}
.btn{display:inline-block;background:var(--g);color:white;border:0;border-radius:10px;padding:12px 17px;font-weight:bold;font-size:13px;text-decoration:none;cursor:pointer}.light{background:var(--p);color:var(--d);border:1px solid #cfe6d6}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
label{display:block;color:#355743;font-size:13px;font-weight:bold;margin:13px 0 7px}textarea,input[type=url]{width:100%;border:1px solid #d7e6dc;border-radius:10px;padding:13px;font:14px Arial;background:#fcfefc}textarea{min-height:135px;resize:vertical}.checks{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:12px 0}.check{display:flex;gap:9px;padding:12px;border:1px solid var(--l);border-radius:10px;font-size:13px;line-height:1.45}.check input{accent-color:var(--g)}
.result{background:#fff;border:1px solid var(--l);border-radius:15px;padding:20px;margin-top:18px}.risk{display:inline-block;padding:8px 13px;border-radius:22px;background:var(--p);color:var(--g);font-size:12px;font-weight:bold}.HIGH{background:#fff0e8;color:#a44716}.MEDIUM{background:#fff8df;color:#896915}.result h3{color:#195b36;margin:20px 0 8px}.result li{font-size:13px;color:#4c6657;line-height:1.6;margin:5px 0}.notice{background:var(--p);border:1px solid #d5eadb;border-radius:12px;padding:14px;color:#41634e;font-size:13px;line-height:1.6}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:12px 9px;border-bottom:1px solid #edf3ee}th{font-size:11px;color:var(--m);text-transform:uppercase}
@media(max-width:850px){.side{width:210px}.main{margin-left:210px}.grid{grid-template-columns:repeat(2,1fr)}.toolgrid{grid-template-columns:repeat(2,1fr)}.content{padding:22px}}
@media(max-width:620px){.side{position:relative;width:100%;height:auto;padding:9px}.brand{padding:4px 7px 10px;margin:0 0 7px}.navlabel,.sidefoot{display:none}nav{display:flex;overflow-x:auto;gap:4px}nav a{white-space:nowrap;padding:9px;font-size:12px}.main{margin:0}.top{height:50px;padding:0 14px}.content{padding:17px 12px}.hero{grid-template-columns:1fr;padding:19px}.art{display:none}.grid{gap:8px}.metric{padding:12px}.toolgrid{grid-template-columns:1fr 1fr;gap:8px}.tool{padding:12px}.checks{grid-template-columns:1fr}.heading h2{font-size:24px}}
"""
LOGO='<svg class="logo" viewBox="0 0 64 64"><path d="M32 4 55 13v17c0 15-9 24-23 30C18 54 9 45 9 30V13Z" fill="#16834a"/><path d="m23 32 6 6 13-14" fill="none" stroke="white" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ART='<svg viewBox="0 0 240 180"><circle cx="120" cy="90" r="78" fill="#e4f4e9"/><path d="M120 25 170 44v36c0 31-19 49-50 64-31-15-50-33-50-64V44Z" fill="#16834a"/><path d="m95 87 17 17 34-38" fill="none" stroke="white" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def hist(): return session.get("history",[])
def report(name,score,flags,tips,detail=""):
    score=min(10,int(score)); lv="HIGH" if score>=8 else "MEDIUM" if score>=4 else "LOW"; stamp=datetime.now().strftime("%d %b %Y, %I:%M %p")
    f="".join("<li>"+html.escape(x)+"</li>" for x in flags) or "<li>No strong warning signs found in the provided information.</li>"
    t="".join("<li>"+html.escape(x)+"</li>" for x in tips)
    session.setdefault("history",[]).append({"name":name,"score":score,"risk":lv,"time":stamp});session["history"]=session["history"][-50:];session.modified=True
    return f'<div class="result"><small style="color:#819487">ASSESSMENT REPORT · {stamp}</small><h2 style="color:#195b36">{name}</h2><span class="risk {lv}">{lv} RISK</span> <b>Score: {score}/10</b><p style="color:#647d6e;font-size:13px">{detail}</p><h3>Indicators</h3><ul>{f}</ul><h3>Recommended actions</h3><ul>{t}</ul><small style="color:#819487">Educational rule-based assessment only; not a live security scan.</small></div>'
def shell(active,body):
    links="".join(f'<a class="{"active" if s==active else ""}" href="/{s}"><span class="ico">{i}</span>{l}</a>' for s,l,i in PAGES); title=dict((s,l) for s,l,i in PAGES)[active]
    template="""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}} | CyberShield</title><style>{{css|safe}}</style></head><body><aside class="side"><a class="brand" href="/dashboard">{{logo|safe}}<div><h1>CyberShield</h1><small>CYBER SAFETY EXPERT SYSTEM</small></div></a><div class="navlabel">WORKSPACE</div><nav>{{links|safe}}</nav><div class="sidefoot">● SYSTEM READY<br>Educational rule-based engine<br>Version 1.0</div></aside><main class="main"><header class="top"><span>Workspace / <b>{{title}}</b></span><span class="status">● SYSTEM READY</span></header><section class="content">{{body|safe}}</section></main></body></html>"""
    return render_template_string(template,title=title,css=CSS,logo=LOGO,links=links,body=body)
def head(k,t,d): return f'<div class="heading"><div class="eyebrow">{k}</div><h2>{t}</h2><p>{d}</p></div>'
def text_page(slug,title,desc,kind):
    body=head("CYBERSHIELD TOOL",title,desc)+f'<div class="card"><form method="post"><label>Paste text for review</label><textarea name="message" placeholder="Paste the text here. Do not include passwords or private information." required></textarea><div class="actions"><button class="btn">Analyze now →</button><a class="btn light" href="/{slug}">Reset</a></div></form></div>'
    if request.method=="POST":
        t=request.form["message"].lower()
        rules={
        "scam":[("Urgent pressure or threats",3,["urgent","immediately","within 24 hours","account will be blocked"]),("Requests for OTP, PIN, password, or bank details",4,["otp","pin","password","bank details","card number"]),("Unexpected prize or lottery claim",2,["you won","prize","lottery","free gift"]),("Advance payment request",3,["processing fee","send money","pay first","transfer fee"]),("Suspicious link wording",2,["click here","verify now","claim now"])],
        "job":[("Upfront recruitment or processing fee",4,["registration fee","security fee","training fee","pay first"]),("Unusually high income promise",2,["guaranteed income","earn thousands daily","easy money"]),("Sensitive banking information requested",3,["otp","bank password","pin","card details"]),("Pressure to act immediately",2,["limited time","today only","immediately"])],
        "email":[("Unexpected sender wording",2,["unknown sender","unfamiliar sender"]),("Credentials or financial information requested",4,["password","otp","bank details","credit card"]),("Urgent action language",2,["urgent","immediately","suspended"]),("Unexpected attachment or link",2,["attachment","open the file","click the link","download now"])]}
        found=[(label,points) for label,points,words in rules[kind] if any(w in t for w in words)]
        body+=report(title+" result",sum(p for _,p in found),[x for x,_ in found],["Do not share OTPs, PINs, passwords, or banking details.","Verify the sender through an official contact method.","Pause before clicking links or opening unexpected files."])
    return shell(slug,body)
@app.route("/")
def root(): return redirect("/dashboard")
@app.route("/dashboard")
def dashboard():
    h=hist(); names=dict((s,l) for s,l,i in PAGES); icons=dict((s,i) for s,l,i in PAGES)
    desc={"scam":"Identify warning signs in suspicious messages.","job":"Review job offers for recruitment scams.","link":"Check URLs for unusual patterns.","email":"Review email text for phishing indicators.","password":"Review password habits without entering a password.","account":"Review account protection settings.","device":"Review device safety practices.","wifi":"Review Wi-Fi network settings.","privacy":"Review everyday privacy settings."}
    tools="".join(f'<a class="tool" href="/{s}"><i>{icons[s]}</i><b>{names[s]}</b><small>{d}</small></a>' for s,d in desc.items())
    rows="".join(f'<tr><td>{x["time"]}</td><td>{x["name"]}</td><td>{x["risk"]}</td><td>{x["score"]}/10</td></tr>' for x in h[::-1][:5]) or '<tr><td colspan="4">No assessments yet. Choose a tool to get started.</td></tr>'
    n=len(h); hi=sum(x["risk"]=="HIGH" for x in h); med=sum(x["risk"]=="MEDIUM" for x in h); lo=sum(x["risk"]=="LOW" for x in h)
    body=f'<div class="hero"><div><div class="eyebrow">YOUR DIGITAL SAFETY WORKSPACE</div><h2>Stay alert. Stay protected.</h2><p>Review common online safety risks with simple rule-based checks and practical recommendations.</p><div class="actions"><a class="btn" href="/scam">Start assessment →</a><a class="btn light" href="/guide">How it works</a></div></div><div class="art">{ART}</div></div><div class="grid"><div class="metric"><span>Total assessments</span><b>{n}</b></div><div class="metric"><span>High risk</span><b>{hi}</b></div><div class="metric"><span>Medium risk</span><b>{med}</b></div><div class="metric"><span>Low risk</span><b>{lo}</b></div></div><div style="margin:27px 0 13px"><div class="eyebrow">SECURITY MODULES</div><h3 style="color:#195b36">Choose a tool</h3></div><div class="toolgrid">{tools}</div><div class="card" style="margin-top:20px"><h3 style="color:#195b36">Recent assessments</h3><table><tr><th>Date</th><th>Assessment</th><th>Risk</th><th>Score</th></tr>{rows}</table></div>'
    return shell("dashboard",body)
@app.route("/scam",methods=["GET","POST"])
def scam(): return text_page("scam","Scam Checker","Review suspicious messages for common scam signals.","scam")
@app.route("/job",methods=["GET","POST"])
def job(): return text_page("job","Job Offer Checker","Look for warning signs in recruitment messages.","job")
@app.route("/email",methods=["GET","POST"])
def email(): return text_page("email","Email Phishing","Review email wording for phishing indicators.","email")
@app.route("/link",methods=["GET","POST"])
def link():
    body=head("CYBERSHIELD TOOL","Link Safety","Review a URL structure. This does not check live website reputation.")+'<div class="card"><form method="post"><label>Website URL</label><input type="url" name="url" placeholder="https://example.com" required><div class="actions"><button class="btn">Check link →</button></div></form></div>'
    if request.method=="POST":
        u=urlparse(request.form["url"]); host=(u.hostname or "").lower(); score=0; flags=[]
        if u.scheme=="http":score+=2;flags.append("The link uses unencrypted HTTP.")
        if not host or "." not in host:score+=3;flags.append("The address does not look like a normal public domain.")
        if re.search(r"(\\d{1,3}\\.){3}\\d{1,3}",host):score+=3;flags.append("The address uses a raw IP address.")
        if len(host)>45 or host.count("-")>=3:score+=2;flags.append("The domain has unusual length or many hyphens.")
        body+=report("Link safety result",score,flags,["Verify the domain independently before entering details.","Check spelling of the official web address.","Avoid unexpected downloads."],"Basic URL pattern check only; no live reputation lookup.")
    return shell("link",body)
CHECKS={
"password":("Password Safety","Review password habits. Never enter your actual password.",[("short","Password is shorter than 12 characters",3),("mix","It lacks a mix of character types",2),("reuse","It is reused on other accounts",4),("personal","It may contain personal or common information",2),("manager","It is not stored in a password manager",1)],["Use long, unique passwords.","Consider a reputable password manager.","Enable multi-factor authentication."]),
"account":("Account Security","Review account protection settings.",[("mfa","Multi-factor authentication is not enabled",2),("reuse","The same password is reused",3),("login","An unknown login or session was noticed",4),("recovery","Recovery information is outdated",2),("alerts","Security alerts have been ignored",2)],["Enable multi-factor authentication.","Use unique passwords and review active sessions.","Update recovery options."]),
"device":("Device Safety","Review everyday device security practices.",[("updates","System or apps are not updated",2),("sources","Apps came from unknown sources",3),("lock","No screen lock is enabled",2),("popups","Unrecognised apps or unusual pop-ups appear",3),("backup","Important data is not backed up",1)],["Install updates from official settings.","Use trusted app stores.","Use a screen lock and keep backups."]),
"wifi":("Wi-Fi Security","Review home or public Wi-Fi settings.",[("default","Router uses its default administrator password",3),("open","Network has no password",4),("weak","Outdated or weak Wi-Fi encryption is used",3),("unknown","Unknown devices are connected",2),("firmware","Router firmware has not been updated",2)],["Use WPA2 or WPA3 on your own router.","Change default administrator credentials.","Update router firmware."]),
"privacy":("Privacy Checkup","Review common privacy settings.",[("permissions","Apps have permissions they do not need",2),("public","Personal contact details are public",2),("location","Location sharing is always enabled",2),("settings","Privacy settings have not been reviewed",2),("profiles","Personal details are public across many sites",2)],["Limit app permissions.","Review public profile information and location sharing.","Use privacy controls."])}
@app.route("/<slug>",methods=["GET","POST"])
def checklist(slug):
    if slug not in CHECKS: return ("Not found",404)
    title,desc,fields,tips=CHECKS[slug]; body=head("CYBERSHIELD ASSESSMENT",title,desc)
    if slug=="password":body+='<div class="notice"><b>Privacy reminder:</b> Never type or paste your real password into this tool.</div>'
    body+='<div class="card"><form method="post"><div class="checks">'+''.join(f'<label class="check"><input type="checkbox" name="{k}"><span>{label}</span></label>' for k,label,p in fields)+'</div><div class="actions"><button class="btn">Assess now →</button><a class="btn light" href="/'+slug+'">Reset</a></div></form></div>'
    if request.method=="POST":
        chosen=[(label,p) for k,label,p in fields if request.form.get(k)=="on"]
        body+=report(title+" result",sum(p for _,p in chosen),[x for x,_ in chosen],tips)
    return shell(slug,body)
@app.route("/history")
def history_page():
    rows="".join(f'<tr><td>{x["time"]}</td><td>{x["name"]}</td><td>{x["risk"]}</td><td>{x["score"]}/10</td></tr>' for x in hist()[::-1]) or '<tr><td colspan="4">No assessments yet.</td></tr>'
    body=head("WORKSPACE RECORDS","Assessment History","Checks completed during this browser session.")+f'<div class="card"><table><tr><th>Date and time</th><th>Assessment</th><th>Risk</th><th>Score</th></tr>{rows}</table><form method="post" action="/history/clear"><div class="actions"><button class="btn light">Clear session history</button></div></form></div>'
    return shell("history",body)
@app.route("/history/clear",methods=["POST"])
def clear():session["history"]=[];return redirect("/history")
@app.route("/guide")
def guide():
    body=head("HELP CENTRE","Security Guide","A quick guide to using CyberShield.")+'<div class="card"><h3>How to use the system</h3><ol style="line-height:2;color:#4c6657"><li>Choose a feature from the sidebar. Each opens its own web page and URL.</li><li>Enter only requested information. Never paste passwords, OTPs, or bank details.</li><li>Select Analyze or Assess to run predefined rules.</li><li>Read the risk level, score, indicators, and recommendations.</li><li>Use Assessment History to review checks in this browser session.</li></ol></div><div class="card"><h3>About CyberShield</h3><p style="line-height:1.8;color:#587263">CyberShield is an educational rule-based expert system. It demonstrates predefined IF-THEN rules on supplied text and checklist answers. It does not connect to live threat databases, scan devices, or guarantee that a message or link is safe.</p></div><div class="notice"><b>Safety first:</b> Never share passwords, one-time codes, banking PINs, or private identity information.</div>'
    return shell("guide",body)
if __name__=="__main__":
    try:
        from google.colab.output import eval_js
        from threading import Thread
        Thread(target=lambda:app.run(host="0.0.0.0",port=7861,debug=False,use_reloader=False),daemon=True).start()
        print("CyberShield is starting. Open this URL:")
        print(eval_js("google.colab.kernel.proxyPort(7861)"))
    except Exception:
        app.run(host="127.0.0.1",port=7861,debug=False)
