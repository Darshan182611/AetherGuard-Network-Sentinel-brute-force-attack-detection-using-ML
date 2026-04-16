# IEEE LaTeX Research Paper - Customization Template

## FILL IN YOUR INFORMATION BELOW

### PRIMARY AUTHOR (Author 1)
```
Name: Darshan Kumar
Affiliation: Department of Computer Science and Engineering
University: [Your University/Institution Name]
City: [Your City]
Country: [Your Country]
Email: darshan182611@email.com
```

### SECONDARY AUTHOR (Author 2)
```
Name: [Your Co-Author Name]
Affiliation: [Department Name]
University: [University/Institution Name]
City: [City]
Country: [Country]
Email: [Email Address]
```

### TERTIARY AUTHOR (Author 3)
```
Name: [Your Advisor/Third Author]
Affiliation: [Department/Lab Name]
University: [University/Institution Name]
City: [City]
Country: [Country]
Email: [Email Address]
```

---

## LATEX CODE TEMPLATE - UPDATE YOUR research_paper.tex

### Step 1: Update Title Page

Replace Lines 20-37 with your information:

```latex
\title{Real-Time Network Intrusion Detection System Using\\
Machine Learning Classification with Neural Network Enhancement}

\author{\IEEEauthorblockN{Darshan Kumar\IEEEauthorrefmark{1}, 
Dr. Your Co-Author Name\IEEEauthorrefmark{2},
Prof. Your Advisor Name\IEEEauthorrefmark{3}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}Department of Computer Science and Engineering,
Your University Name, Your City, Your Country\\
Email: darshan182611@email.com}
\IEEEauthorblockA{\IEEEauthorrefmark{2}School of Information Technology,
Your University Name, Your City, Your Country\\
Email: coauthor@email.com}
\IEEEauthorblockA{\IEEEauthorrefmark{3}Cybersecurity Research Lab,
Your University Name, Your City, Your Country\\
Email: advisor@email.com}}
```

### Step 2: Update Acknowledgment Section

Replace Lines 280-285 with:

```latex
\section*{Acknowledgment}

The authors acknowledge [Your Research Lab Name], [Your University Name] 
for providing computational resources. Special thanks to Dr. [Advisor Name] 
for invaluable guidance and mentorship. This work was supported by 
[Funding Organization/Grant Number, if applicable].
```

### Step 3: Add Your Biographical Notes (Optional)

Add after \end{thebibliography}:

```latex
\begin{IEEEbiography}{Darshan Kumar}
received the B.Tech. degree in Computer Science and Engineering from 
[University Name], in 20XX. His research interests include machine learning, 
cybersecurity, and network intrusion detection systems.
\end{IEEEbiography}

\begin{IEEEbiography}{Dr. Your Co-Author Name}
received the Ph.D. degree in Computer Science from [University Name] 
in 20XX. He is currently an Assistant Professor at [University Name]. 
His research focuses on network security and machine learning applications.
\end{IEEEbiography}

\begin{IEEEbiography}{Prof. Your Advisor Name}
received the Ph.D. degree from [University Name] in 20XX. 
He is a Professor and Head of the Cybersecurity Research Lab. 
His research interests include intrusion detection, anomaly detection, 
and AI-based security systems.
\end{IEEEbiography}
```

---

## REFERENCE CUSTOMIZATION

### Adding Your Institutional References

If your university/organization has published papers, add them:

```latex
\bibitem{ref19}
[Your Name et al.],
``Your Previous Research Title,''
\textit{Conference/Journal Name}, [Year].

\bibitem{ref20}
[Advisor Name] and [Co-worker],
``Related Work in Your Field,''
\textit{IEEE Transactions on [Field]}, vol. X, no. X, pp. X-X, [Month Year].
```

### Citation Examples by Type

**Journal Article:**
```latex
\bibitem{refX}
J. Author, ``Title of article,'' 
\textit{Abbreviated Journal Title}, vol. X, no. X, pp. XXX–XXX, Abbrev. Month and Year, 
doi: XX.XXXX/######.
```

**Conference Paper:**
```latex
\bibitem{refX}
J. Author, ``Title of conference paper,'' 
in \textit{Abbreviated Conference Title}, Abbrev. City, 
Abbrev. State, Abbrev. Country, YYYY, pp. XXX–XXX, doi: XX.XXXX/######.
```

**Book:**
```latex
\bibitem{refX}
J. Author and Second Author, 
\textit{Title of Book} (Edition), 
Publisher Name, Pubisher City, Abbrev. State, Abbrev. Country, 
Year, ch. X, pp. XXX–XXX, doi: XX.XXXX/######.
```

---

## KEY CUSTOMIZATIONS SUMMARY

| Element | Location | Update Required |
|---------|----------|-----------------|
| Title | Line 15 | Optional - keep as is or customize |
| Author 1 Name | Line 20 | Keep: Darshan Kumar |
| Author 2 Name | Line 21 | Replace with actual name |
| Author 3 Name | Line 22 | Replace with actual name |
| Author 1 Email | Line 25 | Keep or update |
| Author 2 Email | Line 27 | Add email |
| Author 3 Email | Line 29 | Add email |
| University/Org | Lines 24-30 | Replace with your institutions |
| Acknowledgment | Line 282 | Personalize with your supervisors |
| References | Line 313+ | Keep as provided or add yours |
| Biographical Info | After bib | Optional - add author bios |

---

## EXAMPLE - COMPLETE AUTHOR BLOCK

```latex
\author{\IEEEauthorblockN{Darshan Kumar\IEEEauthorrefmark{1}, 
Dr. Rajesh Sharma\IEEEauthorrefmark{2},
Prof. Anil Kumar Sharma\IEEEauthorrefmark{3}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}Department of Computer Science and Engineering,
Indian Institute of Technology Delhi, New Delhi, India\\
Email: darshan@iiitd.ac.in}
\IEEEauthorblockA{\IEEEauthorrefmark{2}School of Information Technology,
IIIT Delhi, New Delhi, India\\
Email: rsharma@iiitd.ac.in}
\IEEEauthorblockA{\IEEEauthorrefmark{3}Cybersecurity Research Lab,
Delhi University, New Delhi, India\\
Email: asharma@du.ac.in}}
```

---

## IEEE GUIDELINES CHECKLIST

- [ ] All author names and affiliations correct
- [ ] Email addresses valid and current
- [ ] Abstract between 150-250 words
- [ ] Keywords 4-6 relevant terms
- [ ] Section headings follow IEEE style
- [ ] References 20+ for comprehensive paper
- [ ] All citations in IEEE format
- [ ] No plagiarism (use proper citations)
- [ ] Grammar proofread
- [ ] Compliance with 6-8 page limit for conferences

---

## COMPILATION TEST

After updating, test compile with:

```powershell
# PowerShell command
pdflatex research_paper.tex

# Check for errors
if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilation successful!"
} else {
    Write-Host "Compilation failed - check errors above"
}
```

---

## QUICK CHECKLIST - Things NOT to Change

- [ ] \documentclass{IEEEtran}
- [ ] \usepackage commands
- [ ] \maketitle command
- [ ] Section structures
- [ ] \begin{thebibliography} format
- [ ] IEEE citation style
- [ ] Core mathematical equations

---

## FINAL STEP: EXPORT & SUBMIT

Once customized and compiled:

1. **Generate PDF**: `pdflatex research_paper.tex`
2. **Output File**: `research_paper.pdf`
3. **Rename (Optional)**: 
   - `IDS_Detection_System_2026.pdf`
   - Or per conference requirements
4. **Submit to**: 
   - Your university for thesis/project
   - Conference for publication
   - Journal for review

---

## SUPPORT RESOURCES

- IEEE LaTeX Templates: https://www.ieee.org/conferences/publishing/templates.html
- Overleaf Help: https://www.overleaf.com/learn
- LaTeX Symbol List: https://www.ctan.org/pkg/comprehensive
- BibTeX Citation Format: http://www.bibtex.org/
