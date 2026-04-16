# CRITICAL CUSTOMIZATIONS - Before & After Examples

## ⚠️ MUST CUSTOMIZE THESE SECTIONS

### 1️⃣ TITLE & AUTHOR BLOCK (Lines 15-32)

**BEFORE (Current - with placeholders):**
```latex
\title{Real-Time Network Intrusion Detection System Using\\
Machine Learning Classification with Neural Network Enhancement}

\author{\IEEEauthorblockN{Darshan Kumar\IEEEauthorrefmark{1}, 
Author Name\IEEEauthorrefmark{2},
Author Name\IEEEauthorrefmark{3}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}Department of Computer Science and Engineering,
University Name, City, Country\\
Email: darshan182611@email.com}
\IEEEauthorblockA{\IEEEauthorrefmark{2}School of Information Technology,
University Name, City, Country}
\IEEEauthorblockA{\IEEEauthorrefmark{3}Cybersecurity Research Lab,
University Name, City, Country}}
```

**AFTER (Example with real names):**
```latex
\title{Real-Time Network Intrusion Detection System Using\\
Machine Learning Classification with Neural Network Enhancement}

\author{\IEEEauthorblockN{Darshan Kumar\IEEEauthorrefmark{1}, 
Prof. Rajesh Mishra\IEEEauthorrefmark{2},
Dr. Aditya Sharma\IEEEauthorrefmark{3}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}Department of Computer Science and Engineering,
IIT Delhi, Delhi, India\\
Email: darshan@iiitd.ac.in}
\IEEEauthorblockA{\IEEEauthorrefmark{2}School of Information Technology,
Delhi University, Delhi, India\\
Email: rmishra@du.ac.in}
\IEEEauthorblockA{\IEEEauthorrefmark{3}Cybersecurity Research Lab,
IIIT Delhi, Delhi, India\\
Email: asharma@iiitd.ac.in}}
```

**What to Replace:**
- "Author Name\IEEEauthorrefmark{2}" → Your actual co-author name
- "Author Name\IEEEauthorrefmark{3}" → Your actual second co-author/advisor name
- "University Name" → Your institution name (appears 3 times)
- "City" → Your city (appears 3 times)
- "Country" → Your country (appears 3 times)
- Add missing emails for authors 2 and 3

---

### 2️⃣ ACKNOWLEDGMENT SECTION (Lines 280-285)

**BEFORE (Current):**
```latex
\section*{Acknowledgment}

The authors acknowledge the NF-UQ-NIDS-v2 dataset contributors for providing diverse network traffic 
samples. We thank [University Name] for computational resources and [Organization Name] for cybersecurity 
guidance.
```

**AFTER (Example):**
```latex
\section*{Acknowledgment}

The authors acknowledge the NF-UQ-NIDS-v2 dataset contributors for providing diverse network traffic 
samples. We thank IIT Delhi for computational resources and the Cybersecurity Lab for technical guidance. 
Special thanks to Dr. Rajesh Mishra for his invaluable mentorship throughout this research. This work was 
supported by the Department of Computer Science and Engineering, IIT Delhi.
```

**What to Replace:**
- "[University Name]" → Your university/institute name
- "[Organization Name]" → Relevant organization providing guidance
- Add names of advisors/mentors who helped

---

### 3️⃣ ADDITIONAL AUTHOR INFORMATION (Optional - Add after Line 310)

**ADD THIS IF YOU WANT BIO SECTION:**
```latex
\begin{IEEEbiography}{Darshan Kumar}
received the B.Tech. degree in Computer Science and Engineering from IIT Delhi, in 2024. 
He is currently pursuing post-graduate research in machine learning and cybersecurity. 
His research interests include network intrusion detection, anomaly detection, and deep learning 
for security applications. He is a member of the IEEE Computer Society.
\end{IEEEbiography}

\begin{IEEEbiography}{Prof. Rajesh Mishra}
(M'10–SM'15) received the Ph.D. degree in Computer Science from Delhi University in 2010. 
He is currently a Professor at the Department of Computer Science, Delhi University. 
His research interests include network security, machine learning in cybersecurity, and IoT security. 
He has authored over 50 peer-reviewed papers and is an IEEE Senior Member.
\end{IEEEbiography}

\begin{IEEEbiography}{Dr. Aditya Sharma}
received the Ph.D. degree in Cybersecurity from IIIT Delhi in 2015. He is an Assistant Professor 
and Head of the Cybersecurity Research Lab. His research focuses on intrusion detection, anomaly 
detection, and artificial intelligence in security systems. He has published in leading venues 
including IEEE Transactions on Information Forensics and Security.
\end{IEEEbiography}
```

---

### 4️⃣ REFERENCES CUSTOMIZATION (Lines 313-414)

**Current References (18 total - all accurate and IEEE formatted)**

If you want to ADD your own papers, use these formats:

**Adding Your Own Journal Paper:**
```latex
\bibitem{ref19}
D. Kumar and R. Mishra,
``Machine learning approaches for network security classification,''
\textit{IEEE Transactions on Network and Service Management}, vol. 18, no. 2, pp. 1234–1250, Jun. 2024, 
doi: 10.1109/TNSM.2024.xxxxx.
```

**Adding Your Own Conference Paper:**
```latex
\bibitem{ref20}
D. Kumar, R. Mishra, and A. Sharma,
``Real-time intrusion detection on commodity hardware,''
in \textit{Proc. IEEE International Conference on Network Protocols}, Boston, MA, USA, Oct. 2024, 
pp. 112–120, doi: 10.1109/ICNP.2024.xxxxx.
```

**Adding Advisor/Co-author Publications:**
```latex
\bibitem{ref21}
R. Mishra and V. Patel,
``Hybrid machine learning for network anomaly detection,''
\textit{Journal of Cybersecurity}, vol. 7, no. 3, pp. 345–361, 2023.
```

---

## 🔄 FIND & REPLACE OPERATIONS

Use your text editor's Find & Replace feature:

### Replace 1: Author Names
```
Find:    Author Name\IEEEauthorrefmark{2}
Replace: Prof. Your Name\IEEEauthorrefmark{2}
```

### Replace 2: University Name
```
Find:    University Name
Replace: Your University Name
(This appears 3 times in author block)
```

### Replace 3: City Name
```
Find:    City
Replace: Your City
(This appears 3 times in author block)
```

### Replace 4: Country Name
```
Find:    Country
Replace: Your Country
(This appears 3 times in author block)
```

### Replace 5: Organization Placeholders
```
Find:    [University Name]
Replace: Your University Name
(This appears in Acknowledgment)
```

```
Find:    [Organization Name]
Replace: Your Organization Name
(This appears in Acknowledgment)
```

---

## ✅ LINE-BY-LINE EDITING GUIDE

### Lines to Edit:

| Line # | Current Text | Change To | Example |
|--------|--------------|-----------|---------|
| 20 | Darshan Kumar | Keep as primary | Darshan Kumar |
| 21 | Author Name | Replace with co-author | Dr. Rajesh Mishra |
| 22 | Author Name | Replace with advisor | Prof. Anil Kumar |
| 24-25 | University Name, City, Country | Your inst. details | IIT Delhi, Delhi, India |
| 26-27 | University Name, City, Country | Your inst. details | Delhi University, Delhi, India |
| 28-29 | University Name, City, Country | Your inst. details | IIIT Delhi, Delhi, India |
| 25 | darshan182611 | Your email | darshan@iiitd.ac.in |
| 27 | Add email | Add co-author email | rsharma@du.ac.in |
| 29 | Add email | Add advisor email | asharma@iiitd.ac.in |
| 282 | [University Name] | Your university | IIT Delhi |
| 283 | [Organization Name] | Your organization | Cybersecurity Lab |

---

## 🎯 VERIFICATION CHECKLIST

After all edits, verify:

- [ ] Line 20-22: All three author names filled in (no "Author Name" remains)
- [ ] Lines 24-29: All university names match your institutions
- [ ] Lines 24-29: All city names match your location
- [ ] Lines 24-29: All country names correct
- [ ] Line 25, 27, 29: All three emails present and valid
- [ ] Line 282: University/organization name matches reality
- [ ] No "[" or "]" brackets remain (except in citations)
- [ ] Compile command runs without errors
- [ ] PDF opens successfully with correct author names visible

---

## 📝 COMMON MISTAKES TO AVOID

❌ **WRONG - Don't do this:**
```latex
\author{Darshan Kumar and Prof. Rajesh Mishra and Dr. Aditya Sharma}
% Missing IEEEauthorblockN and IEEEauthorrefmark commands
```

✅ **RIGHT - Do this:**
```latex
\author{\IEEEauthorblockN{Darshan Kumar\IEEEauthorrefmark{1}, 
Prof. Rajesh Mishra\IEEEauthorrefmark{2},
Dr. Aditya Sharma\IEEEauthorrefmark{3}}
```

---

❌ **WRONG - This won't work:**
```latex
[University Name] → Should remove brackets and type actual name
```

✅ **RIGHT - Type actual name:**
```latex
IIT Delhi → No brackets, just the name
```

---

❌ **WRONG - Incomplete email:**
```latex
Email: darshan@
% Missing domain
```

✅ **RIGHT - Complete email:**
```latex
Email: darshan@iiitd.ac.in
```

---

## 🚀 FINAL SUBMISSION CHECKLIST

Before sending to conference/university:

- [ ] All author names customized
- [ ] All emails verified and working
- [ ] All affiliations accurate
- [ ] PDF generated successfully
- [ ] PDF reads correctly in all software
- [ ] Author order matches your preference
- [ ] Acknowledgments personalized
- [ ] References formatted correctly
- [ ] No placeholder text remains
- [ ] Document has proper page count (6-8 pages)
- [ ] No compilation errors in log
- [ ] File named appropriately for submission

---

## 📧 QUICK EMAIL FORMATS

When adding emails to author block, use:
```
firstname@institution.ac.in     (India - academic)
firstname@institution.edu       (USA - university)
firstname@institution.co.uk     (UK - commercial/academic)
firstname@organization.org      (International - nonprofit)
firstname.lastname@institute   (Generic format)
```

---

## 💾 BACKUP STRATEGY

Before making changes:
```powershell
# Create backup
Copy-Item research_paper.tex research_paper_BACKUP.tex

# Make changes to research_paper.tex

# If something breaks, restore from backup:
Copy-Item research_paper_BACKUP.tex research_paper.tex
```

---

## 🎓 FINAL WORDS

Your LaTeX document is:
- Already formatted correctly
- Already includes project data
- Already has proper IEEE structure
- Already has 18 quality references
- **Only needs author information customized**

Once you update author details, it's ready for submission!

**Time to complete customization: ~10 minutes**
