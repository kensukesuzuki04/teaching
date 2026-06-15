# GitHub Copilot Instructions

## Purpose

This guide explains how students should use GitHub Copilot in this course, why we use it, and how it supports learning.

## Table of Contents

- [Purpose](#purpose)
- [Why We Use Copilot](#why-we-use-copilot)
- [What Students Should Do](#what-students-should-do)
- [How Copilot Helps You](#how-copilot-helps-you)
- [Good Prompt Examples](#good-prompt-examples)
- [Using Agent Roles (Reviewer, Coauthor)](#using-agent-roles-reviewer-coauthor)
- [Class Rules for Responsible Use](#class-rules-for-responsible-use)
- [Required AI Statement in Submissions](#required-ai-statement-in-submissions)
- [Quick Workflow](#quick-workflow)
- [Final Reminder](#final-reminder)

## Why We Use Copilot

- To help you start coding tasks faster.
- To help you understand syntax and structure in Python and Quarto.
- To practice reading, testing, and improving generated code.
- To build debugging and problem-solving skills with support.

Copilot is a learning assistant, not a replacement for your own reasoning.

## What Students Should Do

### 1. Before starting a task

- Sign in to GitHub in VS Code.
- Confirm Copilot is active.
- Open your working folder in VS Code.
- Review the task prompt before asking Copilot for help.

### 2. During coding

- Write your own problem statement first in plain language.
- Ask Copilot for a first draft of code.
- Read every suggested line before accepting it.
- Run the code in small steps.
- Check outputs and error messages.
- Revise prompts when results are incorrect or unclear.

### 3. After getting suggestions

- Explain the code in your own words.
- Add comments where logic is not obvious.
- Test edge cases and confirm results.
- Keep only code you understand.

## How Copilot Helps You

- Faster first draft of code and text.
- Better understanding of common coding patterns.
- Quicker troubleshooting when errors occur.
- More time to focus on interpretation and economic reasoning.
- Improved confidence for beginners.

## Good Prompt Examples

- Write Python code to load a CSV file and show the first 10 rows.
- Explain this error message and suggest two fixes.
- Create a Quarto section with a figure, table, and short interpretation.
- Refactor this code to be easier to read.

## Using Agent Roles (Reviewer, Coauthor)

### Why this matters

- Different tasks need different feedback styles.
- A `reviewer` role can focus on errors, logic gaps, and missing evidence.
- A `coauthor` role can focus on structure, clarity, and argument quality.
- Using role-specific instructions gives more consistent and useful responses.

### How to set up agents in a class folder

1. In your project folder, create `.github/agents/`.
2. Add a file for each role, for example:
	- `.github/agents/reviewer.agent.md`
	- `.github/agents/coauthor.agent.md`
3. Put clear instructions in each file (what to check, output format, tone).
4. Save files and reopen Copilot Chat if needed.

Minimal example for `coauthor.agent.md`:

```markdown
---
description: Coauthor feedback for economics writing and revisions
tools: ['codebase', 'editFiles', 'runCommands']
---

You are a coauthor for an economics writing assignment.
Give direct, constructive feedback.
Focus on argument, evidence, and clarity.
Return feedback with these sections:
1. What Works
2. Major Issues
3. Minor Issues
4. Next Steps
```

### How to use these agents

1. Open Copilot Chat in VS Code.
2. Select the custom agent role (for example `coauthor` or `reviewer`) if it appears in the chat mode or agent list.
3. If your setup exposes slash commands, run the role command (for example `/coauthor`).
4. Paste your draft or ask the agent to review the current file.
5. Revise your document based on the feedback and run the role again.

Tip: Use `coauthor` for draft improvement and `reviewer` for stricter checks before submission.

### How to train or customize an agent over time

You can improve agent quality by giving it better context from your own work history.

Useful inputs include:

- A previous assignment submission that you wrote.
- Instructor feedback comments on that submission.
- A short note on what you want to improve (for example, argument flow, coding style, or table interpretation).

Example prompt:

```text
Here is my previous submission and my instructor's comments.
Please identify repeated weaknesses and create a revision checklist for this new draft.
Focus on structure, clarity, and evidence.
```

Best practice:

1. Ask the agent to extract patterns from feedback first.
2. Ask it to create a checklist you can reuse.
3. Apply the checklist to your current draft.
4. Re-run the agent and compare what improved.

Important:

- Use your own prior work and authorized feedback only.
- Do not ask the agent to copy old content directly into new submissions.
- Use feedback to improve your process, not to bypass learning.

## Class Rules for Responsible Use

> **CRITICAL POLICY (READ CAREFULLY)**
>
> **AI is not your replacement. AI is your assistant.**
>
> **You are fully responsible for everything you submit.**
>
> **Correct content can still receive zero credit if it does not align with class discussion, assignment goals, or course context.**
>
> **Accuracy alone is not enough. Relevance to the assignment and course context is required.**
>
> **AI does not fully know our class context. Situating the answer in course context is your responsibility.**

- Verify all code, interpretation, and output before submission.
- Do not submit AI-generated content that you cannot explain.
- Follow all course policies on collaboration and academic integrity.
- When required, disclose where Copilot assisted your work.

## Required AI Statement in Submissions

If you used AI tools (including GitHub Copilot) for an assignment, you must include an `AI Statement` section in your submission.

The statement must confirm both points:

1. How you used AI.
2. That the final submission is your own work and understanding.

Copy-paste template:

```text
AI Statement:
I used [tool name] to help with [brainstorming / code drafting / editing / debugging / formatting].
I reviewed, tested, and revised all AI-assisted output.
I confirm that this submission reflects my own understanding and that I take full responsibility for all content.
```

## Quick Workflow

1. Read the task.
2. Ask Copilot for a draft.
3. Run and test.
4. Debug and revise.
5. Explain results in your own words.

## Final Reminder

Use Copilot to learn actively. The goal is not just to finish code, but to understand the method, the output, and the economic meaning behind the result.
