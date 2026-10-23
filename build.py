#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-couples.

A single-purpose page for the seasonal "vision board for couples" / "couples goals 2027" intent
(couples plan the new year together in December-January): 36 shared goals in 6 groups, each with
why it matters and a first step you do together this week, and a link that opens the free phone
maker with that goal and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098),
so both partners can save the same lock screen. Plus 12 questions to ask each other, a 45-minute
plan for the evening, a box for your own shared goal, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-couples/"
SRC = "ghpages_couples"
CAMPAIGN = "couples_2027"

# (group, [(shared goal, why it matters, a first step you do together this week)])
GROUPS = [
    ("Home", [
        ("A home that feels calm when we walk in", "The place we come back to sets the mood of the evening.", "Clear the hallway together on Saturday"),
        ("Our own place by the end of 2027", "A date turns a dream into a plan.", "Look at three listings together on Sunday"),
        ("One room we finally finish", "Half-done rooms quietly cost energy every day.", "Pick the room and write the three things it needs"),
        ("A shared weekly reset", "Chores split fairly stop being a fight.", "Agree on one 30-minute Sunday reset and try it"),
        ("Plants, light and a table we eat at", "Small comforts make an ordinary Tuesday better.", "Eat one dinner at the table this week, no screens"),
        ("Less stuff, more room for us", "Fewer things to manage, more time for each other.", "Each of us gives away five things this weekend"),
    ]),
    ("Money", [
        ("A savings goal we both believe in", "Saving is easier when it has a name and a date.", "Name the goal and the amount over coffee"),
        ("No money surprises", "Most money fights start with not knowing.", "Do a 20-minute money date and look at last month"),
        ("Debt-free together", "Every payment is a step toward more freedom.", "List every debt on one page with the next payment"),
        ("A buffer of three months", "A safety net makes hard months less scary.", "Set up one automatic transfer on payday"),
        ("A trip paid in cash", "Fun without the bill afterwards.", "Open a separate pot and put the first 20 EUR in"),
        ("One shared budget we actually use", "A plan we both understand beats a perfect one.", "Pick the app or sheet and fill in one week"),
    ]),
    ("Travel and adventure", [
        ("One trip just the two of us", "Time away is where we remember why we are together.", "Pick the month and put it in both calendars"),
        ("A new place every season", "Four small adventures beat one big someday.", "Write four places, one per season, and choose the first"),
        ("Our first trip abroad together", "New places show new sides of each other.", "Check both passports and their expiry dates tonight"),
        ("A weekend with no plan", "Spontaneity needs a gap in the calendar.", "Block one free weekend in the next two months"),
        ("Learn a little of a new language", "Ordering dinner in their language is a good story.", "Install one app and do the first lesson together"),
        ("Sunrise somewhere beautiful", "Some memories are worth the early alarm.", "Find one sunrise spot within an hour of home"),
    ]),
    ("Time together", [
        ("A real date every week", "Couples who keep dating stay close.", "Put a recurring date night in both calendars"),
        ("Phones away at dinner", "Attention is the simplest way to show love.", "Leave both phones in another room at dinner tonight"),
        ("A ten-minute talk every evening", "Small daily check-ins prevent big monthly fights.", "Ask each other one question from this page tonight"),
        ("A hobby we share", "Learning something together builds a new kind of team.", "Each suggest one hobby and try one this month"),
        ("A monthly look back", "Noticing progress keeps the board alive.", "Set a reminder for the last Sunday of the month"),
        ("More laughing, less logistics", "Not every conversation needs to be about schedules.", "Watch or play one silly thing together this week"),
    ]),
    ("Health and energy", [
        ("Move together three times a week", "It is easier to keep a habit when someone waits for you.", "Plan two walks together this week"),
        ("Sleep before midnight", "Rested people are kinder to each other.", "Agree on a lights-out time and try it for three nights"),
        ("Cook at home more", "Cooking together is a date that also feeds you.", "Plan three dinners and shop for them together"),
        ("A first race or hike together", "A shared finish line is a strong memory.", "Pick one event in 2027 and look up the date"),
        ("Less alcohol, more energy", "Better mornings, better weekends.", "Choose two alcohol-free days this week"),
        ("Take care of what we postpone", "Health checks are easier with company.", "Book the appointment each of us keeps postponing"),
    ]),
    ("Family and friends", [
        ("See our friends more often", "Friendships need time on the calendar too.", "Invite one couple over this month"),
        ("Our own traditions", "Rituals make a couple feel like a family.", "Choose one tradition to start this December"),
        ("Fair time with both families", "Balance avoids quiet resentment.", "Write down how we split the holidays this year"),
        ("Get ready for a baby", "Preparing together makes the change less scary.", "Each write three hopes and three worries and share them"),
        ("Host a dinner every season", "A full table is good for a home.", "Pick the date and the first guests for winter"),
        ("Help someone together", "Giving as a team feels different from giving alone.", "Choose one cause and plan one afternoon for it"),
    ]),
]

QUESTIONS = [
    "What was your favorite moment of us in 2026?",
    "What do you want to feel more of next year?",
    "What is one thing I could do that would make your week easier?",
    "Where do you want us to be living at the end of 2027?",
    "What is one place you want us to see together?",
    "What does a perfect ordinary Saturday look like for you?",
    "What is one money goal that would make you feel safer?",
    "Which habit of ours do you want to keep, and which one to drop?",
    "What do you want to learn in 2027, and how can I help?",
    "How do you want us to handle the busy weeks?",
    "What tradition do you want us to start?",
    "What is one thing you are proud of us for?",
]

PLAN = [
    ("10 minutes: look back.", "Each of you names three moments from 2026 you loved and one you want to do differently. Listen, do not fix."),
    ("15 minutes: ask the questions.", "Take turns with the 12 questions below. Write down every answer that makes you both nod."),
    ("10 minutes: pick three shared goals.", "One for home or money, one for time together, one just for fun. Fewer goals, kept, beat a long list."),
    ("10 minutes: make it visible.", "Turn your favorite goal and its first step into the same lock screen on both phones, or make a full board together."),
]

FAQ = [
    ("What is a vision board for couples?",
     "A board of the goals you share as a couple for the coming year, such as a home, a trip, a savings goal or more time together. "
     "You make it together, so it doubles as a conversation about what you both want."),
    ("How do you make a couples vision board?",
     "Look back at the year together, ask each other a few honest questions, pick three shared goals and make them visible. "
     "This page has 36 shared goals with a first step, 12 questions and a 45-minute plan."),
    ("What should a couple put on a vision board?",
     "Goals you both care about: where you live, money, travel, time together, health and the people around you. "
     "Add one first step to each goal so the board tells you what to do this week, not only what to dream about."),
    ("Can we both have the same lock screen?",
     "Yes. Press a goal or type your own, save the 1080x1920 image, then open the same link on the other phone. "
     "Seeing the same goal every day is a quiet reminder that you are working on it together."),
    ("Is the lock-screen maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing."),
    ("Can we make a full vision board with several goals?",
     "Yes. Start from your shared goal in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]


def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step together:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it our lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vision Board for Couples 2027: %%COUNT%% Shared Goals, %%NQ%% Questions &amp; a Free Lock Screen</title>
<meta name="description" content="Plan 2027 together: %%COUNT%% shared goals for couples, each with a first step for this week, %%NQ%% questions to ask each other and a 45-minute plan. Turn your goal into the same free lock screen on both phones. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Vision board for couples 2027 - %%COUNT%% shared goals and a free lock screen">
<meta property="og:description" content="Shared goals with a first step, %%NQ%% questions to ask each other, and the same lock screen on both phones. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#BE185D;--bg:#FDFAF9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#9D174D;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Vision board for couples 2027: %%COUNT%% shared goals and one lock screen for both of you</h1>
  <p class="lede">Plan next year together instead of making two separate lists. Below are %%COUNT%% shared goals, each with why it matters and a first step you can do together this week, plus %%NQ%% questions to ask each other. Press a goal and it opens on a free phone lock screen with the first step under it. Save it, open the same link on the other phone, and you both see the same goal every day. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; 1080&times;1920 lock screen &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your shared goal?</h2>
  <div class="row">
    <div><label for="ownGoal">Our goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Our own place with a garden" autocomplete="off"></div>
    <div><label for="ownStep">Our first step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Look at three listings on Sunday" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it our lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, save, then open the same link on the other phone.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions to ask each other before you choose</h2>
  <p>Take turns. One person asks, the other answers, then swap. Write down every answer that makes you both nod: those are your goals.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Make it together in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with several goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full vision board around our goals</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-couples">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own shared goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your shared goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
