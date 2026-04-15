# Student Prompting Guide

This guide helps students work with Codex in a way that improves learning instead of just getting answers quickly.

The goal is not to ask Codex to build everything.
The goal is to use Codex as a learning partner while you build the project yourself.

## What to do before prompting

Before writing a prompt, do these steps first:

1. Read the project task carefully.
2. Rewrite the task in your own words.
3. Identify your current week.
4. Remember the concepts allowed in your current week.
5. Break the project into one small step.
6. Try that step yourself first.
7. Then ask Codex about the exact part where you are stuck.

Do not jump directly to:

- "build the whole app"
- "give me full code"
- "fix everything"

That may feel fast, but it usually reduces learning.

## The best prompting habit

A strong prompt usually includes:

1. your current week
2. the project name
3. the exact task you are working on
4. what you already tried
5. what is going wrong
6. what type of help you want
7. your current code

## Best general prompt template

Use this template:

```text
I am in Week <number>.

Project: <project name>

My current task: <one small task only>

Allowed concepts this week: <topics>

I already tried: <short explanation>

What is happening now: <bug / confusion / wrong output>

Please help me learn this step without giving the full project solution first.
First explain the mistake or next step in simple English.
Then give me a small hint or a very small code example only for this part.

Here is my code:
<paste code>
```

## If you are starting a new project

Do not ask for the full app immediately.
Ask for a plan first.

Example:

```text
I am in Week 2.

Project: Reading Queue

Please help me plan this project using only Week 2 concepts.

First give me:
1. the main features
2. the components I may need
3. what state I may need
4. the best build order

Do not give me the full code yet.
```

## If you are stuck on one feature

Example:

```text
I am in Week 1.

Project: Daily Pulse Board

My current task: when I click a mood button, I want the selected mood text to update.

I already tried using useState, but the UI is not changing.

Please tell me:
1. what concept I am missing
2. what kind of line I should check
3. one small hint only

Here is my code:
<paste code>
```

## If you want a code review

Example:

```text
I am in Week 3.

Project: City Weekend Planner

I finished the filter section and localStorage part.
Please review this like a mentor.

Tell me:
1. what is correct
2. what is weak
3. what I should improve next

Please do not rewrite everything unless necessary.

Here is my code:
<paste code>
```

## If Codex gives something too advanced

Say this clearly:

```text
Please keep the solution inside Week <number> concepts only.
Do not use advanced concepts yet.
```

You can also say:

```text
Please simplify this and break it into smaller steps.
```

## If the answer is too big

Ask Codex to reduce scope:

```text
Do not solve the full project.
Help me only with the next small step.
```

## Good prompting rules

- Ask about one problem at a time.
- Always mention your week.
- Mention the project name.
- Share what you already tried.
- Paste the real code.
- Ask for explanation before solution.
- Ask for a review after making an attempt.
- Ask for smaller steps if the answer feels too big.

## Prompting mistakes to avoid

Avoid prompts like:

- "do my project"
- "build the full app"
- "fix this"
- "it does not work"
- "write all code"

Also avoid:

- asking about many different bugs in one prompt
- not sharing code
- not telling Codex your current week
- hiding what you already tried

## Real-world project workflow

This workflow will help in beginner projects and later real-world projects too:

1. understand the requirement
2. break it into features
3. pick one small feature
4. attempt it yourself
5. ask a focused question
6. apply the answer
7. test it
8. ask for review
9. improve the code
10. repeat

## Final rule

The best prompt is not the longest prompt.
The best prompt is the clearest prompt.

Give Codex:

- the right context
- the current limits
- one small task
- your real attempt

That will usually give the best learning result.
