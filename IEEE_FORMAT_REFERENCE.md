# IEEE LaTeX Reference - Quick Commands & Tips

## 📌 IMPORTANT FILES IN YOUR PROJECT

```
research_paper.tex                    ← Main LaTeX document
LATEX_COMPILATION_GUIDE.md            ← How to compile
AUTHOR_CUSTOMIZATION_TEMPLATE.md      ← How to customize authors
IEEE_FORMAT_REFERENCE.md              ← This file - quick reference
```

---

## 🔤 BASIC LaTeX COMMANDS

### Text Formatting
```latex
\textbf{bold text}              → bold text
\textit{italic text}            → italic text
\texttt{typewriter/code}        → typewriter/code
\underline{underlined}          → underlined
```

### Math Mode
```latex
\(x^2 + y^2 = z^2\)         → inline equation
\[x^2 + y^2 = z^2\]         → display equation
\begin{equation}
    E = mc^2
\end{equation}               → numbered equation
```

### Symbols
```latex
\alpha, \beta, \gamma        → Greek letters α, β, γ
\geq, \leq, \neq             → ≥, ≤, ≠
\times, \div                 → ×, ÷
\infty                       → ∞
\approx, \equiv              → ≈, ≡
```

---

## 📋 PAPER STRUCTURE COMMANDS

### Sections
```latex
\section{Main Section}           → Section 1. Main Section
\subsection{Subsection}          → 1.1 Subsection
\subsubsection{Subsubsection}    → 1.1.1 Subsubsection
```

### Lists
```latex
% Unordered list
\begin{itemize}
    \item First point
    \item Second point
\end{itemize}

% Ordered list
\begin{enumerate}
    \item First point
    \item Second point
\end{enumerate}
```

### Tables
```latex
\begin{table}[h]
    \centering
    \caption{Table Title}
    \begin{tabular}{|l|c|r|}
        \hline
        Left & Center & Right \\
        \hline
    \end{tabular}
\end{table}
```

### Figures
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\linewidth]{image.png}
    \caption{Figure description}
    \label{fig:label}
\end{figure}

% References
See Figure \ref{fig:label}
```

---

## 📚 CITATION COMMANDS

### In-Text Citations
```latex
\cite{ref1}                  → [1]
\cite{ref1,ref2,ref3}       → [1]–[3]
\cite{ref1,ref5,ref3}       → [1], [3], [5]
```

### Bibliography Entry Formats

**Journal:**
```latex
\bibitem{labelX}
Firstname Lastname and Another Author,
``Article Title,''
\textit{IEEE Transactions on Field}, vol. X, no. Y, pp. XX–YY, Mon. Year, doi: XX.XXXX/XXXXX.
```

**Conference:**
```latex
\bibitem{labelX}
Firstname Lastname,
``Paper Title,''
in \textit{Proc. Conference Name}, City, Country, Year, pp. XX–YY, doi: XX.XXXX/XXXXX.
```

**Book:**
```latex
\bibitem{labelX}
Author Name and Another Author,
\textit{Book Title},
Edition ed. Publisher, City, Country, Year, ch. X, pp. XX–YY.
```

---

## 🎨 IEEE FORMAT SPECIFICS

### Document Structure (for conferences)
```
1. Title (centered, 14pt bold)
2. Authors (centered, names with affiliations)
3. Abstract (150-200 words, italic)
4. Keywords (4-6 terms)
5. Introduction
6. Main Content (2-4 sections)
7. Experimental Results
8. Discussion
9. Conclusion
10. Acknowledgments
11. References
```

### Page Layout
- Margins: 1 inch (2.54 cm) all sides
- Column format: Two columns (conference format)
- Font: Times Roman, 10pt body, 11pt headers
- Line spacing: Single
- Page limit: Usually 6-8 pages

### Numbering Style
- Sections: 1., 2., 3., etc.
- Subsections: 1.1, 1.2, 2.1, etc.
- Equations: (1), (2), (3), etc.
- Figures/Tables: Fig. 1, Table 1, etc.
- References: [1], [2], [3], etc.

---

## ✍️ YOUR PAPER - KEY SECTIONS

### Abstract Section (Already Written)
Located at: Line 50-60
- Already includes your project metrics
- Length: ~200 words (perfect)
- Includes: Problem, solution, results

**Example format if you need to rewrite:**
```latex
\begin{abstract}
This paper presents [what you did]. 
We achieve [key results]. 
The system processes [how many samples]. 
Our model shows [performance metrics]. 
This work contributes by [significance].
\end{abstract}
```

### Introduction Section (Already Written)
Located at: Line 68-100
- Sets context for problem
- Motivates research
- Lists contributions
- Outlines paper structure

### Results Section (Already Written)
Located at: Line 182-220
- Table with metrics (Line 196)
- Confusion matrix (Line 209)
- Performance analysis (Line 220+)

---

## 🔍 COMMON LaTeX ERRORS & FIXES

| Error | Cause | Fix |
|-------|-------|-----|
| Undefined control sequence | Wrong command name | Check spelling, add backslash |
| Missing \$ inserted | Math mode not activated | Wrap math in \$ or \[ \] |
| Illegal character | Special char not escaped | Use \%, \$, \\, \&, \#, \_, \{, \} |
| Missing { or } | Unmatched braces | Count opening/closing braces |
| Citation undefined | Reference not in bib | Add \bibitem or check label |

---

## 📊 YOUR PAPER METRICS (DO NOT CHANGE)

### Model Performance
```latex
Testing Accuracy: 87.94\%
Sensitivity: 89.39\%
Specificity: 85.00\%
ROC-AUC: 0.9502
```

### Dataset
```latex
Training Samples: 40,000
Test Samples: 10,000
Features: 41
Classes: Binary (Benign/Attack)
```

### Real-Time Performance
```latex
Processing Capacity: 24,000+ samples
Samples/Test: 1,000
Detection Rate: 64.6\%
Latency: 0.3 seconds per packet
```

All these are already in your paper!

---

## ☑️ EDITING CHECKLIST

Before compiling final PDF:

- [ ] All author names corrected
- [ ] All emails valid
- [ ] University names accurate
- [ ] Affiliation details complete
- [ ] No "Author Name" or "[Name]" placeholders remain
- [ ] Acknowledgments personalized
- [ ] No red squiggly lines (spell check)
- [ ] All citations present and formatted
- [ ] Equations properly numbered
- [ ] Tables have clear captions
- [ ] Figures/diagrams appropriate
- [ ] Abstract is 150-200 words
- [ ] Keywords are 4-6 terms
- [ ] Conclusion summarizes findings

---

## 🚀 QUICK START - EDIT & COMPILE

### Step 1: Edit Authors (5 minutes)
```bash
# Open research_paper.tex in notepad++/VSCode
# Find line 20: \author{\IEEEauthorblockN{
# Replace author names and emails
# Save file
```

### Step 2: Compile to PDF (2 minutes)
```powershell
# In PowerShell:
cd 'c:\Users\darsh\.gemini\antigravity\scratch\IDS_Project'
pdflatex research_paper.tex
```

### Step 3: Check Output (1 minute)
```bash
# Output file: research_paper.pdf
# Opens in default PDF viewer
# Check for errors in template
```

---

## 📖 EQUATION EXAMPLES ALREADY IN YOUR PAPER

### Feature Normalization (Line 147)
```latex
x_{\text{scaled}} = \frac{x - \mu}{\sigma}
```

### Logistic Regression (Line 168)
```latex
P(y=1|x) = \frac{1}{1 + e^{-(\beta_0 + \sum_{i=1}^{n}\beta_i x_i)}}
```

### Decision Threshold (Line 172)
```latex
\text{Alert}(x) = \begin{cases}
1 & \text{if } P(y=1|x) > 0.5 \\
0 & \text{otherwise}
\end{cases}
```

---

## 🎯 YOUR IEEE COMPLIANCE

Your paper ALREADY includes:

✅ IEEE document class (IEEEtran)
✅ Proper section structure
✅ Correct citation format
✅ Mathematical equations with numbering
✅ Table and figure environments
✅ Proper abstract format
✅ Keywords section
✅ Double-column layout option
✅ References section with 18 citations
✅ Author and affiliation blocks

---

## 💾 FILE MANAGEMENT

### Keep These Files:
- `research_paper.tex` - Main document
- `research_paper.pdf` - Generated output

### Auxiliary Files (Generated, can delete):
- `research_paper.aux` - Auxiliary info
- `research_paper.log` - Compilation log
- `research_paper.out` - Outline
- `research_paper.fdb_latexmk` - Cache

### Cleanup Command:
```powershell
Get-ChildItem -Filter "research_paper.*" -Exclude "*.tex", "*.pdf" | Remove-Item
```

---

## 🔗 USEFUL LINKS

- **IEEE Author Guidelines**: https://www.ieee.org/content/dam/ieee-org/ieee/web/org/pubs/author_guidelines.pdf
- **Citation Examples**: https://www.ieee.org/content/dam/ieee-org/ieee/web/org/pubs/information-for-ieee-journal-authors.pdf
- **LaTeX Beginners**: https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes
- **IEEE Templates**: https://www.ieee.org/conferences/publishing/templates.html
- **Symbol Reference**: https://mirror.ctan.org/fonts/comprehensive/comprehensive.pdf

---

## 💡 PRO TIPS

1. **Use Overleaf**: Most hassle-free way to compile IEEE LaTeX documents
2. **Keep Backup**: Save original `research_paper.tex` before major edits
3. **Check References**: Verify all citations exist in bibliography
4. **Consistent Formatting**: Don't manually modify section numbering
5. **PDF Preview**: Always check PDF output, not just LaTeX code
6. **Colleague Review**: Have someone proofread before final submission
7. **Conference Requirements**: Check specific venue requirements before submission

---

## ✅ READY TO GO!

Your LaTeX document is:
- ✅ IEEE Format compliant
- ✅ Properly structured
- ✅ Contains all required sections
- ✅ Has sample references
- ✅ Includes your project metrics
- ✅ Ready for customization
- ✅ Compiles without errors

**Next Steps:**
1. Update author information
2. Customize affiliation details
3. Add biographical information (optional)
4. Compile to PDF
5. Submit to appropriate venue
