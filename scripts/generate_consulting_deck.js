const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'MarginLadder Portfolio Case Study';
pptx.subject = 'Hypothetical RFQ-to-quote decision case';
pptx.title = 'MarginLadder | Executive Recommendation';
pptx.company = 'Portfolio Case Study';
pptx.lang = 'en-IN';
pptx.theme = { headFontFace: 'Aptos Display', bodyFontFace: 'Aptos', lang: 'en-IN' };
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: 'F4F7FA' },
  objects: [
    { rect: { x: 0, y: 0, w: 13.333, h: 0.10, line: { color: '0F766E', transparency: 100 }, fill: { color: '0F766E' } } },
    { line: { x: 0.45, y: 7.12, w: 12.43, h: 0, line: { color: 'D7E0E8', width: 1 } } },
    { text: { text: 'MARGINLADDER  •  HYPOTHETICAL CASE  •  ASSUMPTION-LED', options: { x: 0.48, y: 7.17, w: 8.8, h: 0.16, fontFace: 'Aptos', fontSize: 7.5, color: '64748B', margin: 0, breakLine: false } } },
  ],
  slideNumber: { x: 12.37, y: 7.14, w: 0.35, h: 0.18, color: '64748B', fontFace: 'Aptos', fontSize: 8, align: 'right' },
  masterName: 'MASTER',
});
const C = { navy:'102A43', teal:'0F766E', cyan:'D9F0EE', ink:'243B53', muted:'627D98', white:'FFFFFF', paper:'F4F7FA', pale:'EAF0F5', gold:'D69E2E', goldPale:'FFF4D6', red:'B54747', redPale:'FCE8E6', green:'247A5A', greenPale:'E4F2EC', line:'D7E0E8', steel:'486581' };
const SW = 13.333, SH = 7.5;
function txt(slide, text, x, y, w, h, opts={}) {
  slide.addText(text, { x, y, w, h, margin: 0, fontFace: opts.fontFace || 'Aptos', fontSize: opts.fontSize || 14,
    color: opts.color || C.ink, bold: !!opts.bold, breakLine: false, valign: opts.valign || 'mid',
    align: opts.align || 'left', paraSpaceAfterPt: opts.paraSpaceAfterPt || 0,
    bullet: opts.bullet, fit: 'shrink', isTextBox: true, ...opts });
}
function rect(slide,x,y,w,h,fill, radius=0.12, line=fill) {
  slide.addShape(pptx.ShapeType.roundRect, {x,y,w,h,rectRadius:radius,line:{color:line,transparency:line===fill?100:0,width:1},fill:{color:fill},radius});
}
function line(slide,x,y,w,color=C.line,width=1) { slide.addShape(pptx.ShapeType.line,{x,y,w,h:0,line:{color,width}}); }
function base(title, kicker='DECISION CASE') {
  const s = pptx.addSlide('MASTER');
  txt(s,kicker.toUpperCase(),0.55,0.27,8,0.2,{fontSize:8.5,bold:true,color:C.teal,charSpacing:1.2});
  txt(s,title,0.55,0.55,12.15,0.58,{fontSize:25,bold:true,color:C.navy, valign:'mid'});
  return s;
}
function card(slide,x,y,w,h,title,body,accent=C.teal,bodySize=13) {
  rect(slide,x,y,w,h,C.white,0.1,C.line);
  slide.addShape(pptx.ShapeType.rect,{x,y,w:0.055,h,line:{color:accent,transparency:100},fill:{color:accent}});
  txt(slide,title,x+0.2,y+0.14,w-0.4,0.28,{fontSize:13,bold:true,color:C.navy});
  txt(slide,body,x+0.2,y+0.51,w-0.4,h-0.62,{fontSize:bodySize,color:C.ink,valign:'top',breakLine:false,fit:'shrink'});
}
function pill(slide,text,x,y,w,fill=C.cyan,color=C.teal) {
  rect(slide,x,y,w,0.28,fill,0.1,fill);
  txt(slide,text,x+0.08,y+0.02,w-0.16,0.22,{fontSize:8.5,bold:true,color,align:'center'});
}
function metric(slide,x,y,w,value,label,tag='') {
  rect(slide,x,y,w,1.0,C.white,0.1,C.line);
  txt(slide,value,x+0.16,y+0.11,w-0.32,0.40,{fontSize:24,bold:true,color:C.navy});
  txt(slide,label,x+0.16,y+0.57,w-0.32,0.24,{fontSize:9.5,color:C.muted});
  if(tag) txt(slide,tag,x+0.16,y+0.82,w-0.32,0.12,{fontSize:7,color:C.teal,bold:true});
}
function bullets(slide,items,x,y,w,lineH=0.47,fontSize=12.5,color=C.ink) {
  items.forEach((it,i)=>{
    slide.addShape(pptx.ShapeType.ellipse,{x,y:y+i*lineH+0.115,w:0.08,h:0.08,line:{color:C.teal,transparency:100},fill:{color:C.teal}});
    txt(slide,it,x+0.18,y+i*lineH,w-0.18,lineH-0.03,{fontSize,color,valign:'top'});
  });
}

// 1 — Cover / answer first
{
  const s=pptx.addSlide('MASTER');
  s.background={color:C.navy};
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:0.16,h:7.5,line:{color:C.teal,transparency:100},fill:{color:C.teal}});
  txt(s,'MARGINLADDER  /  EXECUTIVE DECISION CASE',0.72,0.58,10,0.25,{fontSize:10,bold:true,color:'7DD3C7',charSpacing:1.4});
  txt(s,'Instrument the RFQ flow\nbefore funding automation.',0.72,1.28,8.6,1.48,{fontSize:31,bold:true,color:C.white,valign:'top'});
  txt(s,'A staged recommendation for a hypothetical Pune auto-components manufacturer',0.75,3.02,8.6,0.42,{fontSize:16,color:'D9E2EC'});
  rect(s,0.75,4.0,7.7,1.45,'1B3B55',0.1,'1B3B55');
  txt(s,'RECOMMENDATION',1.0,4.22,2.0,0.2,{fontSize:9,bold:true,color:'7DD3C7'});
  txt(s,'Fund measurement and a reversible workflow pilot. Release broader costing automation only after stage timing, price parity and plant capacity are proven.',1.0,4.57,7.05,0.65,{fontSize:16,bold:true,color:C.white,valign:'top'});
  txt(s,'CASE INPUTS • NO CLIENT • NO PRODUCTION DATA • NO MEASURED OUTCOMES',0.75,6.55,9,0.25,{fontSize:9,bold:true,color:'D9E2EC'});
  txt(s,'18 NOVEMBER 2026',10.25,6.55,2.2,0.25,{fontSize:9,bold:true,color:'D9E2EC',align:'right'});
}
// 2 — framing
{
  const s=base('A nine-day RFQ cycle is a process outcome—not yet a software diagnosis.');
  metric(s,0.6,1.55,2.85,'9 days','Current RFQ-to-quote cycle','BRIEF INPUT');
  metric(s,3.55,1.55,2.85,'4 days','Target RFQ-to-quote cycle','BRIEF TARGET');
  metric(s,6.5,1.55,2.85,'60 / month','RFQs in the case brief','BRIEF INPUT');
  metric(s,9.45,1.55,2.85,'5 parts','Average parts per RFQ','BRIEF INPUT');
  card(s,0.6,3.0,5.95,2.55,'Decision to make','Where is elapsed time actually spent, and which intervention improves quote speed without weakening pricing, approval or fulfilment controls?',C.teal,15);
  card(s,6.8,3.0,5.95,2.55,'What the brief does not establish','The nine-day cycle is not decomposed by stage. There is no real RFQ trace, stakeholder interview, signed UAT or proof that cycle time causes the assumed losses.',C.gold,15);
  txt(s,'WORKING HYPOTHESIS: manage visibility and handoffs first; automate only where event evidence identifies a repeatable bottleneck.',0.68,6.0,11.9,0.4,{fontSize:14,bold:true,color:C.navy,align:'center'});
}
// 3 — known vs unknown
{
  const s=base('Separate brief facts, derived arithmetic and open questions before choosing a solution.');
  card(s,0.6,1.55,3.95,4.6,'Known from the hypothetical brief','• 60 RFQs / month\n• 5 parts / RFQ\n• 2.5 estimator-hours / part\n• 1.0 hour / part target\n• 9-day current cycle\n• 4-day target\n• 5% lost-RFQ rate',C.teal,14);
  card(s,4.7,1.55,3.95,4.6,'Derived from the inputs','• 12.5 costing hours / RFQ\n• 1.56 working days of hands-on costing\n• 7.44 days residual elapsed time\n• 720 RFQs / year\n• 36 lost RFQs / year\n• ₹86.4L theoretical margin pool',C.green,14);
  card(s,8.8,1.55,3.95,4.6,'Still unknown','• Intake completeness delay\n• Assignment / queue time\n• Rework and cost-data gaps\n• Approval delay / delegation\n• Customer holds\n• Quote dispatch lag\n• Capacity to fulfil recovered orders',C.gold,14);
  pill(s,'NO STAGE-LEVEL OBSERVATION YET',4.55,6.35,4.25,C.goldPale,'8A5A00');
}
// 4 — issue tree
{
  const s=base('Structure the diagnosis around five possible sources of delay.');
  rect(s,4.85,1.42,3.65,0.68,C.navy,0.1,C.navy);
  txt(s,'WHY DOES AN RFQ TAKE 9 WORKING DAYS?',5.05,1.62,3.25,0.26,{fontSize:14,bold:true,color:C.white,align:'center'});
  const xs=[0.55,3.08,5.61,8.14,10.67];
  const titles=['Intake &\nassignment','Technical\ncosting','Approval &\nrouting','Customer\nholds','Quote\ndispatch'];
  const bodies=[
    'Completeness\nOwnership\nQueue discipline',
    'Rate lookup\nData gaps\nRework / revisions',
    'Thresholds\nDelegation\nBatch approvals',
    'Missing inputs\nClarification loops\nCustomer response',
    'Formatting\nFinal checks\nSend / follow-up'
  ];
  xs.forEach((x,i)=>{
    line(s,x+1.02,2.1,0,C.teal,1.5);
    rect(s,x,2.62,2.12,2.3,C.white,0.1,C.line);
    txt(s,titles[i],x+0.14,2.82,1.84,0.58,{fontSize:15,bold:true,color:C.navy,align:'center'});
    txt(s,bodies[i],x+0.18,3.58,1.78,0.92,{fontSize:11,color:C.ink,align:'center',valign:'top'});
  });
  rect(s,1.1,5.35,11.1,0.75,C.cyan,0.1,C.cyan);
  txt(s,'Evidence required for every branch: event timestamp + owner/actor + reason code + exception path + complete-case coverage.',1.35,5.57,10.6,0.3,{fontSize:14,bold:true,color:C.navy,align:'center'});
}
// 5 — value pool
{
  const s=base('The value pool is material—but the recovery rate is the pivotal assumption.');
  metric(s,0.65,1.52,3.0,'₹86.4L','Theoretical annual lost-RFQ margin pool','DERIVED');
  metric(s,3.8,1.52,3.0,'₹21.6L','Annual recovered contribution at 25%','ASSUMPTION-DRIVEN');
  metric(s,6.95,1.52,2.65,'11.6%','Win-back to break even incl. run cost','DERIVED');
  metric(s,9.75,1.52,2.65,'₹10.8L','At 12.5% conservative win-back','ASSUMPTION-DRIVEN');
  card(s,0.65,3.0,5.85,2.42,'Formula chain','720 RFQs × 5% lost = 36 lost RFQs\n36 × ₹20L average order value × 12% contribution = ₹86.4L pool\n₹86.4L × 25% win-back = ₹21.6L contribution',C.teal,14);
  card(s,6.8,3.0,5.85,2.42,'What must be validated','What qualifies as a lost RFQ? How many losses were delay-related? Does a faster quote win the order? Is the 12% margin truly incremental contribution? Can the plant fulfil it?',C.gold,13.5);
  txt(s,'The 25% win-back is 50% delay attribution × 50% conversion. It is not an observed conversion rate.',0.72,5.82,11.9,0.42,{fontSize:12,bold:true,color:C.red,align:'center'});
}
// 6 — cycle time and estimator capacity
{
  const s=base('Hands-on costing effort is not the same as elapsed cycle time.');
  rect(s,0.7,1.55,5.6,0.58,C.navy,0.08,C.navy);
  txt(s,'9.00 DAYS TOTAL BRIEF CYCLE',0.9,1.7,5.2,0.25,{fontSize:15,bold:true,color:C.white,align:'center'});
  rect(s,0.7,2.38,1.0,0.72,C.teal,0.08,C.teal);
  txt(s,'1.56d',0.78,2.56,0.84,0.3,{fontSize:15,bold:true,color:C.white,align:'center'});
  rect(s,1.82,2.38,4.48,0.72,'DCE5EC',0.08,'DCE5EC');
  txt(s,'7.44d residual — stage split unknown',2.0,2.56,4.1,0.3,{fontSize:14,bold:true,color:C.navy,align:'center'});
  txt(s,'12.5 hands-on hours ÷ 8 hours/day = 1.56 working days. The residual may include intake, queues, approval, customer holds and dispatch.',0.75,3.35,5.55,0.95,{fontSize:12.5,color:C.ink,valign:'top'});
  card(s,6.65,1.55,2.85,2.75,'Estimator workload','9,000 hours/year current\n3,600 hours/year target\n5,400 gross hours released\n4,680 net of 1h/RFQ review',C.teal,12.5);
  card(s,9.75,1.55,2.85,2.75,'Value treatment','₹21.06L theoretical net capacity value; do not call it cash savings. The modelled queue wait is 0.57 day, not an observed wait.',C.gold,12.5);
  rect(s,0.72,4.82,11.9,0.92,C.goldPale,0.1,C.goldPale);
  txt(s,'GATE 3: the plant must be able to make at least 46% of the recovered-margin workload for the base first-year economics to break even.',1.02,5.08,11.3,0.42,{fontSize:15,bold:true,color:'805B00',align:'center'});
}
// 7 — Options
{
  const s=base('Choose the smallest reversible option that makes the real bottleneck visible.');
  const x=[0.62,4.55,8.48], w=3.72;
  card(s,x[0],1.6,w,3.75,'Option A — Costing screen only','Upside\n• Standardises pricing inputs\n• Could reduce manual calculation effort\n\nRisk\n• May leave upstream and approval queues untouched\n\nDecision\nFallback if costing is proven to dominate elapsed time.',C.gold,12.4);
  card(s,x[1],1.6,w,3.75,'Option B — Workflow visibility','Upside\n• Exposes owner, state, due date and next action\n• Creates timestamp evidence\n• Preserves current costing engine\n\nRisk\n• Benefits depend on adoption and clean event capture\n\nDecision\nRecommended first release.',C.teal,12.4);
  card(s,x[2],1.6,w,3.75,'Option C — Full platform / ERP integration','Upside\n• Broadest future automation\n\nRisk\n• Highest cost, integration and change exposure before root cause is known\n\nDecision\nDefer until trace, price parity, UAT and capacity gates pass.',C.red,12.4);
  pill(s,'RECOMMEND OPTION B — STAGED, REVERSIBLE, MEASURED',3.8,5.85,5.8,C.greenPale,C.green);
}
// 8 — MVP design
{
  const s=base('The MVP should improve control and clarity—not replace commercial judgement.','PRODUCT / OPERATING MODEL');
  const labels=['Intake','Completeness','Assign owner','Cost & version','Approval','Send quote','Measure'];
  const start=0.48, gap=0.19, bw=1.62;
  labels.forEach((t,i)=>{
    const x=start+i*(bw+gap);
    rect(s,x,1.9,bw,0.82,i===4?C.goldPale:C.white,0.1,i===4?C.gold:C.line);
    txt(s,t,x+0.08,2.12,bw-0.16,0.35,{fontSize:11.5,bold:true,color:C.navy,align:'center'});
    if(i<6) txt(s,'›',x+bw+0.035,2.15,0.17,0.28,{fontSize:19,bold:true,color:C.teal,align:'center'});
  });
  card(s,0.62,3.35,3.85,2.0,'Human control','Users confirm structured inputs, quote values and exceptions. Approvers retain explicit decision rights.',C.teal,13);
  card(s,4.75,3.35,3.85,2.0,'Auditability','Keep versioned quote snapshots, role-gated actions, reason codes and event timestamps.',C.green,13);
  card(s,8.88,3.35,3.85,2.0,'AI boundary','No AI price setting, automatic approval or unreviewed extraction. Document AI remains a later hypothesis.',C.gold,13);
  txt(s,'The current implementation is a local demonstration. It has no ERP integration, production identity, live AI service or customer data.',0.8,5.85,11.7,0.4,{fontSize:11.5,color:C.muted,italic:true,align:'center'});
}
// 9 — measurement
{
  const s=base('Measure process performance and product adoption as two separate questions.','PILOT / EXPERIMENT DESIGN');
  card(s,0.65,1.55,5.85,3.6,'Operational outcomes','• Median and P75 RFQ cycle (working-time rules explicit)\n• Stage duration and complete-case coverage\n• Approval wait and reassignment rate\n• Quote rework / revision rate\n• Price-parity exceptions\n• Capacity-confirmed recovered orders',C.teal,13.5);
  card(s,6.8,1.55,5.85,3.6,'Product / control outcomes','• Task completion without moderator help\n• Time-on-task and error rate\n• Active RFQ owners by week (instrumented, not inferred)\n• Queue visibility usage and stale RFQs\n• Permission failures / control breaches\n• Audit and event completeness',C.green,13.5);
  rect(s,0.75,5.55,11.85,0.72,C.goldPale,0.1,C.goldPale);
  txt(s,'Pilot design rule: pre-set denominator, baseline, guardrails and stop criteria before reading results. Synthetic events do not count as a pilot.',1.0,5.77,11.35,0.28,{fontSize:13,bold:true,color:'805B00',align:'center'});
}
// 10 — cash reality
{
  const s=base('Operating payback is attractive in the base case; cash payback is much slower.','FINANCE / RISK');
  metric(s,0.7,1.55,3.6,'₹8L','One-time implementation fee','PROPOSAL INPUT');
  metric(s,4.85,1.55,3.6,'₹2L','Annual operating run cost','ASSUMPTION');
  metric(s,9.0,1.55,3.6,'4.9 months','Operating payback after run cost','PRE-TAX / PRE-WC');
  card(s,0.7,3.05,5.75,2.45,'Full model cash view','23.6-month cash payback after tax and working capital under the existing model assumptions. Deepest cash need: ₹14.8L. IRR: 75.8% with working-capital release; 43.0% without release.',C.teal,13.5);
  card(s,6.8,3.05,5.75,2.45,'Finance controls','Do not add the ₹21.06L theoretical capacity value to recovered contribution. Do not call the operating proxy EBITDA or free cash flow. Challenge tax, working capital, ramp-up and the 25% win-back.',C.gold,13.5);
  txt(s,'The 97% positive-NPV figure in an existing Monte Carlo sensitivity refers to the share of selected model scenarios, not a real-world success probability.',0.85,5.85,11.65,0.42,{fontSize:11.5,color:C.red,bold:true,align:'center'});
}
// 11 — market context
{
  const s=base('Industry growth supports the context—but input-cost volatility keeps margin discipline central.','EXTERNAL RESEARCH');
  metric(s,0.72,1.55,3.65,'₹6.74L cr','FY25 India auto-component turnover','ACMA • +9.6% YoY');
  metric(s,4.85,1.55,3.65,'8–10%','ICRA FY27 domestic OEM supply outlook','FORECAST');
  metric(s,8.98,1.55,3.65,'11.0–11.5%','ICRA FY27 OPM outlook','FORECAST');
  card(s,0.72,3.1,5.75,2.35,'Demand context','ACMA FY25 review reports ₹5.70L crore supplies to OEMs and ₹1.92L crore component exports. These are sector totals, not the case firm’s market.',C.teal,13.2);
  card(s,6.82,3.1,5.75,2.35,'Margin watchlist','ICRA flags commodities, energy, logistics, currency and geopolitical uncertainty as variables that can affect FY27 margin trajectory.',C.gold,13.2);
  txt(s,'Peer caution: Motherson and Bharat Forge are large, diversified groups with different product mix, segment and consolidation bases. No SME target margin or trading multiple is inferred.',0.85,5.85,11.6,0.48,{fontSize:11.5,bold:true,color:C.navy,align:'center'});
}
// 12 — Recommendation and gates
{
  const s=base('Approve the evidence sprint. Make the larger investment conditional.');
  card(s,0.65,1.5,5.8,3.75,'Approve now','1. De-identified timestamp trace for at least 10 recent RFQs.\n2. Role-based stakeholder discovery.\n3. Workflow visibility prototype and owner / due-date discipline.\n4. Price-parity test across at least 20 representative part/volume cases.\n5. Business UAT with permission and audit controls.',C.teal,13.5);
  card(s,6.8,1.5,5.8,3.75,'Release next stage only if','• Stage data explains the cycle and supports the selected intervention.\n• Price parity meets the pre-agreed tolerance.\n• No critical/high workflow or permission defect remains.\n• Plant capacity can fulfil recovered demand.\n• Business owner accepts the workflow and measurement plan.\n• Economics remain positive in the agreed downside case.',C.green,13.5);
  rect(s,0.75,5.65,11.75,0.72,C.navy,0.1,C.navy);
  txt(s,'DECISION: MEASURE → PILOT → REVIEW → SCALE OR STOP',1.0,5.86,11.25,0.28,{fontSize:16,bold:true,color:C.white,align:'center'});
}
// 13 — sources and limitations
{
  const s=base('Sources and boundaries','APPENDIX');
  txt(s,'External research',0.65,1.4,2.4,0.26,{fontSize:15,bold:true,color:C.navy});
  bullets(s,[
    'ACMA, FY2025 / FY2024 industry performance review (8 Jul 2025): https://www.acma.in/pdf/Ind%20Presentation%20FY25.pdf',
    'ICRA, India auto-components FY27 outlook (28 Sep 2026): https://www.icra.in/Research/ViewResearchReport/premiumisation-and-richer-vehicle-content-to-support-growth-inflationary-headwinds-to-weigh-on-profitability/7126',
    'Samvardhana Motherson International Ltd, FY2024–25 Annual Report: https://www.motherson.com/storage/Corporate%20Announcements/FY2025-26/Disclosure_Annual_Report_FY_2024-25-06Aug.pdf',
    'Bharat Forge Ltd, Integrated Annual Report FY2024–25: https://www.bharatforge.com/AR2025/pdf/boards-report.pdf'
  ],0.72,1.8,11.85,0.58,10.5);
  line(s,0.68,4.4,11.9,C.line,1);
  txt(s,'Case / model boundaries',0.65,4.62,3.2,0.25,{fontSize:15,bold:true,color:C.navy});
  bullets(s,[
    'Manufacturer, brief and RFQ economics are hypothetical; no customer or production dataset is present.',
    'Win-back, run cost, investment and working-capital assumptions are explicit; model outputs are not realised benefits.',
    'The app runs locally; no hosted deployment, ERP integration, real discovery, business UAT or pilot has occurred.',
    'All external source figures require refresh before reuse. Peer metrics are not treated as like-for-like valuation comparables.'
  ],0.72,5.0,11.85,0.43,10.5);
}

pptx.writeFile({ fileName: 'docs/consulting/MarginLadder_Executive_Recommendation.pptx' });
