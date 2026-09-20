# LearnFlow AI - Pre-Event Checklist

## 48 Hours Before

### Code & Infrastructure
- [ ] Pull latest code from GitHub
- [ ] Test locally: `python -m uvicorn web.learnflow:app --port 8001`
- [ ] Verify all routes working (home, start, /run/)
- [ ] Check database: `ls -la learnflow.db`
- [ ] Confirm PDF upload works
- [ ] Test progress bar displays correctly
- [ ] Verify "Learn Next Topic" button appears on mastery

### Environment Setup
- [ ] `.env` file has OPENROUTER_API_KEY set
- [ ] API key tested and working
- [ ] Database cleared (fresh for demo): `rm learnflow.db`
- [ ] All dependencies installed: `pip list | grep fastapi`
- [ ] No port conflicts on 8001

### Documentation
- [ ] README.md up to date
- [ ] RUN.md commands tested
- [ ] JUDGES_SCRIPT.md memorized
- [ ] PITCH_2MIN.md ready to deliver
- [ ] All files pushed to GitHub

---

## 24 Hours Before

### Presentation
- [ ] Practice 2-minute pitch (time yourself)
- [ ] Practice live demo (dry run, 3-5 minutes)
- [ ] Prepare answers to FAQ
- [ ] Print judges statement
- [ ] Print pitch script
- [ ] Have backup: PDF of slides/script on phone

### Technical Backup
- [ ] Backup screenshots of working app
- [ ] Record short video of demo (in case live demo fails)
- [ ] Have offline version of presentation
- [ ] Test screen sharing (if virtual event)
- [ ] Test audio/video (if presentation requires it)

### Content Check
- [ ] Problem statement is clear
- [ ] Solution is understandable in 2 minutes
- [ ] Tech stack is correct
- [ ] Status is honest (local dev, not deployed)
- [ ] Impact statement resonates

---

## Day Before

### Final Testing
- [ ] Fresh database: `rm learnflow.db` and restart
- [ ] Create test topic: "Photosynthesis" or similar
- [ ] Complete 1 full cycle end-to-end
- [ ] Verify progress bar shows 1/3
- [ ] Answer follow-up correctly → mastery
- [ ] Click "Learn Next Topic" → goes to home
- [ ] Check history displays date + topic correctly

### System Preparation
- [ ] Close all unnecessary apps before event
- [ ] Update operating system if needed
- [ ] Charge laptop fully
- [ ] Backup power bank ready
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Close other terminals/windows

### Presentation Material
- [ ] Print 3 copies of judges statement
- [ ] Print 2 copies of pitch script
- [ ] Export RUN.md to PDF
- [ ] Save GitHub link: https://github.com/kanishpravin/learnflow-ai
- [ ] Save demo URL: http://127.0.0.1:8001 (write it down)

### Mental Prep
- [ ] Read through script 2-3 times
- [ ] Practice opening line: "LearnFlow AI diagnoses understanding"
- [ ] Practice closing: ask for feedback/partnership/investment
- [ ] Visualize successful demo
- [ ] Review FAQ answers
- [ ] Sleep well

---

## Morning Of Event

### Technical
- [ ] Start laptop early (30+ min before)
- [ ] Start server: `python -m uvicorn web.learnflow:app --port 8001`
- [ ] Confirm app loads: http://127.0.0.1:8001
- [ ] Test 1 quick cycle (don't use main demo data yet)
- [ ] Keep server running in background
- [ ] Have terminal visible but minimized

### Environment
- [ ] Quiet room for presentation
- [ ] Good internet (if streaming/video needed)
- [ ] Monitor/screen at good angle
- [ ] Water nearby (hydrate before speaking)
- [ ] Phone on silent

### Personal
- [ ] Professional appearance
- [ ] No distracting accessories
- [ ] Comfortable clothing
- [ ] Minimal caffeine (avoid jitters)
- [ ] Calm mindset

### Materials
- [ ] Pitch script (printed, in hand)
- [ ] Judges statement (printed)
- [ ] GitHub repo link (written down)
- [ ] RUN.md (printed or on phone)
- [ ] Contact info ready to share

---

## Just Before Presentation

### Code Check (5 min before)
- [ ] Server still running: `http://127.0.0.1:8001` ✓
- [ ] Database exists: `learnflow.db` present ✓
- [ ] Fresh data ready for demo ✓
- [ ] Terminal visible but not distracting ✓
- [ ] No error messages in terminal ✓

### Mental Check
- [ ] Calm breathing (4 counts in, 4 out)
- [ ] Remember: judges want you to succeed
- [ ] You've practiced this
- [ ] Focus on problem → solution → impact
- [ ] If demo fails, have video backup

### Setup Check
- [ ] Browser open to home page
- [ ] Script printed and visible
- [ ] Judges have pen/paper
- [ ] Camera/screen share working (if needed)
- [ ] Microphone working

---

## During Presentation

### Opening (30 sec)
- [ ] Introduce yourself
- [ ] Say opening line: "LearnFlow AI diagnoses understanding"
- [ ] Make eye contact

### Problem (20 sec)
- [ ] State 3 problems clearly
- [ ] Don't rush
- [ ] Pause for effect

### Solution (60 sec)
- [ ] Walk through 8-step flow
- [ ] Use simple language
- [ ] Refer to script if needed

### Demo (5 min) - If attempted live:
1. Go to home page
2. Enter topic: "Photosynthesis"
3. Paste notes about photosynthesis
4. Click "Begin lesson"
5. Read lesson
6. Type explanation (deliberate gap)
7. Click "Evaluate"
8. Show gap detection + feedback
9. Confirm diagnosis
10. Answer follow-up
11. Show mastery screen + progress bar
12. Click "Learn Next Topic"

**If demo fails:** 
- "Let me show you this video I prepared" (play backup video)
- Continue with slides/script
- Stay calm

### Technical Stack (15 sec)
- [ ] FastAPI, OpenRouter, SQLite
- [ ] Don't go too deep
- [ ] "Production-ready architecture"

### Status (15 sec)
- [ ] "Working locally, core flows validated"
- [ ] "Not deployed yet—prioritizing validation"
- [ ] "Ready to deploy in <1 hour"

### Impact (15 sec)
- [ ] Students know what they understand
- [ ] Teachers see concept gaps
- [ ] Measurable, personal learning

### Closing (20 sec)
- [ ] "This is learning that understands understanding"
- [ ] Ask: "Questions?"
- [ ] Have GitHub link ready
- [ ] Offer: "Happy to do live demo or discuss further"

---

## FAQ - Quick Answers Ready

**Q: Why not deployed yet?**
A: "Validating core flows first. Deployment ready in 1 hour if needed."

**Q: How is this different from Quizlet/Khan?**
A: "We diagnose *understanding*, not content delivery. Gap detection at concept level."

**Q: What if AI makes wrong diagnosis?**
A: "Student confirms diagnosis before feedback. Prevents cascade errors."

**Q: Can this work offline?**
A: "Yes. Falls back to formatted notes. No forced internet dependency."

**Q: Timeline to launch?**
A: "Validation phase: 2-3 weeks. Then deploy. Launch ready by [date]."

**Q: What's your unfair advantage?**
A: "Pedagogy. Human gate + concept gap detection + mastery-based progression."

---

## If Demo Fails (Backup Plan)

**Option A: Video Backup**
- Have 2-min video recorded showing full cycle
- Play instead of live demo
- Say: "Let me show you this quick recording"

**Option B: Screenshots**
- Have screenshots of each step
- Walk through them
- Click through screenshots manually

**Option C: Description**
- Skip demo entirely
- Describe flow from script
- Offer: "I can show you live after presentation"

**Never:** Panic or apologize excessively. Move forward.

---

## After Presentation

### Immediately After
- [ ] Collect judge feedback
- [ ] Note any questions you couldn't answer
- [ ] Get contact info if interested
- [ ] Offer GitHub link

### Follow Up (Within 24 hours)
- [ ] Send GitHub repo link
- [ ] Send RUN.md instructions
- [ ] Thank you message
- [ ] Offer live demo if they want

### Document Feedback
- [ ] Note what went well
- [ ] Note what to improve
- [ ] Update presentation for next event

---

## Success Criteria

✅ **Delivered 2-min pitch clearly**  
✅ **Showed working demo or video**  
✅ **Explained problem → solution → impact**  
✅ **Answered judge questions**  
✅ **Gave GitHub repo link**  
✅ **Remained calm if issues occurred**  

---

## Contact Info Ready To Share

**GitHub:** https://github.com/kanishpravin/learnflow-ai  
**Email:** [your email]  
**Phone:** [your phone]  
**LinkedIn:** [your LinkedIn]  

Print these on a business card or write on paper.

---

## Final Reminders

- You built something real. It works.
- Judges want you to succeed.
- If demo fails, you still have script and video.
- Calm + clear > fast + perfect.
- This is learning that understands understanding.

**You've got this. 🚀**