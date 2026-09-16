#!/usr/bin/env python3
"""Generates the Behavioral Software Engineering Interview Prep document."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    ListFlowable, ListItem, KeepTogether, HRFlowable
)
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = "Behavioral_Interview_Prep.pdf"

# ---------------------------------------------------------------- styles ---
ss = getSampleStyleSheet()

NAVY = colors.HexColor("#1B2A4A")
GOLD = colors.HexColor("#B7862C")
GRAY = colors.HexColor("#5A5F6B")
LGRAY = colors.HexColor("#F2F3F5")
GREEN = colors.HexColor("#2E7D46")
RED = colors.HexColor("#B3372C")

styles = {
    "CoverTitle": ParagraphStyle("CoverTitle", parent=ss["Title"], fontSize=28,
                                  leading=34, textColor=NAVY, spaceAfter=10, alignment=TA_LEFT),
    "CoverSub": ParagraphStyle("CoverSub", parent=ss["Normal"], fontSize=14,
                                 leading=20, textColor=GRAY, spaceAfter=6),
    "PartTitle": ParagraphStyle("PartTitle", parent=ss["Title"], fontSize=20,
                                  leading=24, textColor=NAVY, spaceBefore=0, spaceAfter=14,
                                  borderWidth=0),
    "H2": ParagraphStyle("H2", parent=ss["Heading2"], fontSize=14, leading=17,
                           textColor=NAVY, spaceBefore=16, spaceAfter=8),
    "H3": ParagraphStyle("H3", parent=ss["Heading3"], fontSize=12, leading=15,
                           textColor=GOLD, spaceBefore=12, spaceAfter=6),
    "Body": ParagraphStyle("Body", parent=ss["Normal"], fontSize=9.6, leading=13.5,
                             spaceAfter=6, textColor=colors.black),
    "BodySmall": ParagraphStyle("BodySmall", parent=ss["Normal"], fontSize=8.8, leading=12,
                             spaceAfter=4, textColor=colors.black),
    "Bullet": ParagraphStyle("Bullet", parent=ss["Normal"], fontSize=9.6, leading=13.5,
                               leftIndent=12, spaceAfter=3),
    "Note": ParagraphStyle("Note", parent=ss["Normal"], fontSize=9, leading=12.5,
                             textColor=RED, spaceAfter=6, spaceBefore=10, leftIndent=6,
                             borderColor=RED, borderWidth=0.6, borderPadding=6,
                             backColor=colors.HexColor("#FBEEEC")),
    "Placeholder": ParagraphStyle("Placeholder", parent=ss["Normal"], fontSize=9.4, leading=13,
                             textColor=colors.HexColor("#8A5A00"), spaceAfter=4, leftIndent=12),
    "TableCell": ParagraphStyle("TableCell", parent=ss["Normal"], fontSize=8.2, leading=10.6),
    "TableHead": ParagraphStyle("TableHead", parent=ss["Normal"], fontSize=8.4, leading=10.6,
                             textColor=colors.white, fontName="Helvetica-Bold"),
    "Quiz": ParagraphStyle("Quiz", parent=ss["Normal"], fontSize=9.4, leading=13,
                             leftIndent=10, spaceAfter=4, textColor=NAVY),
    "Checklist": ParagraphStyle("Checklist", parent=ss["Normal"], fontSize=9.6, leading=14,
                             leftIndent=4, spaceAfter=3),
    "CardLabel": ParagraphStyle("CardLabel", parent=ss["Normal"], fontSize=9, leading=12,
                             textColor=NAVY, fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=2),
    "Footer": ParagraphStyle("Footer", parent=ss["Normal"], fontSize=7.5, textColor=GRAY),
}

flow = []

def P(text, style="Body"):
    flow.append(Paragraph(text, styles[style]))

def SP(h=6):
    flow.append(Spacer(1, h))

def HR(color=GOLD, thick=1):
    flow.append(HRFlowable(width="100%", thickness=thick, color=color, spaceBefore=4, spaceAfter=8))

def PART(number, title, subtitle=""):
    flow.append(PageBreak())
    flow.append(Paragraph(f"PART {number}", ParagraphStyle("pn", parent=ss["Normal"], fontSize=10,
                            textColor=GOLD, fontName="Helvetica-Bold", spaceAfter=2)))
    flow.append(Paragraph(title, styles["PartTitle"]))
    if subtitle:
        flow.append(Paragraph(subtitle, styles["CoverSub"]))
    HR()

def H2(t):
    P(t, "H2")

def H3(t):
    P(t, "H3")

def bullets(items, style="Bullet"):
    lf = ListFlowable(
        [ListItem(Paragraph(i, styles[style]), spaceAfter=3) for i in items],
        bulletType="bullet", start="•", leftIndent=14
    )
    flow.append(lf)

def note(text, label="IMPORTANT"):
    P(f"<b>{label}:</b> {text}", "Note")

def placeholder(text):
    P(f"[FILL IN — {text}]", "Placeholder")

def card_label(t):
    P(t, "CardLabel")

def keep(items):
    flow.append(KeepTogether(items))

def make_table(header, rows, col_widths, font_size=8.2, header_bg=NAVY, small=True):
    style_name = "TableCell" if not small else "TableCell"
    data = [[Paragraph(h, styles["TableHead"]) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), styles[style_name]) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CDD3")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LGRAY]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    flow.append(t)
    SP(8)

def checklist(items):
    for i in items:
        P(f"[&#160;&#160;] {i}", "Checklist")

# =============================================================== COVER ===
flow.append(Spacer(1, 60))
P("BEHAVIORAL INTERVIEW", "CoverTitle")
P("PREPARATION SYSTEM", "CoverTitle")
SP(4)
P("For Software Engineering Internships and Early-Career Roles", "CoverSub")
P("Prepared for: sawissah@st.knust.edu.gh", "CoverSub")
SP(20)
HR(NAVY, 1.4)
SP(10)
P("<b>What this document is.</b> A working system for turning your real engineering "
  "experience &#8212; the Financial Account Aggregation API, LedgerCore, the FarmLink hackathon, "
  "Robotics Club, and the KNUST CS Open Source Community &#8212; into a small set of stories you know "
  "so well that you can answer almost any behavioral question naturally, without a memorized script.",
  "Body")
P("<b>What this document is not.</b> It is not a list of answers to memorize. There are no "
  "paragraphs written for you to recite. Every story card has blanks marked "
  "<font color='#8A5A00'><b>[FILL IN]</b></font> where only you can supply the real detail "
  "&#8212; the exact number, the exact moment, the exact words someone said. If you fill in a blank "
  "with something that didn't happen, the system breaks the first time an interviewer asks a follow-up.",
  "Body")
note("This document never invents an event, a metric, a conflict, or a failure on your behalf. "
     "Where your background material didn't include a specific detail (an exact number, a specific "
     "conflict, a specific piece of feedback), you'll see a bracketed prompt instead of a fabricated "
     "answer. Filling those in honestly, before your interview, is part of the preparation &#8212; "
     "not an optional extra.")
SP(10)
H2("How to use this document")
bullets([
    "Read Parts 1&#8211;2 once, so you understand what behavioral interviews are actually measuring.",
    "Spend most of your time in Part 3 and Part 5 &#8212; build your Story Bank and fill in every "
    "[FILL IN] blank with a real, specific, honest detail.",
    "Use Part 6, Part 8, and Part 24 for practice &#8212; out loud, not silently in your head.",
    "Use Part 20 (rubric) to score yourself honestly after each practice session.",
    "Review Part 26 (the Handbook) the night before an interview &#8212; not the whole document.",
])
SP(10)
H2("Document map")
toc_rows = [
    ("1", "What Behavioral Interviews Actually Test"),
    ("2", "Behavioral Competency Map"),
    ("3", "Your Story Bank"),
    ("4", "Story Coverage Matrix"),
    ("5", "The Story Card System (full cards)"),
    ("6", "Question &#8594; Story Mapping"),
    ("7", "Deep Prep on the Highest-Stakes Questions"),
    ("8", "Follow-Up Question Training (20 chains)"),
    ("9", "Project-Specific Behavioral Questions"),
    ("10", "Responsible AI Behavioral Questions"),
    ("11", "Impact and Metrics"),
    ("12", "What Interviewers May Actually Hear"),
    ("13", "Common Behavioral Mistakes and Fixes"),
    ("14", "Conversational Delivery"),
    ("15", "Handling Questions You Don't Have a Perfect Story For"),
    ("16", "Hypothetical Behavioral Questions"),
    ("17", "Company-Specific Preparation Framework"),
    ("18", "Questions to Ask the Interviewer"),
    ("19", "Mock Interview System (6 modes)"),
    ("20", "Scoring Rubric"),
    ("21", "30 / 60 / 2-Minute Answer Compression"),
    ("22", "Active Recall Exercises"),
    ("23", "Story Retrieval Drills"),
    ("24", "Random Question Bank (mixed practice)"),
    ("25", "Your Personal Behavioral Gaps"),
    ("26", "Your Personal Behavioral Handbook"),
]
make_table(["Part", "Contents"], toc_rows, [0.6*inch, 5.9*inch], header_bg=NAVY)

# ================================================================ PART 1 ===
PART(1, "What Behavioral Interviews Actually Test")

H2("Why companies ask behavioral questions at all")
P("A technical interview tells a company whether you can solve a defined problem in a defined "
  "amount of time. It does not tell them how you behave when a problem is ambiguous, when a teammate "
  "disagrees with you, when you're told your first idea is wrong, or when something you built breaks "
  "in a way you didn't anticipate. Almost all of real engineering work happens in exactly those "
  "conditions. Behavioral interviews exist to sample that part of the job.", "Body")

H2("The core assumption behind the format")
P("The format rests on one assumption: <b>the way you handled a real situation in the past is the "
  "best available evidence for how you'll handle a similar situation in the future.</b> Not a perfect "
  "predictor &#8212; just the best evidence an hour-long conversation can produce. That's why "
  "interviewers keep steering you back to specifics ('what did <i>you</i> do', 'what happened next', "
  "'why that option and not the other one') instead of accepting general statements about your "
  "personality or philosophy.", "Body")

H2("Why junior candidates are evaluated differently from senior engineers")
P("An interviewer does not expect an intern or new-grad candidate to have led a team through a "
  "production outage or negotiated a cross-org technical decision. What they're actually checking for "
  "at your level is much more foundational:", "Body")
bullets([
    "Can you accurately describe what you personally did, versus what a team or a tool did for you?",
    "Do you notice when something goes wrong, or do you only notice when someone else points it out?",
    "When you're shown you're wrong, do you get defensive, go quiet, or actually update your approach?",
    "Can you explain a technical decision to someone who doesn't share your technical context?",
    "Do you already have the instinct to check your own work, rather than assuming it's right?",
])
P("This is good news: it means your academic projects, your hackathon, and your club leadership are "
  "not a weaker substitute for \"real\" experience &#8212; for an internship-level interview, they "
  "<i>are</i> the real evidence the interviewer is looking for.", "Body")

H2("Why technical ability alone is not enough")
P("Software is built by teams, reviewed by other engineers, and eventually explained to people who "
  "did not write it &#8212; product managers, support teams, other engineers six months later, "
  "sometimes regulators or customers. An engineer who can write correct code but can't explain a "
  "tradeoff, can't say \"I was wrong about this,\" or can't work through a disagreement, is expensive "
  "to work with regardless of how good the code is. Behavioral interviews are the company's attempt "
  "to price that cost in before they hire you, not after.", "Body")

H2("Why interviewers ask follow-up questions")
P("A rehearsed answer and a lived experience sound identical for about 30 seconds. They diverge the "
  "moment someone asks a question you didn't prepare for &#8212; \"why didn't you just do X instead,\" "
  "\"how did you know it actually worked,\" \"what would you do differently now.\" Interviewers drill "
  "down specifically <i>because</i> a first answer is cheap to prepare. Your job is not to have a "
  "perfect first answer; it's to know your own experience deeply enough that the fifth follow-up "
  "question is no harder to answer than the first.", "Body")

H2("The underlying competencies repeat, even when the wording doesn't")
P("\"Tell me about a challenge,\" \"tell me about a time something didn't go as planned,\" and "
  "\"tell me about a difficult problem you solved\" are, underneath the wording, often the same "
  "question. This document is built around that idea: instead of memorizing answers to hundreds of "
  "possible phrasings, you learn roughly 24 underlying competencies (Part 2) and a small set of real "
  "stories (Part 3) that map onto them (Part 4), so that any new phrasing is just a matter of picking "
  "the right story and adjusting emphasis &#8212; not writing a new answer from scratch.", "Body")

# ================================================================ PART 2 ===
PART(2, "Behavioral Competency Map",
     "24 competencies interviewers actually screen for. For each: what it means, what strong and weak "
     "evidence look like, which of your stories can carry it, and where the gaps are.")

COMPETENCIES = [
    dict(name="Communication", means="Explaining ideas so the listener actually understands, adjusting "
         "to their background, and listening as much as you talk.",
         wants="Can this person be understood by teammates, PMs, and non-engineers?",
         strong="Clear structure, checks the listener understood, adapts language to audience, answers "
         "the question asked.", weak="Jargon-heavy, rambling, monologuing, never checks in.",
         stories="S3, S8, S9", qs="Explain a technical concept to a non-technical person; describe your "
         "role on a project.", mistake="Explaining a system the way you'd explain it to another engineer, "
         "regardless of who's asking."),
    dict(name="Teamwork", means="Working productively inside a group toward a shared goal.",
         wants="Do you make the people around you more effective, or do you work in spite of them?",
         strong="Names specific teammates' contributions, describes real coordination, shows shared "
         "credit without erasing personal contribution.", weak="Only 'we', no visible personal role, or "
         "the opposite: no one else in the story at all.",
         stories="S6, S7, S8", qs="Tell me about working on a team; a time you helped a teammate.",
         mistake="Using 'we' so consistently the interviewer can't find you in your own story."),
    dict(name="Conflict resolution", means="Handling a disagreement without damaging the relationship "
         "or avoiding the issue.", wants="Do you address disagreement directly and respectfully, or "
         "avoid/escalate it?", strong="States both perspectives fairly, focuses on evidence/reasoning, "
         "reaches or works toward a resolution.", weak="Makes the other person look foolish, avoids the "
         "conflict entirely, or claims there was never any disagreement.",
         stories="S11 (template &#8212; fill in)", qs="Disagreement with a teammate; a difficult "
         "teammate.", mistake="Framing the other person as simply wrong instead of holding a different, "
         "reasonable view."),
    dict(name="Leadership", means="Taking responsibility for outcomes beyond your own individual task, "
         "often by enabling other people.", wants="Do you step up, and do you make others better, or "
         "just yourself?", strong="Concrete actions that changed what other people did (taught, "
         "organized, unblocked), with a result.", weak="A title with no described action ('I was Training "
         "Lead') or credit-taking for others' independent work.",
         stories="S6, S7", qs="A time you demonstrated leadership; a time you influenced a team without "
         "authority.", mistake="Reciting a title instead of describing an action."),
    dict(name="Ownership", means="Treating a problem as yours to solve even when it isn't strictly your "
         "assigned responsibility, and being accountable for the outcome.",
         wants="When something in your area breaks, do you own it or point elsewhere?",
         strong="\"I noticed / I decided / I was responsible for\", follows through past the comfortable "
         "stopping point.", weak="Vague responsibility, or credit for success without acknowledging "
         "responsibility for the parts that went wrong.",
         stories="S1, S2, S4", qs="A time you took ownership; a time something in your project broke.",
         mistake="Taking ownership of successes only."),
    dict(name="Initiative", means="Starting something valuable without being told to.",
         wants="Do you wait for instructions, or do you notice gaps and act?",
         strong="Names the gap you noticed and the unprompted action you took.",
         weak="Initiative claimed for something that was actually assigned.",
         stories="S8, S9", qs="A time you took initiative; a time you went beyond what was asked.",
         mistake="Describing an assigned task as if it were self-initiated."),
    dict(name="Problem solving", means="Working systematically from a symptom to a root cause and a "
         "working fix.", wants="Is your process organized, or do you get lucky / guess-and-check?",
         strong="Names hypotheses considered and how each was tested; explains why the final approach "
         "won.", weak="\"I looked at it and eventually found the bug\" with no visible reasoning.",
         stories="S1, S3, S4", qs="A difficult technical problem; a bug you had to track down.",
         mistake="Skipping straight to the fix without showing the diagnostic reasoning."),
    dict(name="Failure and learning", means="Recognizing a genuine mistake, owning it, and changing "
         "behavior afterward.", wants="Do you have real self-awareness, or only manufactured humility?",
         strong="A real mistake with real consequences, followed by a concrete, lasting behavior change.",
         weak="A 'fake failure' (a humblebrag) or a real failure with no described change afterward.",
         stories="S10 (template &#8212; fill in)", qs="Tell me about a failure / mistake.",
         mistake="Choosing a failure that is actually a strength in disguise ('I worked too hard')."),
    dict(name="Coachability", means="Actually changing your behavior in response to feedback, not just "
         "agreeing with it politely.", wants="Will this person improve after we invest in mentoring them?",
         strong="Specific feedback received, specific behavior changed, evidence the change stuck.",
         weak="\"I'm very open to feedback\" with no example of feedback ever changing what you did.",
         stories="S12 (template &#8212; fill in)", qs="A time you received difficult feedback.",
         mistake="Describing being told something without describing anything you did differently after."),
    dict(name="Adaptability", means="Adjusting your plan, approach, or expectations when circumstances "
         "change.", wants="Do you rigidly stick to the original plan even after it stops working?",
         strong="Names what changed, what you adjusted, and why the adjustment was reasonable.",
         weak="A plan that never needed to change (not a real adaptability story).",
         stories="S3, S6", qs="A time you had to adapt; a time requirements changed.",
         mistake="Choosing a story where nothing was actually forced to change."),
    dict(name="Prioritization", means="Deciding what matters most when you can't do everything at once.",
         wants="Do you have a reasoning process for tradeoff decisions under time pressure?",
         strong="Names the competing items, the criteria used, and the choice made and why.",
         weak="\"I just did everything\" (avoids the actual prioritization question).",
         stories="S6, S9", qs="Competing priorities; limited time or resources.",
         mistake="Not admitting that something was deliberately deprioritized."),
    dict(name="Working under pressure", means="Maintaining judgment and output quality when time, "
         "stakes, or visibility increase.", wants="Do you degrade gracefully or panic/freeze under "
         "pressure?", strong="Describes the pressure concretely (deadline, stakes) and how you managed "
         "focus, not just the outcome.", weak="Pressure claimed but not actually present in the story "
         "(e.g., a relaxed weekend project).",
         stories="S6", qs="A high-pressure situation; a tight deadline.",
         mistake="Overstating pressure that wasn't really there, which falls apart under follow-up."),
    dict(name="Handling ambiguity", means="Making forward progress when requirements, scope, or the "
         "right approach are unclear.", wants="Do you stall waiting for clarity, or do you make "
         "reasonable assumptions and move?", strong="Names the specific ambiguity and how you resolved "
         "or worked around it.", weak="A story where everything was actually already well-specified.",
         stories="S5, S8", qs="A time requirements were unclear; a time you had to figure things out "
         "yourself.", mistake="Confusing 'hard' with 'ambiguous' &#8212; they're not the same thing."),
    dict(name="Decision-making", means="Choosing between real alternatives using explicit reasoning.",
         wants="Is there an actual decision process, or did you just do the first thing that occurred "
         "to you?", strong="States the alternatives seriously considered, the deciding factor, and the "
         "result.", weak="A 'decision' where there was really only ever one option.",
         stories="S1, S5", qs="A difficult decision; a time you chose between two approaches.",
         mistake="Presenting the option you didn't pick as obviously bad, in hindsight, to make your "
         "choice look better than it was at the time."),
    dict(name="Technical communication", means="Describing a technical system or decision at the right "
         "level of depth for the listener.", wants="Can you scale explanation depth up and down on "
         "request?", strong="A layered explanation: one-sentence version first, more detail available on "
         "request.", weak="One fixed level of detail regardless of who's asking or how they react.",
         stories="S3, S5", qs="Explain a project; explain a technical decision.",
         mistake="Front-loading implementation detail before establishing why the system exists."),
    dict(name="Explaining complex concepts simply", means="Translating jargon into plain, accurate "
         "language without dumbing it down incorrectly.", wants="Could a non-engineer stakeholder follow "
         "this?", strong="Uses an analogy or plain restatement that stays technically accurate.",
         weak="Simplifying to the point of being misleading, or not simplifying at all.",
         stories="S3, S5", qs="Explain something technical to a non-technical audience.",
         mistake="Reaching for an analogy that breaks down under a follow-up question."),
    dict(name="Persuasion", means="Getting someone to seriously consider or adopt your position using "
         "reasoning and evidence.", wants="Do you convince with evidence, or push, or give up too "
         "early?", strong="Names the other party's initial position, the evidence/argument you used, and "
         "what changed.", weak="\"I convinced them\" with no description of how.",
         stories="S8", qs="A time you persuaded someone; a time you changed someone's mind.",
         mistake="Persuasion stories that are actually just 'I was right and they eventually agreed' with "
         "no real description of the exchange."),
    dict(name="Dealing with disagreement", means="Staying constructive when someone (a peer, a tool, an "
         "AI suggestion) pushes back on your view.", wants="Composure and reasoning under pushback.",
         strong="Calm, evidence-based response; willing to update if the pushback has merit.",
         weak="Digging in regardless of evidence, or caving regardless of evidence.",
         stories="S2, S11 (template)", qs="Disagreement with a suggestion, a reviewer, or a teammate.",
         mistake="Treating every disagreement as something you must 'win'."),
    dict(name="Time management", means="Getting real output delivered within a deadline.",
         wants="Do you plan realistically and adjust, or discover the deadline too late?",
         strong="Names how you sequenced or scoped work to hit a real deadline.",
         weak="No visible planning, just an outcome.", stories="S6, S9",
         qs="A tight deadline; a hackathon.", mistake="Skipping straight to the result without the "
         "planning that got you there."),
    dict(name="Accountability", means="Accepting the consequences of your own actions, including "
         "unflattering ones, without deflecting.", wants="When it's your fault, do you say so?",
         strong="Explicit \"that was on me\" language followed by a fix.",
         weak="Passive voice that hides who was responsible ('mistakes were made').",
         stories="S10 (template)", qs="A time you made a mistake.",
         mistake="Technically admitting fault while emotionally blaming circumstances or other people."),
    dict(name="Attention to quality", means="Catching problems before they become someone else's "
         "problem &#8212; correctness, edge cases, data integrity.", wants="Do you check your own work, "
         "or rely entirely on others (reviewers, tests, AI) to catch issues?",
         strong="A specific edge case, duplicate, or race condition you caught and why you looked for "
         "it.", weak="\"I always write clean code\" with no concrete example.",
         stories="S1, S2, S4", qs="A time you caught a bug before it shipped; a quality/correctness "
         "story.", mistake="Confusing 'quality' with 'style' rather than correctness and reliability."),
    dict(name="Responsible use of AI", means="Using AI tools to move faster while still owning "
         "correctness, security, and understanding of the result.", wants="Are you leveraging AI, or "
         "outsourcing your judgment to it?", strong="A concrete moment you verified, tested, or rejected "
         "an AI suggestion.", weak="Either denying using AI at all, or describing it as a black box you "
         "trust without checking.", stories="S2", qs="How do you use AI when coding? Tell me about a "
         "time you disagreed with an AI suggestion.", mistake="Overclaiming AI fluency, or being unable "
         "to say how you verify AI output."),
    dict(name="Customer / user focus", means="Making decisions based on what the eventual user of the "
         "system actually needs, not just what's technically interesting.",
         wants="Do you think about who's affected downstream?",
         strong="Explains a decision in terms of the effect on the end user or data integrity for real "
         "accounts.", weak="Purely internal/technical framing with no mention of who the system serves.",
         stories="S3, S4", qs="A time you made a decision with the user in mind.",
         mistake="This is a genuine moderate-strength area for a student project &#8212; be honest that "
         "your 'users' were often simulated (mock bank providers) rather than real customers, and say so "
         "if asked directly."),
    dict(name="Curiosity", means="Going a level deeper than required because you wanted to actually "
         "understand something, not just make it pass.", wants="Will this person grow, or plateau at "
         "'good enough'?", strong="A specific instance of digging past the first working answer.",
         weak="\"I love learning\" with no concrete instance.",
         stories="S1, S2, S9", qs="A time you went deeper than necessary; a time you taught yourself "
         "something.", mistake="Confusing curiosity with general enthusiasm about the field."),
    dict(name="Career motivation", means="Having a coherent, honest reason for pursuing this field and "
         "this type of role.", wants="Is this genuine interest, or a generic answer that would fit any "
         "candidate?", strong="Specific, personal, tied to real projects and what you want to learn "
         "next.", weak="Generic ('I love solving problems and working with people').",
         stories="See Part 7", qs="Why software engineering? Why this role? Where do you see yourself "
         "in 5 years?", mistake="An answer that would be equally true if you'd never written a line of "
         "code."),
]

for c in COMPETENCIES:
    keep([
        Paragraph(c["name"], styles["H3"]),
        Paragraph(f"<b>What it means:</b> {c['means']}", styles["BodySmall"]),
        Paragraph(f"<b>What the interviewer is checking:</b> {c['wants']}", styles["BodySmall"]),
        Paragraph(f"<b>Strong evidence:</b> {c['strong']}", styles["BodySmall"]),
        Paragraph(f"<b>Weak evidence:</b> {c['weak']}", styles["BodySmall"]),
        Paragraph(f"<b>Your candidate stories:</b> {c['stories']}", styles["BodySmall"]),
        Paragraph(f"<b>Common questions:</b> {c['qs']}", styles["BodySmall"]),
        Paragraph(f"<b>Common mistake:</b> {c['mistake']}", styles["BodySmall"]),
    ])
    SP(4)

# ================================================================ PART 3 ===
PART(3, "Your Story Bank",
     "9 stories anchored in your real projects, plus 3 explicitly-marked gap templates for "
     "competencies your background material didn't document a story for.")

P("These are not 12 unrelated anecdotes. They're chosen so that, together, they cover almost every "
  "competency in Part 2 (see the coverage matrix in Part 4). You do not need more stories than this "
  "&#8212; you need to know these few in enough depth to bend them to whatever's actually asked.", "Body")

note("Three of the twelve rows below (S10, S11, S12) are templates, not finished stories. Your source "
     "material documented real projects and technical themes (concurrency, provider failures, "
     "duplicate prevention, AI-assisted development) but did not include a specific interpersonal "
     "conflict, a specific piece of critical feedback you received, or a specific failure with known "
     "consequences. Rather than invent one, this document leaves those three as structured blanks. "
     "Part 25 explains why that gap exists and how to close it honestly before your interviews.")

story_rows = [
    ("S1", "LedgerCore &#8212; Concurrency &amp; Idempotency", "Ensure double-entry transfers stayed "
     "consistent under concurrent access.", "Diagnosed a consistency risk in concurrent transfers; "
     "reasoned about transaction isolation, idempotency keys, and retry logic; validated with "
     "concurrent stress tests.", "[FILL IN: outcome of stress tests &#8212; did they pass, what "
     "changed]", "Correctness under concurrency has to be tested under concurrency, not assumed from "
     "code review.", "Problem solving, ownership, quality, technical communication, decision-making"),
    ("S2", "LedgerCore &#8212; Rejecting an AI Suggestion", "Use AI to accelerate development on "
     "LedgerCore while remaining responsible for correctness.", "An AI-suggested change would have "
     "masked an underlying data problem rather than fixing it; recognized this, rejected the "
     "suggestion, and pursued the actual root cause instead.", "[FILL IN: what the AI suggested "
     "specifically, and what the real root cause turned out to be]", "AI output has to be evaluated "
     "against understanding of the system, not accepted because it compiles or looks plausible.",
     "Responsible AI use, quality, technical judgment, ownership, curiosity"),
    ("S3", "Aggregation API &#8212; Provider Failures &amp; Rate Limiting", "Keep account linking and "
     "sync working when a mock bank provider fails or rate-limits requests.", "Designed handling for "
     "provider failure and rate-limit scenarios; considered retry/backoff and failure-isolation "
     "tradeoffs so one failing provider wouldn't degrade the whole system.", "[FILL IN: how the system "
     "behaved under simulated provider failure &#8212; recovery time, failure isolation]",
     "Design for the failure case, not just the happy path, especially in a system that touches "
     "financial data.", "Problem solving, tradeoffs, resilience/adaptability, technical communication"),
    ("S4", "Aggregation API &#8212; Duplicate Prevention in Background Sync", "Prevent duplicate "
     "transactions during background transaction synchronization.", "Identified how duplicates could "
     "enter the system during sync/retries; implemented a deduplication approach; verified it held up "
     "across repeated sync runs.", "[FILL IN: how duplicates were confirmed fixed &#8212; test result, "
     "before/after]", "Idempotent processing is not automatic in a distributed/background system "
     "&#8212; it has to be deliberately designed in.", "Attention to quality, problem solving, "
     "ownership, debugging"),
    ("S5", "Aggregation API &#8212; Kafka/Redis Architecture Tradeoff", "Choose an approach for "
     "background processing and caching of account/transaction data.", "Evaluated using Kafka for "
     "background/event-driven processing and Redis for caching/rate-limit state against simpler "
     "in-process alternatives; chose based on the system's actual needs.", "[FILL IN: the simpler "
     "alternative you considered and the specific reason you didn't pick it]", "Infrastructure choices "
     "should be justified by real requirements (throughput, decoupling, resilience), not by what's "
     "trendy.", "Decision-making, tradeoffs, technical communication, handling ambiguity"),
    ("S6", "FarmLink &#8212; Youth Arise Hackathon (Team Nova, won)", "Build a working product under "
     "hackathon time constraints as part of Team Nova.", "[FILL IN: your specific role and actions "
     "&#8212; what you personally built, decided, or presented]",
     "Team Nova won the hackathon. [FILL IN: what you'd credit the win to, and any real metric &#8212; "
     "team size, timeframe, judging criteria]", "[FILL IN: your main takeaway from the experience]",
     "Teamwork, pressure, prioritization, time management, presenting, adaptability"),
    ("S7", "Robotics Club &#8212; Training Lead &amp; Programmer", "Train and support other members as "
     "Training Lead while also contributing as a programmer.", "[FILL IN: specific things you did to "
     "train/mentor others &#8212; a curriculum, a session, a specific member you helped]",
     "[FILL IN: an observable result &#8212; a member's improvement, a competition result, a project "
     "shipped]", "[FILL IN: what you learned about teaching or leading]",
     "Leadership, mentoring, communication, teamwork, initiative"),
    ("S8", "KNUST CS Open Source Community &#8212; Pitch Coaching", "Work with a 3-person team to build "
     "and pitch projects, and help other teams refine startup ideas.", "[FILL IN: a specific team and "
     "idea you helped refine, and specifically what you contributed &#8212; feedback, restructuring the "
     "pitch, technical framing]", "[FILL IN: what happened to that idea/pitch afterward, if known]",
     "[FILL IN: what you learned about persuasion or technical communication]",
     "Persuasion, communication, collaboration, initiative"),
    ("S9", "Learning Fast &#8212; New Technology for the Aggregation API", "Get productive with "
     "unfamiliar tools (e.g., Kafka, Redis, async processing patterns) fast enough to use them "
     "correctly in the system.", "[FILL IN: which specific technology was newest to you, and how you "
     "actually learned it &#8212; docs, a small prototype, trial and error]",
     "[FILL IN: evidence you actually understood it &#8212; a decision you could defend, a bug you "
     "could diagnose]", "[FILL IN: what you'd do differently next time you need to ramp up fast]",
     "Curiosity, learning agility, initiative, technical communication"),
    ("S10", "TEMPLATE &#8212; A Genuine Failure or Mistake", "[FILL IN: what you were responsible for]",
     "[FILL IN: what specifically went wrong, and how you found out]",
     "[FILL IN: what you did once you knew, and what actually happened afterward]",
     "[FILL IN: what you changed about how you work as a result]",
     "Failure and learning, accountability, ownership, coachability"),
    ("S11", "TEMPLATE &#8212; A Real Disagreement With a Person", "[FILL IN: the shared goal you and "
     "the other person both had]", "[FILL IN: what you each believed and why]",
     "[FILL IN: how the disagreement actually got resolved, or didn't]",
     "[FILL IN: what you learned about handling disagreement]",
     "Conflict resolution, communication, dealing with disagreement, emotional maturity"),
    ("S12", "TEMPLATE &#8212; Feedback You Received and Acted On", "[FILL IN: who gave the feedback and "
     "in what context]", "[FILL IN: the feedback itself, as close to their actual words as possible]",
     "[FILL IN: the specific thing you did differently afterward]",
     "[FILL IN: evidence the change actually stuck or helped]",
     "Coachability, self-awareness, adaptability"),
]

make_table(
    ["Story", "Task", "Actions", "Result", "Lesson", "Competencies"],
    [[f"<b>{sid}</b><br/>{title}", task, actions, result, lesson, comps]
     for (sid, title, task, actions, result, lesson, comps) in story_rows],
    [1.25*inch, 1.35*inch, 1.25*inch, 1.05*inch, 1.15*inch, 1.35*inch],
    font_size=7.6,
)

# ================================================================ PART 4 ===
PART(4, "Story Coverage Matrix",
     "You don't need 50 stories. These 12 rows, used flexibly, cover nearly every competency.")

P("Read the matrix by competency (column), not just by story (row): if a question targets "
  "'Leadership', scan down that column for a filled cell, then pick whichever story best fits the "
  "specific wording of the question. A cell marked with a dash means that story isn't a natural fit "
  "for that competency &#8212; don't force it.", "Body")

matrix_comps_full = ["Leadership", "Conflict", "Failure", "Technical", "Teamwork", "Learning",
                     "Pressure", "Ownership", "AI Judgment"]
matrix_comps = ["Lead", "Conf", "Fail", "Tech", "Team", "Lrn", "Pres", "Own", "AI"]
matrix_data = {
    "S1 LedgerCore Concurrency": ["-", "-", "-", "H", "-", "M", "-", "H", "-"],
    "S2 Rejecting AI Suggestion": ["-", "L", "-", "H", "-", "M", "-", "H", "H"],
    "S3 Provider Failures": ["-", "-", "-", "H", "L", "M", "M", "M", "-"],
    "S4 Duplicate Prevention": ["-", "-", "L", "H", "-", "M", "-", "H", "-"],
    "S5 Kafka/Redis Tradeoff": ["-", "-", "-", "H", "L", "M", "-", "M", "-"],
    "S6 FarmLink Hackathon": ["M", "-", "-", "M", "H", "M", "H", "M", "-"],
    "S7 Robotics Training Lead": ["H", "-", "-", "M", "H", "M", "-", "M", "-"],
    "S8 KNUST CS Pitch Coaching": ["M", "L", "-", "L", "H", "M", "-", "L", "-"],
    "S9 Learning Fast": ["-", "-", "-", "M", "-", "H", "M", "L", "-"],
    "S10 Failure (template)": ["-", "-", "H", "?", "-", "H", "-", "H", "-"],
    "S11 Disagreement (template)": ["-", "H", "-", "?", "M", "M", "-", "-", "-"],
    "S12 Feedback (template)": ["-", "-", "-", "-", "-", "H", "-", "-", "-"],
}
rows = [[k] + v for k, v in matrix_data.items()]
make_table(["Story"] + matrix_comps, rows,
           [1.55*inch] + [0.655*inch]*9, font_size=8)
P("Columns: " + ", ".join(f"<b>{a}</b>={f}" for a, f in zip(matrix_comps, matrix_comps_full)),
  "BodySmall")
P("<b>H</b> = strong fit &#160;&#160; <b>M</b> = moderate/secondary fit &#160;&#160; "
  "<b>L</b> = light/possible fit &#160;&#160; <b>-</b> = not a natural fit &#160;&#160; "
  "<b>?</b> = depends entirely on which real incident you fill in.", "BodySmall")

# ================================================================ PART 5 ===
PART(5, "The Story Card System",
     "Full working cards for all 12 stories. Practice talking through these points out loud, in your "
     "own words, in a different order each time. Never read one aloud verbatim &#8212; that's the one "
     "thing that turns a real story into a script.")

def render_story_card(c):
    keep([
        HRFlowable(width="100%", thickness=1.4, color=NAVY, spaceBefore=2, spaceAfter=6),
        Paragraph(f"{c['id']} &#8212; {c['title']}", styles["H2"]),
        Paragraph(f"<i>One-sentence version:</i> {c['one_sentence']}", styles["BodySmall"]),
    ])
    card_label("BLUF (say this first)")
    P(c["bluf"], "Body")
    card_label("Situation (only the context needed)")
    P(c["situation"], "Body" if not c.get("situation_ph") else "Placeholder")
    card_label("Task (my responsibility)")
    P(c["task"], "Body" if not c.get("task_ph") else "Placeholder")
    card_label("Actions (what I personally did)")
    bullets(c["actions"], "Placeholder" if c.get("actions_ph") else "Bullet")
    card_label("Result")
    P(c["result"], "Body" if not c.get("result_ph") else "Placeholder")
    card_label("Metrics")
    P(c["metrics"], "Placeholder" if c.get("metrics_ph", True) else "Body")
    card_label("What I learned")
    P(c["learned"], "Body" if not c.get("learned_ph") else "Placeholder")
    card_label("What I'd do differently")
    P(c["differently"], "Body" if not c.get("differently_ph") else "Placeholder")
    card_label("Competencies demonstrated")
    P(", ".join(c["competencies"]), "BodySmall")
    card_label("Technical depth available if asked")
    P(c["tech_depth"], "BodySmall")
    card_label("Likely follow-up questions")
    bullets(c["followups"], "Bullet")
    SP(10)

STORY_CARDS = [
    dict(id="S1", title="LedgerCore &#8212; Concurrent Transfer Consistency",
        one_sentence="I found and closed a consistency risk in how LedgerCore handled simultaneous "
        "transfers, and proved the fix with concurrent load tests rather than just code review.",
        bluf="The core risk was that two concurrent transfer requests touching the same account could "
        "interleave in a way that broke double-entry consistency; I addressed it with transaction "
        "isolation, idempotency keys, and retry logic, then validated it under real concurrent load.",
        situation="LedgerCore is a FastAPI + PostgreSQL double-entry ledger and settlement system. "
        "Double-entry means every transfer has to debit one account and credit another as a single "
        "atomic fact &#8212; if that ever gets out of sync, the ledger is no longer trustworthy.",
        task="My responsibility was to make sure the transfer path stayed correct when multiple "
        "transfers hit the same account at the same time, not just when tested one request at a time.",
        actions=[
            "Reasoned through what could go wrong when two requests for the same account overlapped "
            "&#8212; specifically around transaction isolation level and double-processing on retries.",
            "Implemented idempotency keys so a retried request couldn't be applied twice.",
            "Used database-level transaction isolation and locking so concurrent writes to the same "
            "account couldn't interleave incorrectly.",
            "Added retry logic for the cases where a transaction had to legitimately be retried after "
            "a conflict, rather than assuming the first attempt always succeeds.",
            "[FILL IN: any specific bug or near-miss you found while doing this &#8212; a real detail "
            "makes this concrete under follow-up questions]",
            "Built and ran concurrent stress tests specifically designed to hit the same accounts from "
            "multiple simultaneous transfers, rather than relying on single-request tests.",
        ],
        result="[FILL IN: what the stress tests actually showed &#8212; did they catch a real issue, "
        "confirm the fix held, at what concurrency level did you test]",
        metrics="[FILL IN: real numbers if you have them &#8212; number of concurrent transfers tested, "
        "pass rate, any latency numbers. If you don't have exact numbers, say 'No verified metric "
        "available' rather than estimating.]",
        learned="Code that looks correct reading it top to bottom can still be wrong under concurrency "
        "&#8212; the only way to be confident is to actually generate concurrent load and watch what "
        "happens, not just reason about it.",
        differently="[FILL IN: e.g., would you design the stress tests earlier, log more state during "
        "testing, or something else specific]",
        competencies=["Problem solving", "Ownership", "Attention to quality", "Technical communication",
                      "Decision-making", "Curiosity"],
        tech_depth="Can discuss: PostgreSQL transaction isolation levels, why double-entry accounting "
        "requires atomicity, idempotency key design, retry-after-conflict logic, how the stress test "
        "was structured.",
        followups=[
            "Why idempotency keys specifically, instead of just relying on database locks?",
            "What transaction isolation level did you use, and why that one instead of a stricter or "
            "looser one?",
            "How did you generate concurrent load for the stress test?",
            "What would happen if two retries of the same request arrived out of order?",
            "How did you know the fix actually worked, versus just not seeing a failure in your test run?",
            "What's the worst case if this bug had shipped to production?",
            "Did you consider using a queue to serialize writes per account instead?",
            "How long did it take you to find this, and what made you look for it in the first place?",
        ]),
    dict(id="S2", title="LedgerCore &#8212; Rejecting an AI Suggestion That Would Have Masked a Bug",
        one_sentence="An AI coding assistant suggested a change that would have made a symptom disappear "
        "without fixing the underlying data problem, and I rejected it in favor of finding the actual "
        "root cause.",
        bluf="The AI's suggestion would have suppressed an error rather than fixing what caused it, "
        "which in a ledger system would have let bad data pass silently; I traced the real cause "
        "instead and fixed that.",
        situation="I was using an AI coding assistant to speed up development on LedgerCore. At one "
        "point it proposed a fix for an issue I was working through.",
        situation_ph=True,
        task="My responsibility was to make sure whatever went into LedgerCore was actually correct, "
        "not just quiet &#8212; especially since this is a financial ledger where a silently-swallowed "
        "error can mean data that looks fine but isn't.",
        actions=[
            "[FILL IN: what the AI actually suggested &#8212; e.g., catching/suppressing an exception, "
            "adding a default value, skipping a check]",
            "Recognized that the suggestion would remove the symptom (an error or failure) without "
            "addressing why the error was happening in the first place.",
            "Rejected the suggestion rather than accepting it because it was fast or because it made "
            "the immediate problem go away.",
            "[FILL IN: how you actually traced the real root cause &#8212; what you looked at, what you "
            "found]",
            "Implemented a fix that addressed the actual cause instead of the symptom.",
            "[FILL IN: how you verified the real fix, e.g., tests, manual verification]",
        ],
        actions_ph=True,
        result="[FILL IN: what the real root cause turned out to be, and what changed once it was fixed "
        "properly]",
        result_ph=True,
        metrics="No verified metric available unless you have a specific before/after data point (e.g., "
        "a specific class of bad records that stopped appearing).",
        learned="AI-assisted development speeds up writing code, but it doesn't understand the "
        "system's actual invariants (in this case, what 'correct' means for a ledger) &#8212; that "
        "judgment still has to come from me.",
        differently="[FILL IN, optional]",
        competencies=["Responsible use of AI", "Attention to quality", "Ownership", "Technical judgment",
                      "Curiosity", "Decision-making"],
        tech_depth="Can discuss: what the AI suggested, why it would have masked rather than fixed the "
        "issue, how you found the real cause, and generally how you validate AI-generated suggestions "
        "in a system where correctness matters (financial/ledger data).",
        followups=[
            "What exactly did the AI suggest?",
            "How did you know it was masking the problem rather than actually fixing it?",
            "What was the real root cause?",
            "How long did it take you to find the real fix compared to just accepting the AI's answer?",
            "Do you usually accept AI suggestions, or do you check all of them this closely?",
            "How do you decide when to trust an AI suggestion versus dig deeper?",
            "Has an AI tool ever given you a suggestion that you accepted and later regretted?",
            "What's your general process for reviewing AI-generated code before it goes in?",
        ]),
    dict(id="S3", title="Aggregation API &#8212; Provider Failures and Rate Limiting",
        one_sentence="I designed how the account aggregation system handled a bank provider being down "
        "or rate-limiting requests, so one failing provider wouldn't take down account syncing for "
        "everyone.",
        bluf="The main risk was that a single mock bank provider failing or rate-limiting could cascade "
        "into failures across the whole sync pipeline; I designed retry/backoff and failure isolation so "
        "one provider's problems stayed contained.",
        situation="The Financial Account Aggregation API (built with FastAPI, PostgreSQL, Redis, and "
        "Kafka) links user accounts to mock bank providers and keeps transaction data in sync with "
        "them. Providers can fail or rate-limit requests, which is realistic behavior for real bank "
        "integrations.",
        task="My responsibility was the account linking and transaction synchronization logic, "
        "including how it behaved when a provider wasn't cooperating.",
        actions=[
            "Identified the specific failure modes to design for: a provider being fully down versus "
            "a provider rate-limiting requests &#8212; these need different handling.",
            "Used retry with backoff for transient failures instead of failing the whole sync "
            "immediately.",
            "Used Redis to track rate-limit state so the system could back off from a specific "
            "provider without needing to hit it again just to find out it was still limiting requests.",
            "Designed the failure handling so one provider's issues were isolated and didn't block "
            "syncing for accounts on other providers.",
            "[FILL IN: how you tested this &#8212; did you simulate provider failure/rate-limiting "
            "against the mock providers, and what did you observe]",
        ],
        result="[FILL IN: concrete outcome &#8212; e.g., sync for unaffected accounts continued "
        "normally during a simulated provider outage, or a specific recovery behavior you observed]",
        metrics="[FILL IN if available: retry counts, backoff intervals used, or number of providers/"
        "accounts in your test setup. Otherwise: No verified metric available.]",
        learned="In a system that talks to external providers, failure handling isn't a nice-to-have "
        "&#8212; it has to be part of the initial design, because provider failure is a normal, "
        "expected condition, not an edge case.",
        differently="[FILL IN, e.g., would you add circuit-breaking, more granular per-provider "
        "metrics, etc.]",
        competencies=["Problem solving", "Tradeoffs", "Adaptability", "Technical communication",
                      "Attention to quality"],
        tech_depth="Can discuss: retry/backoff strategy, why Redis for rate-limit state, failure "
        "isolation between providers, how this interacts with background sync via Kafka.",
        followups=[
            "What's the difference in how you handled a total outage versus a rate limit?",
            "Why Redis for tracking rate-limit state instead of just an in-memory counter?",
            "How did you test provider failure without a real bank to fail?",
            "What happens to a transaction sync that was in progress when a provider started failing?",
            "How would this scale if you had 50 providers instead of a few mock ones?",
            "What would you add if you had another two weeks on this?",
            "How do you decide how long to back off before retrying?",
            "What's the tradeoff between retrying aggressively and giving up too early?",
        ]),
    dict(id="S4", title="Aggregation API &#8212; Preventing Duplicate Transactions in Background Sync",
        one_sentence="I closed a path where background transaction synchronization could record the "
        "same transaction twice, by deliberately designing for duplicate prevention rather than "
        "assuming sync would only ever run once per transaction.",
        bluf="Background sync jobs can retry or overlap, and without explicit dedup logic that risks "
        "double-recording transactions; I designed the sync path so repeated or overlapping runs "
        "couldn't create duplicates.",
        situation="The Aggregation API synchronizes transaction data from linked bank accounts in the "
        "background, which means sync jobs can be retried (e.g., after a provider or network hiccup) "
        "or can potentially overlap.",
        task="My responsibility was making sure that a transaction that had already been recorded "
        "wouldn't get recorded again just because the job that fetched it ran more than once.",
        actions=[
            "Identified the specific ways a duplicate could enter the system: retried sync jobs, "
            "provider responses being replayed, or overlapping sync windows.",
            "Designed a deduplication approach based on stable transaction identifiers rather than "
            "relying on sync-run timing to avoid overlap.",
            "[FILL IN: the specific mechanism &#8212; e.g., a uniqueness constraint at the database "
            "level, a dedup check before insert, or both]",
            "Tested by deliberately re-running sync against the same data to confirm it didn't create "
            "duplicate records.",
        ],
        result="[FILL IN: what you observed when you tested repeated sync runs &#8212; did duplicates "
        "stop appearing, how did you confirm]",
        metrics="[FILL IN if available: number of duplicate records before the fix versus after, or "
        "number of repeated-sync test runs performed. Otherwise: No verified metric available.]",
        learned="'Exactly-once' processing doesn't happen by accident in a background/distributed "
        "system &#8212; it requires an explicit identifier and check, because retries and overlaps are "
        "a normal part of how these systems behave.",
        differently="[FILL IN, optional]",
        competencies=["Attention to quality", "Problem solving", "Ownership", "Debugging"],
        tech_depth="Can discuss: what made a transaction identifier stable enough to dedup on, where "
        "the dedup check lived (application layer vs. database constraint), how this interacts with "
        "retries from the provider-failure handling in S3.",
        followups=[
            "What made a transaction's identifier reliable enough to dedup on?",
            "Did you enforce this at the database level, the application level, or both, and why?",
            "How did you first notice duplicates were even possible?",
            "What would happen if the provider itself sent the same transaction with two different "
            "IDs?",
            "How does this interact with the retry logic from provider failures?",
            "How did you test this without waiting for a real duplicate to occur naturally?",
            "What's the performance cost of the dedup check, if any?",
            "Is this a bug you found, or a risk you designed against before it happened?",
        ]),
    dict(id="S5", title="Aggregation API &#8212; Kafka/Redis Architecture Tradeoff",
        one_sentence="I evaluated using Kafka for background/event-driven processing and Redis for "
        "caching and rate-limit state against simpler alternatives, and chose based on what the system "
        "actually needed rather than defaulting to the most popular tools.",
        bluf="The decision came down to whether background transaction processing needed to be "
        "decoupled and event-driven or could stay simpler and synchronous; given multiple providers "
        "and background sync requirements, I chose Kafka plus Redis over a simpler in-process approach.",
        situation="The Aggregation API needed to process account linking, transaction sync, and "
        "background jobs across multiple mock providers, with data normalization and rate-limit "
        "awareness in the mix.",
        task="Part of my responsibility was deciding how background processing and caching should be "
        "architected, not just implementing whatever was already decided.",
        actions=[
            "Considered a simpler alternative: handling background work with, e.g., in-process "
            "background tasks or a simple job queue, without a message broker.",
            "Weighed that against Kafka, which decouples producers (things that trigger sync) from "
            "consumers (the workers doing the syncing) and handles backpressure and replay more "
            "naturally.",
            "Chose Kafka for background/event-driven processing because of the decoupling and "
            "resilience benefits given multiple providers and retryable failures (see S3/S4).",
            "Chose Redis specifically for caching and rate-limit/state tracking because it's fast for "
            "that kind of ephemeral, frequently-read state, not for durable storage.",
            "[FILL IN: any specific moment where the simpler alternative was seriously on the table "
            "and you had to justify the more complex choice]",
        ],
        result="[FILL IN: how the architecture performed once built &#8212; did it hold up under your "
        "testing, did the decoupling actually pay off in a concrete way]",
        metrics="No verified metric available unless you have a specific comparison (e.g., a load test "
        "comparing the two approaches). It's fine to say so directly if asked.",
        learned="Choosing infrastructure should start from the failure modes and throughput needs you "
        "actually expect, not from which tool is most interesting to use &#8212; complexity has to earn "
        "its place.",
        differently="[FILL IN, e.g., would you introduce Kafka this early again, or start simpler and "
        "add it later]",
        competencies=["Decision-making", "Tradeoffs", "Technical communication", "Handling ambiguity"],
        tech_depth="Can discuss: what Kafka buys you over a simple queue (decoupling, replay, "
        "backpressure), why Redis rather than an in-process cache, how PostgreSQL fits as the system "
        "of record versus Kafka/Redis as processing/caching layers.",
        followups=[
            "What would you have lost by not using Kafka?",
            "At what point would the simpler alternative have actually been the better choice?",
            "How do Kafka and Redis divide responsibilities in your design?",
            "What's the failure mode if Redis goes down? What about Kafka?",
            "Was this your decision alone, or a team decision — what was your specific input?",
            "How would you explain this tradeoff to a non-technical stakeholder?",
            "What's the operational cost of running Kafka that a simpler approach wouldn't have?",
            "If you were rebuilding this today, would you make the same choice?",
        ]),
    dict(id="S6", title="FarmLink &#8212; Youth Arise Hackathon (Team Nova, won)",
        one_sentence="As part of Team Nova, I helped build FarmLink under hackathon time pressure, and "
        "the team won.",
        bluf="[FILL IN: your one-line summary of the biggest challenge and how the team/you solved it "
        "&#8212; e.g., 'The biggest challenge was X, and I solved it by Y']",
        bluf_ph=True,
        situation="FarmLink was built as part of the Youth Arise hackathon, by Team Nova, under normal "
        "hackathon time constraints.",
        task="[FILL IN: your specific role on the team &#8212; e.g., which part of the product you "
        "owned, whether you focused on backend, frontend, pitching, or a mix]",
        task_ph=True,
        actions=[
            "[FILL IN: the specific technical or product work you personally did]",
            "[FILL IN: any decision you personally pushed for or made under time pressure]",
            "[FILL IN: how you coordinated with the rest of Team Nova &#8212; division of labor, how "
            "you kept the team on schedule]",
            "[FILL IN: how the team prepared and delivered the final presentation/pitch, and your part "
            "in it]",
        ],
        actions_ph=True,
        result="Team Nova won the hackathon.",
        result_ph=False,
        metrics="[FILL IN: any real numbers &#8212; team size, number of teams competed against, "
        "hackathon duration, judging criteria if known. Otherwise: No verified metric available beyond "
        "the win itself.]",
        learned="[FILL IN: your real takeaway &#8212; e.g., about working under time pressure, about "
        "team coordination, about scoping ambition to time available]",
        learned_ph=True,
        differently="[FILL IN, optional]",
        competencies=["Teamwork", "Time management", "Working under pressure", "Prioritization",
                      "Adaptability", "Communication"],
        tech_depth="[FILL IN: what tech stack FarmLink actually used, and one or two technical "
        "decisions you can defend in detail]",
        followups=[
            "What exact problem was FarmLink solving?",
            "What was your specific role versus the rest of Team Nova's?",
            "What did you personally build or decide?",
            "What did you have to cut or simplify because of the time limit?",
            "What was the biggest risk to finishing in time, and how did you manage it?",
            "How did the team divide the work?",
            "What made your submission win, in your view?",
            "What would you build next if you kept working on FarmLink after the hackathon?",
        ]),
    dict(id="S7", title="Robotics Club &#8212; Training Lead and Programmer",
        one_sentence="As Training Lead, I was responsible for helping other members build technical "
        "skill, while also contributing as a programmer on the club's own projects.",
        bluf="[FILL IN: e.g., 'The biggest challenge was getting new members from zero programming "
        "background to being able to contribute, and I solved it by...']",
        bluf_ph=True,
        situation="I served as Training Lead and Programmer in the Robotics Club, meaning I had a "
        "dual role: developing other members' skills and doing hands-on programming work myself.",
        task="[FILL IN: the specific scope of the Training Lead responsibility &#8212; how many "
        "members, what skill level they started at, what they needed to learn]",
        task_ph=True,
        actions=[
            "[FILL IN: what training/teaching structure you actually built &#8212; sessions, a "
            "curriculum, pairing people up, hands-on exercises]",
            "[FILL IN: a specific member or group you helped and how]",
            "[FILL IN: how you balanced training responsibilities with your own programming "
            "contributions]",
            "[FILL IN: how you checked whether the training was actually working, rather than assuming "
            "it was]",
        ],
        actions_ph=True,
        result="[FILL IN: an observable outcome &#8212; members who became able to contribute "
        "independently, a competition result, a project the club shipped]",
        result_ph=True,
        metrics="[FILL IN: number of members trained, timeframe, competition placement if any. "
        "Otherwise: No verified metric available.]",
        learned="[FILL IN: what you learned about teaching, mentoring, or leading that you didn't "
        "know before taking this role]",
        learned_ph=True,
        differently="[FILL IN, optional]",
        competencies=["Leadership", "Mentoring", "Communication", "Teamwork", "Initiative"],
        tech_depth="[FILL IN: what technical material you were actually teaching &#8212; e.g., a "
        "programming language, robotics-specific concepts, hardware/software integration]",
        followups=[
            "How did you structure your training sessions?",
            "How did you handle members who were struggling to keep up?",
            "What was the hardest part of teaching something you already understood well yourself?",
            "How did you measure whether the training was effective?",
            "Tell me about a specific member you helped improve.",
            "How did you balance being 'Training Lead' with your own programming work?",
            "What would you change about how you ran training if you did it again?",
            "Did you ever get pushback or disagreement from a member about your approach?",
        ]),
    dict(id="S8", title="KNUST CS Open Source Community &#8212; Pitch Coaching",
        one_sentence="Working with a team of three, I helped build and pitch projects, and helped other "
        "teams refine their startup ideas and pursue outside opportunities.",
        bluf="[FILL IN: e.g., 'The biggest challenge was getting a team's pitch to actually explain the "
        "problem clearly, and I solved it by...']",
        bluf_ph=True,
        situation="Within the KNUST CS Open Source Community, I worked as part of a 3-person team on "
        "our own projects, and separately helped other teams sharpen their startup ideas and pitches.",
        task="[FILL IN: your specific role &#8212; were you doing technical work, pitch coaching, or "
        "both; which team(s) you helped]",
        task_ph=True,
        actions=[
            "[FILL IN: a specific project you and your 3-person team built and pitched]",
            "[FILL IN: a specific instance of helping another team refine their idea &#8212; what was "
            "unclear about their original idea/pitch, and what you suggested]",
            "[FILL IN: how you communicated feedback to a team that wasn't yours &#8212; how you made "
            "sure it landed well]",
            "[FILL IN: any follow-through &#8212; did you help them pursue a specific external "
            "opportunity]",
        ],
        actions_ph=True,
        result="[FILL IN: what happened to the idea/pitch after your involvement, if known]",
        result_ph=True,
        metrics="[FILL IN: number of teams helped, outcome of any external opportunity pursued. "
        "Otherwise: No verified metric available.]",
        learned="[FILL IN: what you learned about communication, persuasion, or technical framing from "
        "doing this repeatedly across different teams]",
        learned_ph=True,
        differently="[FILL IN, optional]",
        competencies=["Persuasion", "Communication", "Collaboration", "Initiative"],
        tech_depth="[FILL IN: what your own 3-person team actually built &#8212; stack and your role "
        "in it]",
        followups=[
            "What was the actual project your 3-person team built?",
            "What was your specific contribution versus your two teammates'?",
            "Tell me about one specific team you helped refine their pitch — what changed?",
            "How do you give feedback on someone else's idea without discouraging them?",
            "What made a pitch weak in the cases you saw, most often?",
            "Did any team push back on your feedback? How did you handle that?",
            "What outside opportunity did a team pursue, and what came of it?",
            "How is coaching someone else's idea different from pitching your own?",
        ]),
    dict(id="S9", title="Learning Fast &#8212; New Technology for the Aggregation API",
        one_sentence="I had to get productive quickly with technology that was new to me (e.g., Kafka, "
        "Redis, or async processing patterns) in order to build the Aggregation API correctly.",
        bluf="[FILL IN: e.g., 'The biggest challenge was understanding X well enough to make a real "
        "design decision, not just copy an example, and I solved it by...']",
        bluf_ph=True,
        situation="Building the Financial Account Aggregation API required using technology I hadn't "
        "necessarily worked with in depth before &#8212; [FILL IN: name the specific one, e.g., Kafka, "
        "Redis, or async background processing patterns].",
        situation_ph=True,
        task="I needed to understand the tool well enough to make real design decisions with it (see "
        "S5), not just get a tutorial example running.",
        actions=[
            "[FILL IN: how you actually learned it &#8212; official docs, a specific tutorial, reading "
            "source/examples, a small throwaway prototype before using it for real]",
            "[FILL IN: a specific concept that was initially confusing and how you worked through it]",
            "Validated understanding by using the tool to make an actual design decision (see S5) "
            "rather than just getting it to run.",
            "[FILL IN: how you checked your own understanding &#8212; e.g., could you explain why a "
            "particular configuration/pattern was needed, could you predict a failure mode]",
        ],
        actions_ph=True,
        result="[FILL IN: evidence you actually understood it, not just used it &#8212; e.g., you could "
        "debug an issue with it, or justify a design choice using it]",
        result_ph=True,
        metrics="No verified metric available unless you have a specific timeframe (e.g., 'went from "
        "no experience with Kafka to using it correctly in the sync pipeline within [FILL IN "
        "timeframe]').",
        learned="[FILL IN: what your actual process is for learning a new technology fast &#8212; e.g., "
        "build something small and real before trusting yourself to use it in the main system]",
        learned_ph=True,
        differently="[FILL IN, optional]",
        competencies=["Curiosity", "Learning agility", "Initiative", "Technical communication"],
        tech_depth="[FILL IN: specific technical details about the technology you learned &#8212; "
        "enough to answer a follow-up question about how it actually works]",
        followups=[
            "What was the hardest part to understand at first?",
            "How did you know you understood it well enough to use it for real, not just copy an "
            "example?",
            "What resource or approach worked best for you when learning it?",
            "Did you make a mistake early on because you didn't fully understand it yet?",
            "How long did it take before you felt confident with it?",
            "How do you generally approach learning something you've never used before, under a "
            "deadline?",
            "What would you tell someone else on your team who had to learn this same thing?",
            "Is there a concept related to this tool you still don't fully understand?",
        ]),
    dict(id="S10", title="TEMPLATE &#8212; A Genuine Failure or Mistake",
        one_sentence="[FILL IN once completed]",
        bluf="[FILL IN: 'The mistake was X, it happened because Y, and here's what I changed.']",
        bluf_ph=True,
        situation="[FILL IN: what you were working on and what your responsibility was at the time]",
        situation_ph=True,
        task="[FILL IN: specifically what you were supposed to deliver or ensure]",
        task_ph=True,
        actions=[
            "[FILL IN: what you actually did that turned out to be wrong, or what you failed to do]",
            "[FILL IN: how and when you found out it had gone wrong &#8212; did you catch it yourself "
            "or did someone else]",
            "[FILL IN: what you did once you knew &#8212; how you fixed or mitigated it]",
            "[FILL IN: who you told, and how you communicated the mistake]",
        ],
        actions_ph=True,
        result="[FILL IN: the actual consequence, honestly stated &#8212; don't minimize it, and don't "
        "claim it 'all worked out perfectly' if it didn't]",
        result_ph=True,
        metrics="No verified metric available until you fill this in with a real incident.",
        learned="[FILL IN: the specific, lasting change to how you work as a result &#8212; not a vague "
        "'I learned to be more careful']",
        learned_ph=True,
        differently="[FILL IN: what you'd do differently if you were back at the start of that "
        "situation]",
        differently_ph=True,
        competencies=["Failure and learning", "Accountability", "Ownership", "Coachability"],
        tech_depth="[FILL IN once you know which real incident this is]",
        followups=[
            "What exactly went wrong?",
            "How did you find out?",
            "Whose fault was it, in your honest assessment?",
            "What was the actual impact?",
            "What did you do in the first hour/day after realizing it?",
            "Has anything like this happened again since?",
            "What would you do differently if you saw the early warning signs again?",
            "How did the people around you react?",
        ]),
    dict(id="S11", title="TEMPLATE &#8212; A Real Disagreement With Another Person",
        one_sentence="[FILL IN once completed]",
        bluf="[FILL IN: 'We disagreed about X; I believed Y because Z, they believed otherwise, and "
        "here's how it resolved.']",
        bluf_ph=True,
        situation="[FILL IN: the shared project or goal you and the other person were both working "
        "toward]",
        situation_ph=True,
        task="[FILL IN: what decision or approach was actually in dispute]",
        task_ph=True,
        actions=[
            "[FILL IN: what you believed and why, stated fairly]",
            "[FILL IN: what the other person believed and why &#8212; stated fairly, not as a strawman]",
            "[FILL IN: what you actually did to work through it &#8212; did you listen first, bring "
            "evidence, propose a compromise, escalate]",
            "[FILL IN: how it was actually resolved &#8212; who was right, or was it a compromise]",
        ],
        actions_ph=True,
        result="[FILL IN: the actual outcome, and the state of the relationship afterward]",
        result_ph=True,
        metrics="No verified metric available until you fill this in with a real incident.",
        learned="[FILL IN: what you learned about handling disagreement specifically from this "
        "situation]",
        learned_ph=True,
        differently="[FILL IN, optional]",
        differently_ph=True,
        competencies=["Conflict resolution", "Communication", "Dealing with disagreement",
                      "Emotional maturity"],
        tech_depth="[FILL IN once you know which real incident this is]",
        followups=[
            "What exactly did you disagree about?",
            "Did you consider that you might be wrong? What made you reconsider, if anything?",
            "How did the other person react to your pushback?",
            "Was this resolved, or did you just agree to disagree?",
            "How did this affect your working relationship afterward?",
            "Would you handle it the same way again?",
            "What would you have done if they outranked you or had more experience?",
            "What's the difference between healthy disagreement and just being difficult?",
        ]),
    dict(id="S12", title="TEMPLATE &#8212; Feedback You Received and Acted On",
        one_sentence="[FILL IN once completed]",
        bluf="[FILL IN: 'I was told X; at first I thought Y, but I changed Z, and here's what happened "
        "after.']",
        bluf_ph=True,
        situation="[FILL IN: who gave you the feedback and in what context &#8212; a code review, a "
        "club leader, a hackathon teammate, a professor]",
        situation_ph=True,
        task="[FILL IN: what you were doing that the feedback was about]",
        task_ph=True,
        actions=[
            "[FILL IN: the feedback itself, as close to their actual words as you can recall]",
            "[FILL IN: your honest initial reaction &#8212; it's fine if it wasn't immediately positive]",
            "[FILL IN: what you specifically did differently afterward]",
            "[FILL IN: how you checked whether the change actually helped]",
        ],
        actions_ph=True,
        result="[FILL IN: evidence the change stuck or made a real difference]",
        result_ph=True,
        metrics="No verified metric available until you fill this in with a real incident.",
        learned="[FILL IN: what this taught you about receiving feedback in general]",
        learned_ph=True,
        differently="[FILL IN, optional]",
        differently_ph=True,
        competencies=["Coachability", "Self-awareness", "Adaptability"],
        tech_depth="[FILL IN once you know which real incident this is]",
        followups=[
            "What was your first reaction when you heard the feedback?",
            "Did you agree with it right away, or did it take time?",
            "What specifically did you change?",
            "How do you know the change actually helped, versus just feeling better about it?",
            "Has anyone given you similar feedback since?",
            "What kind of feedback is hardest for you to hear?",
            "How do you ask for feedback, rather than just waiting to receive it?",
            "Tell me about a time you disagreed with feedback you were given.",
        ]),
]

for c in STORY_CARDS:
    render_story_card(c)

# ================================================================ PART 6 ===
PART(6, "Question &#8594; Story Mapping",
     "For each canonical question: which story to reach for, why, what to actually say, and what "
     "follow-up to expect. This is a starting point, not a rule &#8212; if a question is phrased "
     "slightly differently, use Part 4's matrix to re-pick.")

q6 = [
    ("Tell me about a time you failed.", "Failure and learning", "S10 (fill in first)",
     "A real mistake, honestly owned, with a lasting behavior change afterward.",
     "What would you do differently right now if you saw it happening again?"),
    ("Tell me about a time you disagreed with someone.", "Conflict resolution", "S11 (fill in first) "
     "or S2 (disagreement with an AI suggestion)", "Fair statement of both views; how it was resolved.",
     "Did you ever consider you might be the one who was wrong?"),
    ("Tell me about a time you received difficult feedback.", "Coachability", "S12 (fill in first)",
     "The actual feedback, your honest first reaction, and what specifically changed after.",
     "How do you know the change actually helped?"),
    ("Tell me about a time you demonstrated leadership.", "Leadership", "S7 (Robotics) or S6 (FarmLink)",
     "A concrete action that changed what other people did, not just a title.",
     "What would you do if someone on the team ignored your guidance?"),
    ("Tell me about a time you had to learn something quickly.", "Curiosity / learning agility", "S9",
     "The specific technology, how you actually learned it, and how you validated your own "
     "understanding.", "What's something related you still don't fully understand?"),
    ("Tell me about a difficult technical problem.", "Problem solving", "S1 or S3 or S4",
     "Lead with the BLUF: what the core risk was and how you closed it. Then the diagnostic process.",
     "What alternatives did you consider before landing on this approach?"),
    ("Tell me about a time you worked under pressure.", "Working under pressure", "S6 (FarmLink)",
     "The real deadline/stakes, and how you kept quality up rather than just rushing.",
     "What did you have to cut or simplify because of the pressure?"),
    ("Tell me about a time you had competing priorities.", "Prioritization", "S6 or S9",
     "Name the competing items explicitly and the criteria you used to choose.",
     "What happened to the thing you deprioritized?"),
    ("Tell me about a time you persuaded someone.", "Persuasion", "S8",
     "The other person's starting position, your evidence/argument, and what actually changed.",
     "What if they still hadn't agreed after that?"),
    ("Tell me about a time you made a mistake.", "Accountability", "S10 (fill in first)",
     "Explicit ownership language; don't let the sentence drift into passive voice.",
     "What was the actual impact, in concrete terms?"),
    ("Tell me about a time you disagreed with a teammate.", "Conflict resolution", "S11 (fill in first)",
     "Same as 'disagreed with someone' &#8212; keep the other person's view fair and reasonable.",
     "How is your relationship with them now?"),
    ("Tell me about a time you had to explain something technical.", "Technical communication", "S3 "
     "or S5", "Start with the plain-language version; add technical depth only if they ask for it.",
     "How would you explain the same thing to an engineer instead?"),
    ("Tell me about a time you took initiative.", "Initiative", "S8 or S9",
     "The gap you noticed that nobody assigned you to fix, and the specific unprompted action.",
     "Did anyone tell you not to, or was it outside your role?"),
    ("Tell me about a time something did not go according to plan.", "Adaptability", "S3 or S6",
     "What changed, what you adjusted, and why that adjustment was reasonable at the time.",
     "How did you know your adjustment was the right one and not just a guess?"),
    ("Tell me about a time you had to make a difficult decision.", "Decision-making", "S1 or S5",
     "Real alternatives you seriously considered, not a strawman; the deciding factor.",
     "What information did you wish you'd had before deciding?"),
    ("Tell me about a time you received feedback.", "Coachability", "S12 (fill in first)",
     "Feedback &#8594; reflection &#8594; behavior change &#8594; result, in that order.",
     "What's feedback you've been given more than once?"),
    ("Tell me about a time you helped someone else.", "Teamwork / mentoring", "S7",
     "What the person couldn't do before, what you did, what they could do after.",
     "How did you know they actually needed help, versus assuming?"),
    ("Tell me about a time you had limited resources.", "Prioritization / adaptability", "S6",
     "The specific constraint (time, people, tools) and how it shaped your approach.",
     "What would you have built with no constraint at all?"),
    ("Tell me about a time you had to adapt.", "Adaptability", "S3 or S6",
     "Same guidance as 'didn't go according to plan' &#8212; needs a real forced change.",
     "How long did it take you to realize the original plan wasn't working?"),
    ("Tell me about a time you had to prioritize.", "Prioritization", "S6 or S9",
     "Same guidance as 'competing priorities'.", "Would you make the same call again?"),
]
make_table(["Question", "Primary competency", "Recommended story", "Key points to hit", "Expect this "
            "follow-up"], q6, [1.55*inch, 0.85*inch, 1.05*inch, 2.1*inch, 1.35*inch], font_size=7.2)

# ================================================================ PART 7 ===
PART(7, "Deep Prep on the Highest-Stakes Questions",
     "These get asked in almost every interview. Each section is a framework and a fill-in skeleton "
     "&#8212; not a script. Practice saying it differently each time.")

H2("1. Tell me about yourself")
P("Target length: 60&#8211;90 seconds. Structure: who you are &#8594; what you're studying and "
  "building &#8594; what technical area genuinely interests you &#8594; what shaped that interest "
  "&#8594; what you're looking for next. Don't narrate your life story chronologically &#8212; pull "
  "out only the pieces that explain why you're in this interview.", "Body")
bullets([
    "<b>Who I am:</b> [FILL IN: your name, program, year at KNUST]",
    "<b>What I build:</b> backend systems &#8212; e.g., \"I've been building backend systems like a "
    "financial account aggregation API and a double-entry ledger system, working with FastAPI, "
    "PostgreSQL, Redis, and Kafka.\"",
    "<b>What draws me to that area:</b> [FILL IN: e.g., the part of backend engineering that "
    "genuinely interests you &#8212; correctness under concurrency, system design, data integrity]",
    "<b>What shaped that interest:</b> one concrete anchor &#8212; e.g., \"working on LedgerCore is "
    "what got me interested in [FILL IN: specific sub-area]\"",
    "<b>What I'm looking for:</b> [FILL IN: e.g., an internship where you can work on real systems "
    "with engineers more experienced than you, and get feedback that sharpens your judgment]",
])
note("Do not build this around a childhood story or a fabricated 'always loved computers since I was "
     "5' narrative unless it's literally true. A shorter, accurate answer beats a longer invented one.")

H2("2. Why software engineering / computer science?")
P("Answer from your actual experience, not from a script about 'loving to solve problems.' What "
  "specifically do you enjoy: building something that works end-to-end, debugging something you "
  "don't understand yet until you do, seeing a system hold up under real conditions? Anchor it to "
  "one real moment &#8212; e.g., a specific point in LedgerCore or the Aggregation API where the "
  "work clicked for you.", "Body")
placeholder("your honest answer to: what's the actual moment or realization that made you want to do "
            "this, not the answer you think sounds best")

H2("3. Why this company?")
P("Never say 'your company is innovative and prestigious' &#8212; it's true of every company an "
  "interviewer has ever worked at, so it tells them nothing. Research four things and connect each "
  "to something genuine about you (see Part 17 for the full framework):", "Body")
bullets([
    "What the company actually builds and who uses it.",
    "A specific technology or engineering challenge they're known for.",
    "What the specific team/role does day to day.",
    "What you'd genuinely learn there that you can't get from a class or a solo project.",
])
P("Example structure (fill in real research per company, using Part 17): \"[Company fact] is "
  "interesting to me because I've been working on [related thing from your projects], and I want to "
  "see how that works at a scale / with constraints I haven't dealt with yet.\"", "Body")

H2("4. Why this role?")
P("Connect four things explicitly: your current skills + what you want to learn + what the role "
  "actually involves + why this is a good next step for your development. For an internship, it's "
  "fine &#8212; expected, even &#8212; to say you want mentorship and exposure to real systems, as "
  "long as you also show what you already bring.", "Body")

H2("5. Tell me about a project &#8212; at four depths")
P("Use S1 (LedgerCore) or S3/S5 (Aggregation API). The core content doesn't change across lengths "
  "&#8212; only how much of it you say. Watch the interviewer: if they lean in or ask a follow-up "
  "before you finish, go deeper; if they're just nodding, wrap up.", "Body")
keep([
    Paragraph("30 seconds", styles["H3"]),
    Paragraph("\"LedgerCore is a double-entry ledger system I built with FastAPI and PostgreSQL. The "
        "interesting problem was keeping transfers consistent when multiple ones hit the same account "
        "at once &#8212; I handled that with transaction isolation and idempotency keys, and proved it "
        "with concurrent stress tests.\"", styles["Placeholder"]),
])
keep([
    Paragraph("60 seconds", styles["H3"]),
    Paragraph("Add: what double-entry means and why consistency matters there, what specifically could "
        "go wrong under concurrency, and one sentence on the result of the stress testing.",
        styles["BodySmall"]),
])
keep([
    Paragraph("2 minutes", styles["H3"]),
    Paragraph("Add: the specific mechanism (isolation level, idempotency key design, retry logic), why "
        "you chose that mechanism over an alternative, and what you learned about testing concurrent "
        "systems.", styles["BodySmall"]),
])
keep([
    Paragraph("5 minutes", styles["H3"]),
    Paragraph("Add: the broader system context (how this fits with the rest of LedgerCore), a second "
        "example (e.g., the AI-suggestion story, S2, as a related judgment call), and reflection on "
        "what you'd do differently with more time.", styles["BodySmall"]),
])

H2("6. Tell me about a difficult technical problem")
P("Lead with BLUF, not backstory: \"The core problem was X, and the reason it was hard was Y.\" Then "
  "walk investigation &#8594; hypotheses &#8594; actions &#8594; result &#8594; learning. Use S1, S3, "
  "or S4.", "Body")

H2("7. Tell me about a failure")
note("This is the one question where inventing an answer does the most damage, because a fake "
     "failure sounds fake under any follow-up. Fill in S10 (Part 5) with something real before you "
     "walk into an interview. If you genuinely cannot think of one, that itself is worth reflecting "
     "on honestly (see Part 25) rather than papering over with a fabricated story.")
P("Structure: ownership &#8594; action &#8594; recovery &#8594; learning &#8594; changed behavior. "
  "Do not let the answer resolve into \"but it all worked out great\" &#8212; a real failure has a "
  "real, sometimes still slightly uncomfortable, cost.", "Body")

H2("8. Tell me about a conflict / disagreement")
P("Use S11 once filled in, or S2 (disagreeing with an AI-generated suggestion) if you're not yet "
  "ready with a real interpersonal conflict &#8212; but say so honestly if directly asked for a "
  "person-to-person conflict (see Part 15 for how to bridge that). State the other person's view as "
  "something a reasonable person could hold. Never make them look foolish or malicious.", "Body")

H2("9. Tell me about a time you received feedback")
P("Structure: feedback &#8594; reflection &#8594; behavior change &#8594; result. The interviewer is "
  "not scoring how good the feedback made you feel; they're scoring whether you can point to "
  "something you actually did differently afterward. Use S12 once filled in.", "Body")

H2("10. What is your weakness?")
P("A good weakness answer has five parts: a real, moderate development area; evidence you recognize "
  "it; what you're actively doing about it; evidence of some improvement; what you still want to get "
  "better at. Avoid fake weaknesses ('I work too hard', 'I'm a perfectionist') and avoid weaknesses "
  "that would actually worry an engineering interviewer (e.g., 'I don't test my code').", "Body")
placeholder("a real, moderate weakness from your own experience &#8212; e.g., something like "
            "'I sometimes go deep on a technical rabbit hole before stepping back to check it's worth "
            "the time' only if that is genuinely true for you; otherwise identify your own")
P("Then fill in: <br/>&#8226; Evidence you recognize it: [FILL IN: a specific moment you noticed this "
  "in yourself]<br/>&#8226; What you're doing about it: [FILL IN]<br/>&#8226; Evidence of improvement: "
  "[FILL IN]<br/>&#8226; What you still want to improve: [FILL IN]", "Body")

H2("11. Where do you see yourself in five years?")
P("Show ambition, learning, and increasing responsibility without pretending to know your exact "
  "title. A safe honest shape: \"I want to keep going deeper on [FILL IN: e.g., backend systems and "
  "data correctness], take on more ownership over a system end-to-end, and get to a point where I'm "
  "the one other people come to for [FILL IN: a specific area].\" Avoid over-specific claims like "
  "naming a job title or company you have no real basis for.", "Body")

H2("12. What are you looking for in your next role?")
P("For an internship: learning, mentorship, exposure to real systems and real constraints, and "
  "working alongside engineers more experienced than you. It's fine to say this directly &#8212; "
  "companies hiring interns expect it. Pair it with one concrete thing you already bring (e.g., the "
  "concurrency/reliability work from LedgerCore) so it doesn't sound purely one-directional.", "Body")

# ================================================================ PART 8 ===
PART(8, "Follow-Up Question Training",
     "20 chains. An interviewer rarely stops at your first answer. Practice these chains out loud, "
     "against any story that fits, until answering link 5 feels as easy as answering link 1.")

note("These chains are patterns, not scripts written for a specific story. Pick a story from Part 5 "
     "that fits the chain's theme, then answer each link using that story's real details.")

CHAINS = [
    ("Technical decision chain",
     ["Tell me about a technical problem you faced.", "Why did you choose that approach?",
      "What alternatives did you consider?", "Why didn't you choose the alternative?",
      "What went wrong, if anything, with the approach you did choose?",
      "What did you learn?", "What would you do differently now?",
      "How did you know your solution actually worked?"]),
    ("Root-cause chain",
     ["Tell me about a bug you had to track down.", "What was your first hypothesis?",
      "What told you that hypothesis was wrong?", "What did you check next?",
      "How did you finally confirm the actual cause?", "How did you verify the fix?",
      "How would you prevent this class of bug in the future?"]),
    ("AI-judgment chain",
     ["How do you use AI when you code?", "Tell me about a time an AI suggestion was wrong.",
      "How did you know it was wrong?", "What did you do instead?",
      "How do you generally verify AI-generated code?",
      "Where's the line between using AI as leverage and depending on it?",
      "Has AI ever helped you learn something, versus just producing an answer?"]),
    ("Ownership chain",
     ["Tell me about a time you took ownership of a problem.",
      "Was it technically your responsibility, or did you choose to take it on?",
      "What would have happened if you hadn't?", "Who else was affected?",
      "How did you communicate what you were doing to others?",
      "What did it cost you to take this on (time, tradeoff)?"]),
    ("Failure chain",
     ["Tell me about a time you failed.", "How did you find out it had gone wrong?",
      "What was the actual impact?", "What did you do in the immediate aftermath?",
      "How did the people around you react?", "What did you change afterward?",
      "Has anything similar happened since?"]),
    ("Conflict chain",
     ["Tell me about a disagreement you had.", "What did the other person believe, in their own terms?",
      "Did you consider you might be wrong?", "How was it actually resolved?",
      "How's your relationship with them now?",
      "What would you do differently if it happened again?"]),
    ("Feedback / coachability chain",
     ["Tell me about feedback you received.", "What was your first reaction, honestly?",
      "What did you specifically change?", "How do you know the change helped?",
      "Has anyone given you similar feedback since?",
      "How do you actively ask for feedback, rather than waiting for it?"]),
    ("Leadership chain",
     ["Tell me about a time you led something.", "What made you step into that role?",
      "What specifically did you do that another person on the team couldn't or didn't do?",
      "Did anyone push back on your approach?", "How did you handle someone who was struggling?",
      "What would you do if someone ignored your guidance?"]),
    ("Pressure / deadline chain",
     ["Tell me about working under a tight deadline.", "What was actually at stake if you missed it?",
      "What did you cut or simplify?", "How did you decide what to cut?",
      "Did the quality of your work suffer? Be honest.",
      "What would you do differently with the same deadline again?"]),
    ("Prioritization chain",
     ["Tell me about competing priorities.", "What were the actual options?",
      "What criteria did you use to choose?", "What happened to the thing you didn't prioritize?",
      "Did anyone disagree with your prioritization?", "Would you make the same call again?"]),
    ("Tradeoff / architecture chain",
     ["Tell me about a design decision you made.", "What was the simplest alternative you considered?",
      "Why wasn't the simplest option good enough?", "What did the choice cost you (complexity, time)?",
      "How would this decision change at 10x the scale?", "Who else weighed in, and what was your "
      "specific contribution to the final call?"]),
    ("Learning-under-deadline chain",
     ["Tell me about learning something new quickly.", "What was your process for learning it?",
      "What's a concept you got wrong at first?", "How did you know you finally understood it?",
      "How long did it actually take?", "What would you do differently to learn faster next time?"]),
    ("Quality / correctness chain",
     ["Tell me about a time you caught a bug before it caused a real problem.",
      "What made you look for it in the first place?", "How did you confirm it was real, not a false "
      "alarm?", "How did you fix it?", "How did you make sure it couldn't recur?"]),
    ("Persuasion chain",
     ["Tell me about persuading someone.", "What was their starting position?",
      "What evidence or argument actually changed their mind?", "What if they still hadn't agreed?",
      "How do you know it was genuine agreement and not just them giving in?"]),
    ("Initiative chain",
     ["Tell me about a time you took initiative.", "Whose job was this originally, if anyone's?",
      "What made you decide to act without being asked?", "Did anyone tell you not to?",
      "What was the actual outcome?", "Has that become something you now do regularly?"]),
    ("Ambiguity chain",
     ["Tell me about a time requirements were unclear.", "What assumptions did you make to move "
      "forward?", "How did you validate those assumptions?", "What would you have done if you'd "
      "guessed wrong?", "How do you generally decide when to ask versus when to just proceed?"]),
    ("Scale / impact chain",
     ["Tell me about the impact of something you built.", "How do you know that's the actual impact, "
      "not an assumption?", "What would you measure if you had more visibility into it?",
      "What's the honest, unverified version of this claim if someone pushed on the number?"]),
    ("Mentoring chain",
     ["Tell me about helping someone else improve.", "How did you know they needed help?",
      "What specifically did you do?", "How did you know it was actually helping, versus just being "
      "nice?", "What did you learn about teaching from this?"]),
    ("Disagreeing-up chain",
     ["Tell me about a time you disagreed with someone more experienced than you.",
      "How did you raise it?", "Were you nervous to push back? How did you handle that?",
      "What happened?", "Would you push back the same way again?"]),
    ("Project-depth chain",
     ["Walk me through a project end to end.", "What part did you personally build versus your team?",
      "What was the hardest part technically?", "What would you rebuild if you started over?",
      "What don't you like about it, looking back honestly?"]),
]

for name, chain in CHAINS:
    keep([
        Paragraph(name, styles["H3"]),
        Paragraph(" &#8594; ".join(chain), styles["BodySmall"]),
    ])
    SP(3)

# ================================================================ PART 9 ===
PART(9, "Project-Specific Behavioral Questions",
     "Questions an interviewer may ask specifically about the Aggregation API or LedgerCore, with the "
     "story to reach for. Only speak to what you actually did &#8212; use the [FILL IN] blanks in "
     "Part 5 to prepare specifics before relying on these in a real interview.")

H2("Financial Account Aggregation API")
agg_q = [
    ("Tell me about a difficult decision you made.", "S5 &#8212; Kafka/Redis architecture tradeoff"),
    ("Tell me about a technical mistake.", "S10 if it happened on this project, otherwise be honest "
     "that your clearest mistake example is from elsewhere"),
    ("Tell me about a time you had to learn something quickly.", "S9 &#8212; new tech for this project"),
    ("Tell me about a time you had to debug something.", "S4 &#8212; duplicate transaction debugging"),
    ("Tell me about a time you had competing approaches.", "S5 &#8212; Kafka vs. simpler alternative"),
    ("Tell me about a time you used AI.", "S2 (if it applies to this project) or a general answer per "
     "Part 10"),
    ("Tell me about a time you disagreed with an AI suggestion.", "S2 &#8212; note this happened on "
     "LedgerCore; say so accurately rather than relocating it to this project"),
    ("Tell me about a time you had to balance complexity and simplicity.", "S5"),
    ("Tell me about a time something failed.", "S3 &#8212; provider failure handling (design side) or "
     "S10 if a real failure occurred here"),
    ("Tell me about a time you improved a system.", "S3 or S4 &#8212; closing a resilience or "
     "correctness gap"),
    ("Tell me about a time you had to explain a technical decision.", "S5, told at the depth "
     "appropriate for the audience (Part 7, Q1&#160;'why this approach')"),
    ("Tell me about a time you had to work with uncertainty.", "S5 or S9 &#8212; deciding architecture "
     "or learning a new tool without a clear playbook"),
]
make_table(["Question", "Reach for"], agg_q, [3.6*inch, 3.6*inch], font_size=8)

H2("LedgerCore")
P("Focus areas: concurrency, debugging, failure, AI judgment, testing, ownership, technical "
  "reasoning, reliability.", "Body")
lc_q = [
    ("Tell me about a concurrency problem you solved.", "S1"),
    ("Tell me about a time you had to debug a subtle issue.", "S1 or S2"),
    ("Tell me about a time something failed or almost failed.", "S1 (the risk you found) or S10 if a "
     "real failure occurred here"),
    ("Tell me about a time you disagreed with an AI-generated suggestion.", "S2"),
    ("Tell me about how you test your work.", "S1 &#8212; concurrent stress testing"),
    ("Tell me about a time you took ownership of correctness.", "S1 or S2"),
    ("Tell me about your technical reasoning process for a hard problem.", "S1"),
    ("Tell me about a time you had to validate that something actually worked, not just looked "
     "right.", "S1 &#8212; validating under real concurrent load rather than code review alone"),
]
make_table(["Question", "Reach for"], lc_q, [3.6*inch, 3.6*inch], font_size=8)

# =============================================================== PART 10 ===
PART(10, "Responsible AI Behavioral Questions",
     "Modern engineering roles assume you use AI tools. The organizing principle for every answer in "
     "this section: <b>AI is leverage, not dependency</b> &#8212; you move faster with it, but you "
     "remain personally responsible for correctness, security, testing, and actually understanding "
     "the result.")

ai_q = [
    ("How do you use AI when coding?", "Describe your real, current usage honestly &#8212; e.g., "
     "speeding up boilerplate, exploring an approach, explaining an unfamiliar API &#8212; without "
     "overclaiming fluency you don't have."),
    ("What happens when AI gives you incorrect code?", "Use S2. The short version: you noticed it "
     "would mask a symptom rather than fix a cause, and rejected it in favor of the actual root cause."),
    ("Tell me about a time you disagreed with an AI-generated solution.", "S2, full version (Part 5)."),
    ("How do you verify AI-generated code?", "[FILL IN: your actual practice &#8212; e.g., reading it "
     "line by line before accepting, running it against tests, checking it against your understanding "
     "of the system's invariants]"),
    ("What are the risks of relying on AI?", "It can produce code that runs and looks plausible while "
     "being wrong about the system's actual constraints (as in S2) &#8212; especially dangerous in a "
     "system like a financial ledger where a masked error is worse than a visible one."),
    ("How do you prevent AI from becoming a dependency?", "[FILL IN: your actual habits &#8212; e.g., "
     "trying to solve a problem yourself first, using AI to check your understanding rather than "
     "replace it, being able to explain any code you ship without the AI's help]"),
    ("How do you know when AI's suggestion is wrong?", "By checking it against your own understanding "
     "of what the system actually needs to do (S2) &#8212; not by how confident or fluent the "
     "suggestion sounds."),
    ("Would you use AI to solve an unfamiliar problem?", "Yes, as a starting point for understanding, "
     "the same way you'd use documentation &#8212; but you'd still validate the result yourself (tie "
     "to S9, learning new tech)."),
    ("How do you balance productivity and understanding?", "[FILL IN: your honest answer &#8212; e.g., "
     "using AI for speed on parts you already understand well, and slowing down to learn manually on "
     "parts you don't, so the balance shifts as your own understanding grows]"),
]
for q, a in ai_q:
    keep([Paragraph(q, styles["H3"]), Paragraph(a, styles["BodySmall"])])
    SP(2)
note("Do not exaggerate how much of your work is AI-assisted, and do not claim more verification "
     "process than you actually follow. This is one of the easiest sections to get caught overstating "
     "in a live follow-up.", "HONESTY CHECK")

# =============================================================== PART 11 ===
PART(11, "Impact and Metrics",
     "How to talk about impact honestly &#8212; including when you don't have a clean number.")

H2("My verified metrics")
verified = [
    "Team Nova (FarmLink) won the Youth Arise hackathon &#8212; a verifiable, real outcome.",
    "Role held: Training Lead and Programmer, Robotics Club.",
    "Worked as part of a 3-person team within the KNUST CS Open Source Community.",
    "[FILL IN: any other concrete, checkable fact &#8212; a competition placement, a specific number "
    "of members trained, a specific number of teams coached]",
]
bullets(verified)

H2("Impact statements I need to verify before using them")
P("The following would strengthen your technical stories, but only if the number is real. Go find "
  "or re-derive each one before an interview; if you can't, say so honestly rather than estimating "
  "out loud.", "Body")
tv = [
    ("LedgerCore concurrency", "Exact number of concurrent transfers/requests used in your stress "
     "tests, and the pass/fail outcome."),
    ("LedgerCore reliability", "Any before/after data on the consistency issue you fixed (e.g., "
     "whether you could reproduce it before the fix and not after, across how many runs)."),
    ("Aggregation API dedup", "Number of duplicate records observed before the fix, if any were ever "
     "actually observed, versus after."),
    ("Aggregation API resilience", "Recovery behavior/time under a simulated provider outage in your "
     "own testing."),
    ("Test coverage", "Number of test cases you wrote across either project, if you tracked this."),
    ("FarmLink", "Number of teams competed against, hackathon duration, team size, judging criteria."),
    ("Robotics Club", "Number of members trained, over what timeframe, any measurable change in their "
     "ability."),
    ("KNUST CS community", "Number of teams coached, and outcome of any specific external opportunity "
     "pursued."),
]
make_table(["Area", "What to verify before your interview"], tv, [1.8*inch, 5.4*inch], font_size=8)

H2("How to discuss impact honestly when you don't have an exact number")
P("You don't need a fabricated number &#8212; you need a precise, honest sentence. Use one of these "
  "patterns:", "Body")
bullets([
    "\"I don't have an exact number, but the concrete result was [specific, observable thing that "
    "happened].\"",
    "\"I didn't track that formally &#8212; what I can tell you concretely is [specific test / "
    "observation / before-after behavior].\"",
    "\"That's a fair question &#8212; I'd want to go verify the exact figure rather than guess.\"",
])
note("Never invent a number under follow-up pressure. An interviewer who catches one fabricated "
     "metric will (reasonably) discount every other metric you gave them.")

# =============================================================== PART 12 ===
PART(12, "What Interviewers May Actually Hear",
     "A critical, not flattering, read of each core story: the strong signal, the weak signal, the "
     "red flag, what's missing, and where a follow-up is most likely to expose a gap.")

hear = [
    ("S1 &#8212; LedgerCore concurrency", "Strong: real systems-level correctness reasoning for a "
     "junior candidate.", "Weak: if you can't state a concrete test result, it sounds like design "
     "without proof.", "Red flag: none, if you're honest about what you actually verified.",
     "Missing: the real outcome number/behavior of the stress test.",
     "Vulnerable to: 'how do you know it actually worked' &#8212; have a real answer, not a "
     "hand-wave."),
    ("S2 &#8212; Rejecting an AI suggestion", "Strong: rare, valuable signal of independent technical "
     "judgment.", "Weak: if you can't say specifically what the AI suggested, it sounds generic/"
     "invented.", "Red flag: overclaiming this happens 'all the time' when it may be a single "
     "instance.", "Missing: the specific suggestion and the specific real root cause.",
     "Vulnerable to: 'what exactly did it suggest' &#8212; this is the first thing to fill in."),
    ("S3/S4/S5 &#8212; Aggregation API", "Strong: realistic system design thinking (failure isolation, "
     "dedup, architecture tradeoffs).", "Weak: 'mock bank providers' means this wasn't tested against "
     "real-world chaos &#8212; be ready to say so if asked.", "Red flag: implying this was a production "
     "system with real users, when it's a project with simulated providers.",
     "Missing: concrete test results for the failure/dedup scenarios.",
     "Vulnerable to: 'did real users ever hit this' &#8212; answer honestly that providers were "
     "mocked."),
    ("S6 &#8212; FarmLink hackathon", "Strong: a genuine competitive result (a win) is rare, credible "
     "evidence.", "Weak: currently almost entirely unfilled &#8212; without your specific role, it "
     "reads as 'my team won' rather than 'here's what I contributed to the win'.",
     "Red flag: claiming outsized personal credit for a team win without specifics to back it up.",
     "Missing: your specific actions, and the team's process under time pressure.",
     "Vulnerable to: 'what did you personally build or decide' &#8212; fill this in before relying on "
     "it."),
    ("S7 &#8212; Robotics Club Training Lead", "Strong: a leadership title with real teaching "
     "responsibility is good raw material.", "Weak: currently a title with no described action.",
     "Red flag: describing the title without ever naming something you actually did or someone you "
     "actually helped.", "Missing: a specific member, a specific method, a specific result.",
     "Vulnerable to: 'tell me about one specific person you helped' &#8212; this is the likeliest "
     "follow-up and the card is currently blank there."),
    ("S8 &#8212; KNUST CS community pitch coaching", "Strong: coaching other teams shows persuasion "
     "and communication beyond your own project.", "Weak: currently generic &#8212; 'helped teams "
     "refine ideas' is a description, not a story.", "Red flag: taking credit for another team's idea "
     "or outcome.", "Missing: one specific team, one specific piece of feedback, one specific outcome.",
     "Vulnerable to: 'what changed about their pitch because of you, specifically' &#8212; fill this "
     "in."),
    ("S9 &#8212; Learning fast", "Strong: pairs well with S5 as proof the architecture decision was "
     "actually understood, not copied.", "Weak: 'I learned it from docs' alone is thin.",
     "Red flag: none inherent.", "Missing: which technology specifically, and a concept that was "
     "genuinely hard at first.", "Vulnerable to: 'explain how it actually works' &#8212; make sure "
     "your technical depth here is real, not surface-level."),
]
for row in hear:
    keep([
        Paragraph(row[0], styles["H3"]),
        Paragraph(row[1], styles["BodySmall"]),
        Paragraph(row[2], styles["BodySmall"]),
        Paragraph(row[3], styles["BodySmall"]),
        Paragraph(row[4], styles["BodySmall"]),
        Paragraph(row[5], styles["BodySmall"]),
    ])
    SP(4)

# =============================================================== PART 13 ===
PART(13, "Common Behavioral Mistakes and How to Fix Them")

mistakes = [
    ("Talking too much", "Answer runs past ~2 minutes with no signal the interviewer wants more.",
     "Lead with BLUF, then stop after Situation/Task/Action/Result and let them ask for more."),
    ("Giving excessive context", "5 sentences of backstory before the actual point.",
     "Cut context to only what's needed to understand the decision that follows."),
    ("Using 'we' instead of 'I'", "Interviewer can't tell what you personally did.",
     "Explicitly say 'I decided / I built / I noticed' for your part, 'we' only for genuinely shared "
     "actions."),
    ("Memorizing scripts", "Answer sounds identical word-for-word every time you tell it.",
     "Practice from the bullet points in Part 5, never from a written paragraph."),
    ("Sounding rehearsed", "Flat delivery, no natural pauses, transitions feel canned.",
     "Practice out loud in different orders; use Part 14's natural transition phrases sparingly."),
    ("Giving generic answers", "Answer would be equally true for any candidate.",
     "Anchor every claim to a specific project detail only you would know."),
    ("Not answering the actual question", "Answer is technically related but dodges what was asked.",
     "Restate the question in your own head before answering; if unsure, ask a clarifying question "
     "(Part 14)."),
    ("Blaming teammates", "A conflict or failure story makes someone else look bad.",
     "State the other person's position fairly; own your own part regardless of theirs."),
    ("Making failures sound fake", "The 'failure' is actually a strength ('I care too much').",
     "Use a real mistake with a real, sometimes uncomfortable, cost (Part 5, S10)."),
    ("Avoiding responsibility", "Passive voice hides who was responsible.",
     "Use active 'I' language even when the fact is unflattering."),
    ("Claiming impossible results", "A number or outcome that couldn't plausibly be true for the "
     "scope of the project.", "Scale claims to the actual size of a student/hackathon project."),
    ("Inventing metrics", "A precise-sounding number with no real source.",
     "Use Part 11's honest patterns instead: state what you actually know."),
    ("Giving no measurable result", "Story ends at 'and then it worked' with nothing concrete.",
     "Add at least one observable outcome, even if it's qualitative ('sync continued for other "
     "accounts during the simulated outage')."),
    ("Saying 'I don't know' without demonstrating learning", "A knowledge gap with no follow-through.",
     "Pair 'I don't know' with what you'd do to find out, or what you learned since."),
    ("Turning every answer into a technical explanation", "Human-focused questions (failure, conflict) "
     "get answered with architecture diagrams.", "Match structure to question type (Part 2's "
     "business-vs-human distinction) &#8212; lead with the human reasoning first."),
    ("Turning every answer into a leadership story", "Forcing 'Training Lead' into unrelated "
     "questions.", "Use the coverage matrix (Part 4) to pick the story that actually fits, not the "
     "one that sounds most impressive."),
    ("Speaking negatively about teammates", "Frustration leaks into tone or word choice.",
     "Describe behavior and disagreement, not character judgments."),
    ("Speaking negatively about previous organizations", "Applies less for a student, but avoid "
     "trashing a club, course, or team experience.", "Frame any friction as something you learned from, "
     "not something that was 'badly run'."),
    ("Not knowing the company", "Generic 'why this company' answer.",
     "Use Part 17's research framework before every interview, not just the big-name ones."),
    ("Not asking meaningful questions", "Silence or a question already answered in the job posting at "
     "the end of the interview.", "Prepare from Part 18's bank and tailor at least one question to "
     "something the interviewer said earlier in the conversation."),
]
make_table(["Mistake", "What it looks like", "The fix"], mistakes, [1.4*inch, 2.7*inch, 3.1*inch],
           font_size=7.6)

# =============================================================== PART 14 ===
PART(14, "Conversational Delivery",
     "Sounding like a person talking, not a page being read aloud.")

H2("Habits to build")
bullets([
    "Pause for a second before answering &#8212; a brief pause reads as thoughtful, not unprepared.",
    "If a question is ambiguous, ask a clarifying question rather than guessing what they meant.",
    "It's fine to think out loud briefly (\"let me think of the clearest example...\") &#8212; it "
    "sounds human, as long as you don't do it for 30 seconds.",
    "Keep an internal structure (Situation/Task/Action/Result) without narrating the labels out loud.",
    "Maintain camera/eye engagement; notice if the interviewer looks like they want to jump in.",
    "Cut filler words ('um', 'like', 'basically') by slowing down slightly, not by rushing.",
    "Adjust length based on their reaction &#8212; leaning in and taking notes means go deeper; "
    "a nod and a beat of silence means wrap up.",
    "Recognize when you've answered enough: if you've hit BLUF + Situation + Task + Action + Result, "
    "stop and let them drive.",
])

H2("Useful transitions (use sparingly, not as a checklist)")
bullets([
    "\"The biggest challenge was...\"",
    "\"That was the main constraint I was working around.\"",
    "\"The decision came down to two real options.\"",
    "\"What I personally did was...\"",
    "\"The important lesson for me was...\"",
    "\"Looking back, I'd probably...\"",
    "\"To be specific about my part in this...\"",
])
note("If you use the same transition phrase in every single answer, it starts to sound as scripted "
     "as a memorized paragraph. Rotate naturally.")

# =============================================================== PART 15 ===
PART(15, "Handling Questions You Don't Have a Perfect Story For")

P("You have not had a manager, a paid job, or (as far as your background material shows) a serious "
  "interpersonal conflict on a team. That's normal for someone at this stage &#8212; and inventing "
  "one to avoid saying so is far riskier than answering honestly and pivoting to a real, adjacent "
  "example.", "Body")

H2("The bridge pattern")
P("\"I haven't had that exact situation yet, but I've experienced something similar when "
  "[FILL IN: real adjacent example] &#8212; here's what happened.\" Then tell the real story fully. "
  "Don't apologize repeatedly or dwell on the gap; one sentence, then move to substance.", "Body")

H2("Common substitutions for a student/early-career candidate")
subs = [
    ("A disagreement with your manager", "A disagreement with a hackathon teammate, club co-lead, or "
     "an AI-generated suggestion (S2, S11)."),
    ("Managing a direct report", "Training/mentoring newer Robotics Club members (S7)."),
    ("A production incident", "The concurrency risk you found and fixed in LedgerCore before it "
     "became a real incident (S1), or provider-failure handling in the Aggregation API (S3)."),
    ("A performance review", "Specific feedback from a teammate, club lead, or code review (S12)."),
    ("Negotiating with a client", "Persuading a team to adopt your idea for their pitch (S8)."),
    ("Working across departments/teams", "Coordinating with teammates under hackathon time pressure "
     "(S6), or working across the KNUST CS community with different teams (S8)."),
]
make_table(["If asked about...", "Bridge to..."], subs, [2.6*inch, 4.6*inch], font_size=8)
note("Never invent a manager, a job, or a workplace conflict you didn't have. Interviewers "
     "interviewing students expect exactly the substitutions above, and respect the honesty of the "
     "bridge far more than a fabricated corporate anecdote.")

# =============================================================== PART 16 ===
PART(16, "Hypothetical Behavioral Questions",
     "Answer the hypothetical briefly, then ground it in a real example.")

hyp = [
    ("How would you handle a disagreement?", "General approach: listen fully, look at the evidence, "
     "state your view clearly, be willing to update. \"I actually faced something like this when...\" "
     "&#8594; S2 or S11."),
    ("How do you prioritize tasks?", "General approach: identify what's actually blocking or "
     "highest-stakes, confirm with whoever set the priorities if unclear. \"For example...\" &#8594; "
     "S6 or S9."),
    ("What would you do if you were behind schedule?", "General approach: reassess scope honestly, "
     "communicate early rather than late, cut the least critical piece first. \"This happened during "
     "...\" &#8594; S6."),
    ("What would you do if a teammate was struggling?", "General approach: figure out specifically "
     "where they're stuck before jumping to a fix, offer to pair rather than just telling them the "
     "answer. \"I did something similar when...\" &#8594; S7."),
    ("What would you do if your manager asked you to do something you disagreed with?", "General "
     "approach: raise the concern once clearly with reasoning, then follow the decision unless it's "
     "an integrity issue. Bridge honestly: \"I haven't had a manager yet, but a similar case was...\" "
     "&#8594; S2 or S11."),
    ("What would you do if you discovered a serious bug before release?", "General approach: flag it "
     "immediately regardless of how it affects the timeline, don't quietly patch around it. \"This is "
     "close to what happened when...\" &#8594; S2 or S4."),
]
for q, a in hyp:
    keep([Paragraph(q, styles["H3"]), Paragraph(a, styles["BodySmall"])])
    SP(2)

# =============================================================== PART 17 ===
PART(17, "Company-Specific Preparation Framework",
     "A reusable checklist. Do this research fresh for every company &#8212; JPMorgan Chase, Goldman "
     "Sachs, Bloomberg, Bank of America, Google, or anyone else &#8212; rather than reusing generic "
     "talking points.")

note("This document does not fabricate company-specific facts for you. Every cell below is a "
     "prompt to go verify, not a pre-filled answer &#8212; company details change, and a stale or "
     "invented fact is worse than admitting you'd need to check.")

fw = [
    ("Company", "What does it actually do? Who are its real customers?", "Fact (verify)"),
    ("Technology", "What engineering problems does it solve? What systems/technologies does it "
     "discuss publicly (engineering blog, conference talks)?", "Fact (verify)"),
    ("Role", "What does the specific role involve, per the posting and, ideally, per the recruiter/"
     "interviewer? What skills does it emphasize?", "Fact (verify)"),
    ("Culture / values", "What does the company explicitly say it values (careers page, engineering "
     "blog, public statements)?", "Fact (verify)"),
    ("My connection", "Why do those specific, verified facts genuinely interest you &#8212; tied to "
     "a real project or interest of yours, not a generic compliment.", "Your interpretation"),
]
make_table(["Category", "What to research", "Type"], fw, [1.3*inch, 4.7*inch, 1.2*inch], font_size=8)

H2("Worked skeleton (fill in real research before use)")
P("\"[Company fact you verified] stood out to me because I've been working on [FILL IN: related "
  "project detail, e.g., failure isolation in the Aggregation API]. I want to see how that kind of "
  "problem is handled at [FILL IN: their scale/domain], and [FILL IN: specific role detail] is where "
  "I'd actually get to do that.\"", "Placeholder")
note("Never say a company is 'innovative' or 'prestigious' as the substance of your answer &#8212; "
     "those words carry zero information about why you specifically want to be there.")

# =============================================================== PART 18 ===
PART(18, "Questions to Ask the Interviewer",
     "Avoid anything answered by the job posting. Prefer questions you can follow up on based on "
     "what they actually say.")

ask_groups = {
    "Engineering": [
        "What does the on-call or incident-response process look like for this team?",
        "How does the team decide between building something in-house versus using an existing tool?",
        "What's a recent technical decision the team debated, and how was it resolved?",
    ],
    "Team": [
        "How is the team structured, and how does this role fit into it?",
        "How do engineers on this team typically split time between new features and maintenance?",
    ],
    "Mentorship": [
        "What does mentorship look like for someone in this role &#8212; formal, informal, "
        "assigned?",
        "What's something a past intern or new hire struggled with, and how did the team support "
        "them?",
    ],
    "Learning": [
        "What's something you've personally learned in this role that surprised you?",
        "What resources or practices does the team use to ramp people up on unfamiliar systems?",
    ],
    "Role": [
        "What would success look like in the first three months in this role?",
        "What's the balance between independent work and pairing/collaboration day to day?",
    ],
    "Projects": [
        "What's a project the team shipped recently that you're proud of?",
        "What's the most technically interesting problem the team is currently working on?",
    ],
    "Career development": [
        "What does growth from this role typically look like a year or two in?",
        "How does the team give feedback &#8212; formal reviews, ongoing, both?",
    ],
    "Company": [
        "How has the team's priorities shifted in the last year, and why?",
        "What's something about working here that isn't obvious from the outside?",
    ],
}
for cat, qs in ask_groups.items():
    H3(cat)
    bullets(qs)

H2("Following up naturally")
P("If the interviewer's answer to one of these mentions something specific (a tool, a project, a "
  "challenge), ask one genuine follow-up about that specific thing rather than moving straight to "
  "your next prepared question &#8212; it's the clearest signal you were actually listening.", "Body")

# =============================================================== PART 19 ===
PART(19, "Mock Interview System",
     "Six practice modes. Run these out loud &#8212; alone, recorded, or with a friend &#8212; not "
     "silently in your head.")

H3("Mode 1 &#8212; Rapid behavioral (10 questions, short answers)")
P("Goal: clarity and conciseness. Give yourself 60&#8211;90 seconds per answer, no follow-ups. Pull "
  "10 questions at random from Part 24.", "Body")

H3("Mode 2 &#8212; Deep behavioral (5 questions, heavy follow-ups)")
P("Goal: depth and consistency under pressure. Pick 5 questions from Part 6. After each answer, "
  "immediately fire 3&#8211;4 follow-ups from the matching chain in Part 8.", "Body")

H3("Mode 3 &#8212; Project-focused")
P("Goal: technical-behavioral fluency. Use only Part 9's Aggregation API and LedgerCore questions. "
  "Answer at 60 seconds first, then again at 2 minutes for the same question.", "Body")

H3("Mode 4 &#8212; Company motivation")
P("Run this exact sequence: Tell me about yourself &#8594; Why this company? &#8594; Why this role? "
  "&#8594; Where do you see yourself in five years? &#8594; your prepared questions from Part 18. "
  "Do this once per company you're actually interviewing with, using real research (Part 17).", "Body")

H3("Mode 5 &#8212; Pressure test")
P("Goal: handling the unexpected. Have someone else (or a randomizer) pick questions from Part 24 "
  "without telling you in advance, including at least one you don't have a clean story for &#8212; "
  "practice the bridge pattern from Part 15 live.", "Body")

H3("Mode 6 &#8212; Follow-up interrogation")
P("Goal: defending one story under real pressure. Pick a single story from Part 5. Have a partner "
  "ask follow-up after follow-up &#8212; not from a fixed list &#8212; until you either run out of "
  "real detail or five minutes pass. Where you ran out of real detail is exactly where you need to "
  "fill in more from your own memory before a real interview.", "Body")

# =============================================================== PART 20 ===
PART(20, "Scoring Rubric",
     "Score each practice answer on these dimensions as Strong / Developing / Needs work. This is "
     "diagnostic, not a hire/no-hire score.")

rubric = [
    ("Relevance", "Did I actually answer the question asked, not an adjacent one?"),
    ("Structure", "Was the answer easy to follow &#8212; BLUF, then Situation/Task/Action/Result?"),
    ("Ownership", "Was my personal contribution clearly distinguished from the team's?"),
    ("Communication", "Was I clear, at the right level of detail for the listener?"),
    ("Conciseness", "Did I avoid unnecessary context or rambling?"),
    ("Evidence", "Did I give a concrete example rather than a general claim?"),
    ("Impact", "Did I explain what actually resulted, honestly?"),
    ("Self-awareness", "Did I recognize my own mistakes or limitations where relevant?"),
    ("Learning", "Did I explain what changed afterward, not just what happened?"),
    ("Coachability", "Did I show an actual behavior change, not just openness in the abstract?"),
    ("Authenticity", "Did I sound like I was talking, not reciting?"),
    ("Follow-up readiness", "Could I defend every detail if pushed on it?"),
]
make_table(["Dimension", "Ask yourself"], rubric, [1.5*inch, 5.9*inch], font_size=8.4)
note("If two or more dimensions come back 'Needs work' on the same story repeatedly, that's a "
     "signal to revise the story card in Part 5, not to keep re-practicing the same weak version.")

# =============================================================== PART 21 ===
PART(21, "30 / 60 / 2-Minute Answer Compression",
     "The same story, expanding outward from the same core point. Nothing here is a separate script "
     "&#8212; each longer version is literally the shorter version plus more of the real detail.")

def compression_block(title, s30, s60, s120):
    H2(title)
    keep([Paragraph("30 seconds", styles["H3"]), Paragraph(s30, styles["BodySmall"])])
    keep([Paragraph("60 seconds", styles["H3"]), Paragraph(s60, styles["BodySmall"])])
    keep([Paragraph("2 minutes", styles["H3"]), Paragraph(s120, styles["BodySmall"])])

compression_block(
    "S2 &#8212; Rejecting an AI suggestion",
    "\"While working on LedgerCore, an AI tool suggested a fix that would've made an error disappear "
    "without actually fixing what caused it. I rejected it and traced the real cause instead.\"",
    "Add: what specifically the AI suggested, why it would have masked rather than solved the "
    "problem, and what the actual root cause turned out to be.",
    "Add: how you verified the real fix, what this taught you about reviewing AI output in a system "
    "where correctness really matters, and how this shapes how you use AI tools generally now."
)
compression_block(
    "S6 &#8212; FarmLink hackathon",
    "\"As part of Team Nova, I [FILL IN: your specific contribution] on FarmLink during the Youth "
    "Arise hackathon, and our team won.\"",
    "Add: the specific problem FarmLink solved, your specific role versus your teammates', and the "
    "biggest constraint you worked around under the time limit.",
    "Add: a specific decision you personally pushed for, how the team coordinated under pressure, "
    "and what you learned about scoping ambition to time available."
)
note("Watch the interviewer, not the clock: someone leaning in after your 30-second version wants "
     "the 60- or 2-minute version next, unprompted. Someone who moves on wants you to stay short.")

# =============================================================== PART 22 ===
PART(22, "Active Recall Exercises",
     "Close the document. Answer these from memory. Then check yourself against the earlier parts "
     "&#8212; don't peek first.")

H2("Round 1 &#8212; Story inventory")
bullets([
    "What are your 12 story slots, by ID and one-line title?",
    "Which 3 are still templates you need to fill in?",
    "For each of your 9 concrete stories, what competency is its strongest fit?",
])
H2("Round 2 &#8212; Per-story recall (pick any 3 stories and answer all 5)")
bullets([
    "What happened, in one sentence (the BLUF)?",
    "What did I personally do, distinct from anyone else involved?",
    "What was the actual result?",
    "What did I learn?",
    "What would I do differently?",
])
H2("Round 3 &#8212; Defense")
bullets([
    "For S1: what metric can I actually defend if asked 'how do you know it worked'?",
    "For S2: what exactly did the AI suggest, and what was the real root cause?",
    "For S5: what was the simpler alternative, and why wasn't it enough?",
    "For whichever gap story (S10/S11/S12) I've filled in: what's the one follow-up most likely to "
    "expose a thin spot, and do I have a real answer for it?",
])
note("If you can't answer Round 3 from memory, that story isn't ready for a real interview yet "
     "&#8212; go back to Part 5 and add the missing detail honestly, don't just reread this section.")

# =============================================================== PART 23 ===
PART(23, "Story Retrieval Drills",
     "The goal is speed: given a competency, you should be able to name a story within 2&#8211;3 "
     "seconds, not after searching.")

drill_comps = ["Leadership", "Failure", "Conflict", "Technical communication", "Coachability",
               "Initiative", "Prioritization", "Adaptability", "Ownership", "Persuasion",
               "Decision-making", "Curiosity", "Working under pressure", "Attention to quality",
               "Responsible use of AI"]
P("Go down this list without looking at Part 4. For each competency, say out loud which story you'd "
  "use and why, in under 10 seconds. Then check yourself against the coverage matrix.", "Body")
bullets([f"Competency: {c}" for c in drill_comps])

# =============================================================== PART 24 ===
PART(24, "Random Question Bank",
     "A large, deliberately unsorted mix for practice &#8212; easy, unusual, hypothetical, project-"
     "specific, and human-focused questions all together. The point is to test whether you actually "
     "understand your experience, not whether you've memorized which bucket a question belongs to.")

RANDOM_QS = [
    "What's a project you're proud of, and why?",
    "Tell me about a time you had to say no to something.",
    "How do you approach code review, either giving or receiving it?",
    "Tell me about a time your first solution to a problem was wrong.",
    "What's the most complex system you've worked on?",
    "Tell me about a time you had to work with incomplete information.",
    "How do you handle being told your approach is wrong?",
    "Tell me about a time you had to choose between speed and correctness.",
    "What's something you built that nobody asked you to build?",
    "Tell me about a time you had to give someone unwelcome feedback.",
    "How do you decide when a bug is worth fixing right now versus later?",
    "Tell me about a time you were the least experienced person in the room.",
    "What would your teammates say your biggest strength is?",
    "Tell me about a time you had to trust someone else's work without verifying it yourself.",
    "How do you approach learning a codebase you didn't write?",
    "Tell me about a time a tool or library let you down.",
    "What's a technical opinion you hold that not everyone agrees with?",
    "Tell me about a time you had to make a tradeoff between two things you both cared about.",
    "How do you know when you're done with a task, versus just tired of it?",
    "Tell me about a time you asked for help.",
    "What's the difference between a good and a great engineer, in your view?",
    "Tell me about a time you had to unlearn something you thought was true.",
    "How would you explain what an API is to your grandparent?",
    "Tell me about a time you were wrong about how long something would take.",
    "What's a mistake you see other people make that you try to avoid?",
    "Tell me about a time you had to defend a decision to a skeptical audience.",
    "How do you stay organized across multiple things happening at once?",
    "Tell me about a time you changed your mind about a technical approach mid-project.",
    "What does 'ownership' mean to you, concretely?",
    "Tell me about a time you had to work with a tool you didn't like.",
    "How do you handle a task with no clear owner?",
    "Tell me about a time you caught your own mistake before anyone else did.",
    "What's a skill you're actively trying to improve right now?",
    "Tell me about a time you had to simplify something that was overly complex.",
    "How do you decide how much testing is enough?",
    "Tell me about a time you worked with someone very different from you.",
    "What's the hardest technical concept you've had to learn?",
    "Tell me about a time a plan changed at the last minute.",
    "How do you handle criticism of something you built?",
    "Tell me about a time you had to be patient with a slower process than you wanted.",
    "What's something you'd do differently if you restarted LedgerCore from scratch?",
    "Tell me about a time you helped debug something that wasn't your code.",
    "How do you balance perfectionism with shipping something on time?",
    "Tell me about a time you misjudged how difficult something would be.",
    "What's a question you wish interviewers would ask you?",
    "Tell me about a time you had to advocate for doing something the 'right' way under time "
    "pressure.",
    "How do you approach a problem you've truly never seen before?",
    "Tell me about a time you worked without much supervision.",
    "What's a risk you took that didn't pay off?",
    "Tell me about a time you had to communicate bad news.",
    "How would a teammate describe working with you under pressure?",
    "Tell me about a time you improved a process, not just a piece of code.",
    "What's something about the Aggregation API you'd want to redesign with more time?",
    "Tell me about a time you had to make a call without your team lead available.",
    "How do you handle a disagreement about priorities with someone senior to you?",
    "Tell me about a time you were the one who found a problem nobody else had noticed.",
    "What does a 'good day of work' look like for you?",
    "Tell me about a time you had to say 'I don't know' in front of others.",
    "How do you decide what to automate versus do manually?",
    "Tell me about a time you had to rebuild trust after something went wrong.",
    "What's the last thing you taught yourself, outside of a class requirement?",
]
bullets(RANDOM_QS, "BodySmall")

# =============================================================== PART 25 ===
PART(25, "Your Personal Behavioral Gaps",
     "An honest read of where your evidence is strong, moderate, or weak &#8212; and how to close the "
     "real gaps through more real experience, not through better storytelling.")

gaps = [
    ("Technical problem solving", "Strong", "S1, S3, S4 are all real, specific, and defensible."),
    ("Technical decision-making / tradeoffs", "Strong", "S5 is a genuine architecture tradeoff with "
     "real reasoning."),
    ("Responsible AI use", "Strong", "S2 is a specific, credible, non-generic story &#8212; rare "
     "among candidates."),
    ("Attention to quality / correctness", "Strong", "S1, S2, S4 all show real diligence about "
     "correctness."),
    ("Leadership", "Moderate", "S7 (Robotics) and S6 (FarmLink) are real roles, but currently need "
     "specific actions and results filled in to be strong evidence rather than titles."),
    ("Teamwork / collaboration", "Moderate", "S6 and S8 are real, but thin on specifics of what you "
     "personally contributed versus the group."),
    ("Persuasion / communication with non-engineers", "Moderate", "S8 is a good foundation but needs "
     "one specific, filled-in example to be strong."),
    ("Learning agility / curiosity", "Moderate", "S9 is plausible given the projects, but needs a "
     "specific technology and moment filled in."),
    ("Failure and learning", "Weak (currently a gap)", "No specific, real failure was included in your "
     "background material. This is the single most important gap to close before interviews, since "
     "'tell me about a failure' is one of the most common behavioral questions."),
    ("Interpersonal conflict resolution", "Weak (currently a gap)", "S2 covers disagreeing with an AI "
     "suggestion, but not a person-to-person conflict. Likely to come up directly."),
    ("Receiving and acting on feedback", "Weak (currently a gap)", "No specific feedback-and-change "
     "story was in your background material. Very likely to come up given how strongly interviewers "
     "weight coachability for junior candidates."),
    ("Customer / user focus", "Weak-to-moderate", "Your projects use mock providers, not real users "
     "&#8212; be honest about this rather than implying real customer impact you didn't have."),
]
make_table(["Competency", "Evidence strength", "Why"], gaps, [1.7*inch, 1.1*inch, 4.6*inch],
           font_size=7.8)

H2("How to close these gaps for real, not just for the interview")
bullets([
    "<b>Failure and learning:</b> Reflect honestly on LedgerCore or the Aggregation API &#8212; was "
    "there a version of your dedup or concurrency fix that didn't work the first time? A design "
    "choice you reversed? That is real material for S10, if you look for it honestly instead of "
    "assuming you need a dramatic failure.",
    "<b>Conflict resolution:</b> Look at FarmLink and the KNUST CS community work again &#8212; a "
    "hackathon under time pressure and a 3-person team almost always produce at least one real "
    "disagreement about approach or scope. Recall it honestly rather than assuming there wasn't one.",
    "<b>Feedback and coachability:</b> Think about code review comments (human or AI), a Robotics "
    "Club member's reaction to your teaching, or a KNUST CS teammate's reaction to your pitch "
    "feedback &#8212; feedback doesn't require a formal review process to count.",
    "<b>Customer/user focus:</b> Consider contributing to an actual open-source project with real "
    "users, or extending a personal project so it has real (even if small) usage, if you want "
    "genuine evidence here rather than just an honest disclosure of the gap.",
    "<b>Leadership and teamwork specifics:</b> These aren't gaps in experience, just gaps in "
    "documentation &#8212; go fill in S6, S7, and S8 with real detail; the experience is already "
    "there.",
])
note("Do not fabricate a failure, a conflict, or feedback to fill these gaps. If, after honest "
     "reflection, a gap is genuinely empty, say so plainly if asked directly, and use the bridge "
     "pattern from Part 15. A thoughtfully honest 'I haven't had that yet' is stronger evidence of "
     "self-awareness than a fabricated story that collapses under a follow-up.")

# =============================================================== PART 26 ===
PART(26, "Your Personal Behavioral Handbook",
     "The one section to reread the night before an interview. Everything else in this document "
     "feeds into this page.")

H2("My core stories (fill in once S6&#8211;S12 are complete)")
bullets([
    "S1 &#8212; LedgerCore concurrency and idempotency",
    "S2 &#8212; Rejecting an AI suggestion on LedgerCore",
    "S3 &#8212; Aggregation API provider failure handling",
    "S4 &#8212; Aggregation API duplicate prevention",
    "S5 &#8212; Kafka/Redis architecture tradeoff",
    "S6 &#8212; FarmLink hackathon (Team Nova, won)",
    "S7 &#8212; Robotics Club Training Lead",
    "S8 &#8212; KNUST CS Open Source Community pitch coaching",
    "S9 &#8212; Learning new technology fast",
    "S10, S11, S12 &#8212; [FILL IN once completed]",
])

H2("My main strengths (per Part 25)")
bullets(["Technical problem solving under real constraints (concurrency, failure handling, "
         "duplicates).", "Independent technical judgment, including toward AI-generated suggestions.",
         "Attention to correctness in systems where correctness actually matters (financial data)."])

H2("My development areas (per Part 25)")
bullets(["Documenting leadership and teamwork stories with specific actions, not just roles.",
         "Building and being honest about a real failure story.",
         "Building and being honest about a real interpersonal-conflict story.",
         "Building and being honest about a real feedback-and-change story."])

H2("My career direction")
placeholder("one or two honest sentences on where you want to grow &#8212; e.g., toward backend "
            "systems, data correctness, distributed systems &#8212; based on what actually drew you "
            "into LedgerCore and the Aggregation API")

H2("Why software engineering / why backend systems / why internships")
placeholder("your honest, short answer, built from Part 7 sections 1&#8211;2 and 12")

H2("My strongest story, by category")
strongest = [
    ("Strongest technical project", "LedgerCore (S1) or the Aggregation API (S3/S4/S5)"),
    ("Strongest teamwork story", "S6 (FarmLink) once filled in, or S8"),
    ("Strongest failure/learning story", "S10 &#8212; must be filled in with a real incident first"),
    ("Strongest leadership story", "S7 (Robotics Club) once filled in with specifics"),
    ("Strongest technical challenge", "S1 &#8212; concurrency and idempotency"),
    ("Strongest AI/engineering judgment story", "S2"),
    ("Strongest communication story", "S8 or S5, depending on the audience in the question"),
]
make_table(["Category", "Your story"], strongest, [2.6*inch, 4.6*inch], font_size=8.2)

H2("My key metrics (per Part 11)")
bullets(["Team Nova (FarmLink) won the Youth Arise hackathon.",
         "Robotics Club: Training Lead and Programmer.",
         "KNUST CS Open Source Community: part of a 3-person team.",
         "[FILL IN any additional verified metric from Part 11]"])

H2("Questions I can ask interviewers (see Part 18 for the full bank)")
bullets(["One from Engineering.", "One from Mentorship or Career development.",
         "One built live from something the interviewer said earlier in the conversation."])

# ========================================================== FINAL CHECKLIST
PART("Final", "Final Interview Checklist")

H2("Story preparation")
checklist([
    "I know my 8&#8211;12 core stories.",
    "I know what happened in each story.",
    "I know what I personally did.",
    "I know the result.",
    "I know what I learned.",
    "I know what I would do differently.",
    "I know the competencies each story demonstrates.",
    "I have filled in every [FILL IN] blank in S6&#8211;S12 with real, honest detail.",
])

H2("Delivery")
checklist([
    "I can answer without memorizing a script.",
    "I can give a 30-second version.",
    "I can give a 60-second version.",
    "I can expand when asked.",
    "I can stay concise when a short answer is enough.",
    "I can use 'I' when describing my contribution.",
    "I can explain technical concepts simply, for a non-technical listener.",
])

H2("Behavioral competencies")
checklist(["Teamwork", "Communication", "Leadership", "Ownership", "Failure", "Learning",
           "Coachability", "Conflict", "Prioritization", "Adaptability", "Initiative",
           "Problem solving", "Decision-making", "Technical communication",
           "Responsible use of AI"])

H2("Company preparation")
checklist([
    "I know what the company does.",
    "I understand the role.",
    "I know why I genuinely want the role.",
    "I can explain the connection between my goals and the role.",
    "I have thoughtful questions prepared.",
])

H2("Follow-ups")
checklist([
    "I can explain why I made decisions.",
    "I can explain alternatives I considered.",
    "I can explain tradeoffs.",
    "I can admit what I do not know.",
    "I can explain mistakes honestly.",
    "I can explain what I learned.",
    "I can defend my stories without inventing details.",
])

SP(16)
HR(NAVY, 1.2)
P("<b>The final principle.</b> Do not memorize answers. Know your experiences. Know what you did. "
  "Know why you did it. Know what happened. Know what you learned. Know what you would change. Know "
  "what tradeoffs existed. Know how your behavior changed afterward. Then adapt those stories "
  "naturally to whatever the interviewer actually asks. By the end of the conversation, the "
  "interviewer should understand who you are, how you work, how you learn, how you solve problems, "
  "how you work with people, how you respond when things go wrong, and why you want the role.", "Body")

flow.append(Spacer(1, 20))
flow.append(Paragraph("Prepared for sawissah@st.knust.edu.gh &#8212; a working document. Update the "
    "[FILL IN] blanks as your experience grows, and revisit the Story Bank (Part 3) whenever you "
    "finish a new project.", styles["Footer"]))

print("module loaded ok")

doc = SimpleDocTemplate(OUT, pagesize=LETTER, topMargin=0.6*inch, bottomMargin=0.6*inch,
                         leftMargin=0.55*inch, rightMargin=0.55*inch, title="Behavioral Interview Prep")
doc.build(flow)
print("PDF built:", OUT)
