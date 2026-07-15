# testing1-memo.md

This file is a Q&A draft for the peer-review submission.
Write your answer after each `A:` in your own words.
Use simple sentences (B1 English). Short and clear is better than long and complex.

The submission is a **video**, not a runnable project. This is because the pipeline
needs Docker (for GROBID) and a Gemini API key. A classmate cannot try this in a few
minutes without that setup. This document covers proto3 (the current main
prototype).

---

## 1. Template Statement

**Q1:** Which project template are you using?

> Reuse this sentence (from `report1/report.md` Ch1 §2):
> "This project uses Template 12.1 from the NLP module."

A:

---

## 2. Video Content

**Q2:** What should the video show, step by step?

> Suggested steps, in simple order:
> 1. One sentence about the problem: the project finds the research methodology
>    (method, task, dataset, metric) in a computing paper.
> 2. Show GROBID running in Docker. It turns a PDF into a TEI XML file.
> 3. Show the Colab notebook (`proto3/3pipeline.ipynb`) running on that XML file.
> 4. Show the prompt sent to the LLM for a few seconds. Point at the rule "use the
>    authors' own method, not methods cited from prior work" and the rule that the
>    quote must be copied word-for-word. This shows the prompt was designed with
>    real rules, not just "read this paper and tell me about it."
> 5. Show the final output: one JSON object with an `answer` and `evidence` for each
>    of the four roles (for example, the "Attention Is All You Need" paper).
> 6. Point at the `evidence` field. Explain that it shows a real quote from the
>    paper, so the answer can be checked.
>
> The video does not need to explain every design choice. It needs to show that the
> pipeline works from start to end, and that the prompt was designed with care.

A:

**Q3:** How do you show, in the video, that this is not just "throwing the paper at
an LLM"?

> This is worth planning ahead of time. A reviewer who only watches a short video may
> think you just pasted the paper into a chat window. Use real facts to prevent
> this:
> - The prompt has a clear schema: four named roles (TechnicalMethod, Task, Dataset,
>   EvaluationMetric), each with an `answer` and an `evidence` object.
> - The prompt has a rule to pick the authors' own method, not a method from prior
>   work.
> - The prompt requires the quote to be word-for-word from the paper, so it can be
>   checked.
> - Real testing found a bug: an early version of the prompt was unclear about the
>   shape of `evidence`, so the LLM returned one flat string instead of a
>   `{section, quote}` object. The prompt was then rewritten to fix this. This is a
>   short, concrete design story you can tell in a few seconds — it shows real
>   testing and iteration, not one lucky try.
>
> You can show this in the video itself (Q2, step 4), and/or write one or two
> sentences about it in the short text that goes with the video submission.

A:

**Q4:** How long should the video be? What will you say, and what will you just show
on screen?

> Keep the spoken part short and simple. Show the JSON output on screen instead of
> describing it in words. A short video (a few minutes) that shows the real output
> is better than a long video with a lot of talking.

A:

---

## 3. Software and Hardware Instructions

**Q5:** What software and hardware does a viewer need to know about, even though they
only watch a video?

> List what your own setup needed. This also explains why you chose a video:
> - Docker, to run the GROBID container (`lfoppiano/grobid:0.8.1`, about 1 GB).
> - A Google account, for Google Colab.
> - A Gemini API key (from Google AI Studio). You add it as a Colab secret named
>   `GEMINI_API_KEY`.
> - An internet connection, for Colab and the Gemini API.
> - No local Python install is needed. The notebook installs its own packages
>   (`google-genai`) inside Colab.

A:

**Q6:** Why is a video the right choice here, instead of a runnable project?

> Give the real reason: Docker, GROBID, and a Gemini API key are too much setup for
> a classmate who just wants a quick look. This matches the brief's own reason for
> allowing a video: "if it is not possible to submit a runnable project... you can
> submit a video."

A:

---

## 4. Peer-Review Questions

**Q7:** What three statements do you want reviewers to rate? Pick 3 (or write your
own). Each answer will be one of: Disagree / Partially disagree / Neither agree nor
disagree / Partially agree / Agree.

> Candidate statements (simple B1 English, one idea per sentence):
> - Trust in the answer: "The evidence shown for each answer made me believe the
>   answer was correct."
> - Clarity of output: "The final output (the JSON with answer and evidence) was
>   easy to understand."
> - Problem clarity: "The video made it clear what problem this project solves."
> - Technical demonstration (recommended, see Q3): "The video showed careful prompt
>   design and real testing, not just one simple question to an LLM."
>
> Including the technical-demonstration statement is a good idea. It turns the
> question you are worried about ("did they just prompt an LLM?") into something
> reviewers rate directly, using what you showed in Q3 — instead of leaving it as an
> unspoken doubt.
>
> Each statement must work with the agree/disagree scale. Do not write a question
> ("Did you understand...?"). Write a statement ("I understood...").

A:

