# Quarto Drafting Guide

This guide is a quick reference for writing course documents with Quarto.

## Table of Contents

- [0. Working Directory (Read This First)](#0-working-directory-read-this-first)
- [1. General Template (Copy and Paste)](#1-general-template-copy-and-paste)
- [2. How to Add Figures](#2-how-to-add-figures)
- [3. How to Make Tables](#3-how-to-make-tables)
- [4. How to Include Hyperlinks](#4-how-to-include-hyperlinks)
- [5. How to Write Equations (LaTeX syntax)](#5-how-to-write-equations-latex-syntax)
- [6. Render the Document](#6-render-the-document)

## 0. Working Directory (Read This First)

When you run `quarto render draft.qmd`, Quarto looks for files relative to the folder that contains `draft.qmd`.

Simple rule for beginners:

- Keep `draft.qmd`, your data files, and your image files in the same project folder (or in clear subfolders under it).
- Open that folder in VS Code before rendering.

Example:

```text
coding_exercise/
  draft.qmd
  figure1.png
  table1.csv
  data/
    sample.xlsx
```

## 1. General Template (Copy and Paste)

Create a file named `draft.qmd` and paste this template:

```markdown
---
title: "Draft Title"
author: "Your Name"
date: today
format:
  html: default
  pdf: default
---

# Introduction

Write 2-3 sentences about the purpose of this draft.

# Figure Example

![Example figure caption](figure1.png)

# Table Example

| Variable | Value |
|---|---:|
| A | 10 |
| B | 20 |

# Equation Example

Inline equation: $y = a + bx$

Block equation:
$$
\hat{y}_i = \beta_0 + \beta_1 x_i + \varepsilon_i
$$

# Notes

- Point one
- Point two
```

## 2. How to Add Figures

If your image file is in the same folder as `draft.qmd`:

```markdown
![My figure](my_plot.png)
```

If your image is in a subfolder (for example `figures/`):

```markdown
![My figure](figures/my_plot.png)
```

Common error: wrong path. If the image does not appear, check the file name and folder path carefully.

## 3. How to Make Tables

### Option A: Write a simple Markdown table manually

```markdown
| Item | Amount |
|---|---:|
| Apples | 12 |
| Oranges | 8 |
```

### Option B: Convert from Excel (easy workflow)

1. In Excel, open your sheet.
2. Save As `CSV (Comma delimited) (*.csv)`.
3. Use one of these quick methods:
  - Paste values into a Markdown table generator website and copy the Markdown output.
   - Use a small Quarto code chunk to read and print the CSV table.

Useful websites:

- TableConvert: https://tableconvert.com/excel-to-markdown
- TablesGenerator: https://www.tablesgenerator.com/markdown_tables
- ConvertCSV: https://www.convertcsv.com/csv-to-markdown.htm

Example Quarto chunk (Python):

```python
#| label: tbl-sample
#| tbl-cap: "Sample table from CSV"
import pandas as pd
pd.read_csv("table1.csv")
```

Note: For this Python chunk, Python and `pandas` must be installed.

## 4. How to Include Hyperlinks

Use this Markdown format:

```markdown
[Link text](https://example.com)
```

Examples:

```markdown
[Quarto Documentation](https://quarto.org/docs/)
[GitHub](https://github.com)
```

You can also link to files in the same folder:

```html
<a href="setup_pre_course_preparation.md" target="_blank" rel="noopener noreferrer">See the setup guide</a>
```

## 5. How to Write Equations (LaTeX syntax)

Use `$...$` for inline equations:

```markdown
The demand function is $Q_d = a - bP$.
```

Use `$$...$$` for display equations:

```markdown
$$
GDP = C + I + G + NX
$$
```

More examples:

```markdown
$\frac{a}{b}$
$\sum_{i=1}^{n} x_i$
$\alpha, \beta, \gamma$
```

Useful references for LaTeX math syntax:

- Overleaf Mathematical Expressions: https://www.overleaf.com/learn/latex/Mathematical_expressions
- Detexify (find symbol commands): https://detexify.kirelabs.org/classify.html
- LaTeX Wikibook Mathematics: https://en.wikibooks.org/wiki/LaTeX/Mathematics

## 6. Render the Document

In the VS Code terminal, run:

```bash
quarto render draft.qmd
```

To render PDF directly:

```bash
quarto render draft.qmd --to pdf
```

If PDF rendering fails, check whether your PDF engine is installed.
