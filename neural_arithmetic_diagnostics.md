# When High Arithmetic Accuracy Is Not Enough:
# A Diagnostic Framework for Structural Robustness in Neural Arithmetic

**Mohamed Mhamdi**

---

## Abstract

High arithmetic accuracy in neural models does not by itself establish robust reasoning. A model may perform strongly on standard evaluations while remaining fragile under structured stress. We introduce a diagnostic framework for neural arithmetic that distinguishes among distribution-bound fit, bounded compositional competence, and stronger algorithm-like behavior through a multi-dimensional scorecard. The framework combines in-distribution testing, structured adversarial families, bounded length extrapolation analysis, mechanism-sensitive probes, repeated-run validation, and qualification-aware interpretation. Using this framework, we obtain a stable baseline matrix across MLP, LSTM, and Transformer models and identify a clear architecture-dependent split on a block-boundary stress pattern. We then evaluate a first intervention based on adversarial training and show that it can produce strong gains on a seen adversarial family without yielding broad held-out robustness transfer. These results show that intervention success can be real yet still structurally narrow. More broadly, the paper argues that arithmetic evaluation should move beyond score-only reporting and toward transfer-sensitive, structure-aware diagnostics.

---

## 1. Introduction

High arithmetic accuracy is not, by itself, evidence of robust reasoning. Neural models can achieve strikingly strong performance on arithmetic tasks while still failing under structured stress, making standard benchmark scores insufficient for stronger claims about what the model has actually learned.

Arithmetic is an especially useful domain for exposing this problem because it has a known underlying rule structure. That makes it possible to separate two situations that are often conflated in model evaluation: a model may learn a solution that works well over a substantial but limited region of the data distribution, or it may acquire a more robust internal structure that survives distributional, structural, and procedural variation. Under standard testing conditions, these two forms of success can look deceptively similar.

This work grows out of that tension. Earlier stages of the broader research line found strong arithmetic performance under standard evaluation, but later structured tests and a full trust-recovery audit showed that performance, interpretation, and scientific confidence had to be separated much more carefully. That process restored substantial trust in the empirical backbone of the project, but it also clarified a broader lesson: high arithmetic accuracy should not be interpreted in isolation. It must be tested against structured stress and interpreted through a framework capable of distinguishing local success from broader robustness.

Project 4 was designed as the methodological answer to this problem. Instead of continuing to chase stronger raw scores, it asks a more diagnostic question: how can we distinguish between distribution-bound fit, bounded compositional competence, and stronger algorithm-like behavior in neural arithmetic models? To answer that, we introduce a diagnostic framework organized around a multi-dimensional scorecard. The framework combines in-distribution accuracy, structured adversarial evaluation, bounded length behavior, and mechanism-sensitive probes such as rounding dependence and carry corruption sensitivity. Crucially, it also includes an explicit validation layer so that interesting single-run results are not mistaken for stable findings.

Using this framework, we obtain a stable baseline matrix across three model families—MLP, LSTM, and Transformer—and identify a clear architecture-dependent split on a block-boundary stress pattern. We then test a first intervention based on adversarial training and show that it can produce a strong gain on a seen adversarial family without yielding broad held-out robustness transfer. This illustrates one of the central points of the framework: intervention success can be real and stable while still remaining structurally narrow.

The contribution of this work is therefore not the claim that a new model has solved arithmetic reasoning. Rather, the contribution is methodological. We provide a practical and reproducible way to evaluate whether apparent arithmetic progress reflects broader structural robustness or only localized gains. In doing so, we argue for a shift in arithmetic-model evaluation: away from score-only reporting and toward transfer-sensitive, structure-aware diagnostic testing.

### Contributions

Our main contributions are:

1. We introduce a diagnostic framework for neural arithmetic reasoning that distinguishes distribution-bound fit, bounded compositional competence, and stronger algorithm-like behavior.

2. We define a practical multi-dimensional evaluation scorecard that combines in-distribution performance, structured adversarial testing, bounded length behavior, and mechanism-sensitive probes.

3. We produce a stable baseline matrix across multiple model families and show that architecture-dependent differences can emerge sharply on structured adversarial patterns.

4. We show that adversarial training can improve performance on a seen adversarial family without producing broad held-out robustness transfer.

5. We argue that high arithmetic accuracy alone is not sufficient evidence of robust reasoning, and that arithmetic evaluation should move toward structured diagnostic testing rather than benchmark score interpretation alone.

---

## 2. Related Work

This work sits at the intersection of four research threads:

1. **neural arithmetic and algorithm learning**
2. **compositional generalization**
3. **adversarial and structure-sensitive evaluation**
4. **mechanistic and diagnostic analysis of model behavior**

### 2.1 Neural Arithmetic and Learned Computation

A long-standing line of work in neural networks has asked whether models can learn arithmetic procedures in a way that generalizes beyond narrow training conditions. Arithmetic has often been treated as a useful testbed for this question because it combines:
- exact correctness conditions,
- explicit local and global structure,
- and a clear distinction between rule-following and partial approximation.

In many settings, neural models achieve strong observed performance on arithmetic tasks, especially under in-distribution or moderately shifted evaluation. However, these results leave open a deeper question: does strong performance reflect robust learned structure, or does it reflect a narrower solution that is only reliable inside a restricted region of the task space?

Project 4 contributes to this line of work by shifting emphasis away from raw arithmetic success alone and toward diagnostic characterization of *what kind* of success is present.

### 2.2 Compositional Generalization

The broader literature on compositional generalization has repeatedly shown that success on familiar distributions does not guarantee robust behavior under recombination, extrapolation, or structured novelty. Models may appear strong on held-out data while still relying on local statistical regularities that fail under more systematically organized variation.

This concern is especially relevant in arithmetic because arithmetic tasks naturally invite stronger interpretations. If a model performs well over many examples or longer sequences, it is easy to infer that it has learned something rule-like. But compositional-generalization research cautions against that inference unless robustness survives meaningful structural shifts.

Project 4 contributes to this area by making the distinction operational. Rather than asking only whether arithmetic behavior generalizes, it asks whether that generalization is:
- distribution-bound,
- bounded but meaningful,
- or stronger and more structurally stable.

### 2.3 Adversarial and Structure-Sensitive Evaluation

A growing body of work in machine learning has shown that standard evaluation can fail to detect brittle or shortcut-based behavior. This has motivated the use of adversarial examples, worst-case analysis, and challenge sets in domains such as vision, language, and reasoning.

However, many adversarial approaches focus on perturbation at the input level without always preserving the internal task structure that makes the evaluation scientifically interpretable. In contrast, arithmetic allows the design of **structured adversarial families** whose difficulty is tied to meaningful internal task regularities rather than arbitrary perturbation.

This is one of the central motivations for Project 4. The framework uses structured adversarial arithmetic families—not just generic difficulty—to probe whether model competence transfers across qualitatively different stress conditions.

The goal is not simply to produce harder examples, but to create evaluation families that distinguish:
- local improvement
from
- broader structural robustness

### 2.4 Evaluation Beyond Aggregate Accuracy

Recent work across machine learning has increasingly emphasized that aggregate metrics can conceal important failure modes. Average performance can hide:
- subgroup collapse,
- worst-case failures,
- shortcut dependence,
- or sensitivity to small but meaningful structural changes.

This motivates richer evaluation frameworks that preserve:
- per-condition reporting,
- worst-case behavior,
- and stability under reruns.

Project 4 is aligned with this direction. Its scorecard does not treat average performance as sufficient. Instead, it requires:
- pattern-wise reporting,
- worst-case pattern accuracy,
- repeated-run validation,
- and multi-dimensional interpretation.

This places the framework closer to robust evaluation methodology than to traditional benchmark reporting.

### 2.5 Mechanistic and Diagnostic Analysis

A separate but related line of work asks not only whether models succeed or fail, but what internal processes support that behavior. Mechanistic interpretability, probing, and circuit analysis all belong to this broader effort to move from performance description toward structured behavioral understanding.

Project 4 does not itself provide a full mechanistic account. Its contribution is earlier in the chain: it provides a framework that can identify the kinds of stable behavioral contrasts that would make mechanistic analysis scientifically meaningful.

In this sense, Project 4 is complementary to mechanistic work:
- it does not replace internal analysis,
- but it helps define which empirical contrasts are worth explaining.

### 2.6 Position of This Work

The present work differs from much of the prior literature in one key way:

> it is not primarily an arithmetic-accuracy paper, nor primarily a mechanistic paper, nor merely an adversarial-evaluation paper.

Instead, it is a **diagnostic framework paper**.

Its central claim is methodological:
- high arithmetic accuracy should not be interpreted alone
- intervention gains should not be trusted without transfer checks
- and arithmetic reasoning should be evaluated through structured, validation-aware diagnostics rather than score-only reporting

This is the specific niche this paper aims to occupy.

### 2.7 Summary

The relevant literature suggests three broad lessons:

1. strong observed performance can be misleading
2. compositional generalization requires structure-sensitive evaluation
3. robust scientific interpretation requires more than a single scalar benchmark

Project 4 builds directly on those lessons by providing a practical framework for applying them to neural arithmetic.

---

## 3. Motivation and Framing

The motivating problem behind this work is not merely that arithmetic is difficult for neural networks. The deeper issue is that **high performance can be epistemically misleading**. A model may achieve strong results under conventional evaluation while still lacking the kind of robustness that would justify stronger reasoning claims.

Arithmetic is especially useful for studying this problem because its underlying rule structure is explicit. This makes it possible to distinguish between two situations that often look similar under standard testing: first, a model may learn a solution that works well over a substantial but limited region of the data distribution; second, a model may acquire a more robust internal structure that survives distributional, structural, and procedural variation. Standard benchmarks often fail to separate these possibilities sharply enough.

Project 4 is framed around this distinction. Its question is not simply which model achieves the best score, but what kind of competence that score actually represents.

To address that question, the framework uses three working regimes:

- **Distribution-bound fit**: strong performance tied to a relatively narrow evaluation regime, with sharp degradation under more structured shifts.
- **Bounded compositional competence**: meaningful generalization within a bounded range, but without broader robustness to harder extrapolation or adversarial structure.
- **Stronger algorithm-like behavior**: more stable performance across length, adversarial structure, and equivalent formulations of the same underlying rule.

These are diagnostic categories, not metaphysical claims about cognition. Their value lies in organizing evidence in a way that prevents over-interpretation.

This leads to the central methodological principle of Project 4:

> No single metric is sufficient for regime classification.

A model may have strong in-distribution performance but weak worst-case adversarial behavior. Another may appear robust on one structured family while collapsing on another. An intervention may improve one family while failing to transfer beyond the patterns it explicitly saw during training. In all such cases, a single scalar metric can hide the actual scientific story.

For this reason, Project 4 uses a multi-dimensional scorecard rather than a winner-takes-all benchmark. The framework combines:
- in-distribution accuracy,
- structured adversarial performance,
- length behavior,
- rounding sensitivity,
- and carry corruption sensitivity.

This combination is deliberate. It allows us to ask not only whether a model succeeds, but whether that success:
- transfers,
- remains stable,
- depends on post-processing,
- or breaks under structured perturbation.

Structured adversarial families are especially central in this framing. Standard random test sets are useful, but they do not systematically probe the internal regularities that may matter most. By contrast, adversarial carry-pattern families place the model under sharply defined structural pressures. They make it possible to distinguish broad robustness from narrow family-specific adaptation.

This matters not only for baseline evaluation, but also for interventions. An intervention can appear successful if it improves one difficult family. That does not yet imply general robustness. The improvement may remain local to the seen family and may even trade off against performance elsewhere. Project 4 therefore treats *transfer across adversarial families* as a more meaningful signal than improvement on any single family in isolation.

This framing also explains why negative or qualified outcomes are scientifically valuable. If a model fails under a structured diagnostic, that is not an embarrassment to be hidden. It is evidence about the nature and limits of the learned solution. Likewise, if an intervention produces narrow gains without broad transfer, that is not a weak null result. It is a positive finding about the limits of that intervention.

Project 4 is built around this idea: the goal of evaluation is not merely to rank models, but to reveal what their apparent success actually consists of. Arithmetic is the domain used here, but the methodological lesson is broader: whenever a task has a known internal rule structure, strong benchmark performance should be stress-tested against structure-sensitive diagnostics before stronger interpretive claims are made.

---

## 4. Diagnostic Framework

Project 4 introduces a diagnostic framework for evaluating arithmetic reasoning beyond benchmark-style accuracy reporting. The framework is designed to characterize the *type* of competence a model exhibits, not merely the level of its raw performance.

It has four core components:

1. **working regime definitions**
2. **diagnostic test families**
3. **a multi-dimensional scorecard**
4. **a validation layer**

Together, these components define the evidential standard used throughout the project.

### 4.1 Working Regimes

The framework organizes model behavior into three working regimes.

#### Regime 1 — Distribution-Bound Fit
A model performs well within relatively narrow evaluation conditions, but degrades sharply under structured or mechanism-relevant shifts.

#### Regime 2 — Bounded Compositional Competence
A model exhibits nontrivial compositional behavior within a bounded range, but does not remain stable under harder extrapolation or systematically novel structure.

#### Regime 3 — Stronger Algorithm-Like Behavior
A model remains stable across longer lengths, structured adversarial families, and equivalent formulations of the same rule.

These regime labels are intended as diagnostic categories, not as final philosophical claims about model cognition.

### 4.2 Diagnostic Test Families

To distinguish among these regimes, the framework uses multiple evaluation families rather than a single benchmark.

#### In-Distribution Random
This family measures standard performance on random examples drawn from the same broad family as training data. It serves as a baseline sanity condition, but it is never treated as sufficient evidence of robust reasoning.

#### Structured Adversarial
This is the most important family in Project 4.

The v1.0 adversarial core contains:
- **alternating carry**
- **full propagation chain**
- **block-boundary stress**

These patterns were selected because they place sharply different demands on carry behavior and structural generalization.

#### Length Extrapolation
This family measures how performance changes as sequences extend beyond the core training range.

#### Mechanism-Sensitive Probes
This family includes probes such as:
- rounding sensitivity
- carry corruption sensitivity

These are not full mechanistic proofs. Rather, they test whether performance depends strongly on specific procedural assumptions or signal channels.

### 4.3 Multi-Dimensional Scorecard

The framework records model behavior through a scorecard rather than a single scalar.

The core scorecard dimensions in Project 4 v1.0 are:

1. **in-distribution accuracy**
2. **structured adversarial accuracy**
3. **worst-case pattern accuracy**
4. **length extrapolation trend**
5. **rounding sensitivity**
6. **carry corruption sensitivity**

The reason for this structure is simple:

> No single metric is sufficient for regime classification.

A model may have strong average adversarial accuracy but collapse on one pattern. Another may improve on a seen family but fail on a held-out family. A third may preserve standard accuracy while remaining highly dependent on post-processing. Project 4 therefore requires pattern-wise reporting, worst-case reporting, and multi-dimensional interpretation.

### 4.4 Pattern-Wise and Worst-Case Reporting

Project 4 explicitly avoids reducing structured adversarial behavior to a single mean value.

For every structured adversarial evaluation, the following must be reported:

- pattern-wise breakdown
- mean adversarial accuracy
- worst-case pattern accuracy

This is essential because one catastrophic failure can be hidden inside an otherwise moderate or strong average. Worst-case pattern behavior is therefore treated as a first-class diagnostic signal.

### 4.5 Length Trend as a Diagnostic Object

Length behavior is not treated only descriptively. It must also be expressed in a computable form.

At minimum, Project 4 requires:
- accuracy by tested length
- relative drop beyond the training range
- a qualitative trend label such as:
  - stable
  - gradual decline
  - sharp collapse

### 4.6 Intervention Evaluation Logic

The framework is also designed to evaluate interventions, not only baselines.

An intervention is not treated as successful merely because one metric improves. Instead, the framework asks:

- Did the intervention improve only a seen family?
- Did it transfer to unseen structured conditions?
- Did it improve one dimension while damaging another?
- Did it create local gain without broader robustness?

### 4.7 Validation Layer

Project 4 includes an explicit validation layer.

Interesting results are not enough; stable results are required.

The framework therefore distinguishes between:
- single-run artifacts
- repeat checks
- stability-supported findings

At MVP stage, repeated-run validation is required before a result is elevated into a real Project 4 finding.

### 4.8 Rule-Guided Classification

Although the framework computes scorecards and generates regime guidance, final regime classification is **not fully automated**.

This is intentional. A fully automatic classifier would risk:
1. overfitting interpretation to threshold artifacts
2. concealing ambiguity in borderline cases

Project 4 therefore uses:
- rule-guided indicators
- scorecard-based evidence
- and explicit human-reviewed rationale

### 4.9 What the Framework Is Designed to Detect

The framework is especially well suited to detecting situations such as:

- high standard performance with low adversarial robustness
- strong seen-family gains without held-out transfer
- architecture-specific pattern differences
- local success that does not scale into broader structural competence

These are exactly the kinds of cases that standard arithmetic accuracy reporting tends to obscure.

### 4.10 Summary of Framework Role

The Project 4 framework should therefore be understood as:

- a structured evidence system
- a robustness diagnosis tool
- and an anti-overclaim mechanism

Its purpose is not to decide in advance that a model is good or bad. Its purpose is to force the project to answer a harder and more useful question:

> What kind of arithmetic competence is actually present, and how far does it transfer under structured stress?

---

## 5. Experimental Setup

This section describes the empirical setup used in Project 4. The setup was designed to support the diagnostic framework rather than to maximize benchmark performance in isolation.

The experimental design has three major components:

1. **baseline model families**
2. **diagnostic evaluation families**
3. **intervention protocol**

All reported Project 4 results were interpreted under the framework’s validation and qualification rules.

### 5.1 Baseline Model Families

Project 4 began with three baseline model families:

- **MLP**
- **LSTM**
- **Transformer**

These baselines were selected because earlier stages of the research line had already established them as important reference families for arithmetic behavior, and because they provide meaningful variation in inductive bias.

The role of the baseline matrix was not simply to rank models. It was to establish a stable comparative reference under a common diagnostic framework.

At the MVP stage, these baselines were evaluated using a bounded but repeated-run protocol so that cross-model observations would not depend on a single accidental run.

### 5.2 Baseline Source and Runtime Context

The baseline execution paths in Project 4 were built on top of the previously audited codebase. In particular, Project 4 baseline work used bounded evaluation paths derived from the post-audit validated code context, especially the multidigit arithmetic infrastructure associated with the Phase 30 family.

These should therefore be interpreted as:
- post-audit diagnostic baselines
- rather than raw unaudited historical reruns

That distinction matters because Project 4 does not blindly repeat the earlier research line. It uses the audited foundation as a controlled starting point for a new diagnostic project.

### 5.3 In-Distribution Evaluation

The in-distribution family served as a baseline sanity condition. Its purpose was narrow:
- to determine whether a model performs nontrivially under a standard random evaluation path

### 5.4 Structured Adversarial Evaluation

The v1.0 adversarial family consisted of:
- **alternating carry**
- **full propagation chain**
- **block-boundary stress**

These patterns probe:
- periodic carry structure
- long carry propagation dependence
- and robustness at local/global boundary interfaces

### 5.5 Length Evaluation

Project 4 also tracked bounded length-conditioned behavior in order to preserve a length-sensitive scorecard dimension without claiming broad scaling conclusions from a single curve.

### 5.6 Mechanism-Sensitive Dimensions

Two additional dimensions were included:
- **rounding sensitivity**
- **carry corruption sensitivity**

These were useful as framework dimensions, though not equally mature across all execution paths at MVP stage.

### 5.7 Validation Protocol

Project 4 adopted a validation-aware reporting policy from the start. Baseline and intervention findings were not treated as established merely because they appeared once.

At MVP stage, repeated-run validation was applied to both:
- the accepted baseline matrix
- and the first intervention signal

### 5.8 Intervention Design

The first Project 4 intervention was:
- **adversarial training**

Its design separated:
- **seen adversarial families**
- **held-out adversarial families**

This was necessary to distinguish:
- local intervention gain
from
- broader structural transfer

### 5.9 Blockwise Extension Attempt

Project 4 also included a first attempt at a blockwise decomposition intervention.

However, this branch was not accepted into the scientific result core because the implementation path became methodologically unresolved during debugging.

### 5.10 Reporting Policy

All Project 4 results were reported under the following rules:

1. no single metric determines the interpretation
2. pattern-wise reporting is required
3. worst-case behavior must be preserved
4. repeated-run stability matters
5. regime classification remains human-reviewed and rationale-based
6. unresolved branches are explicitly marked rather than silently dropped

### 5.11 Summary of Experimental Design

The experimental setup of Project 4 was designed to answer a diagnostic question rather than an optimization question:

- establish stable baselines
- expose structured failure or selectivity
- test whether intervention gains transfer
- preserve qualifications
- and avoid overclaiming beyond the evidence

This was sufficient to produce a meaningful MVP result even without solving the strongest version of arithmetic robustness.

## 6. Stable Baseline Matrix

The first major empirical outcome of Project 4 was the construction of a stable baseline matrix across three model families:
- **MLP**
- **LSTM**
- **Transformer**

These baselines were not treated as one-off exploratory runs. They were repeated and checked for stability under the Project 4 validation protocol. The goal of this stage was not simply to determine which model had the highest score, but to establish whether the framework could reveal stable, structured, architecture-dependent differences.

It could.

### 6.1 Why the Baseline Matrix Matters

A diagnostic framework is only useful if it can expose meaningful structure before intervention work begins. If all baseline models look effectively identical, then the framework may not be discriminating enough. If stable cross-model differences emerge under structured evaluation, the framework is already doing something scientifically useful.

That is what happened in Project 4.

Across repeated runs, the baseline matrix showed that the three model families did **not** merely differ by small random variation. Instead, they displayed:
- broadly weak exact-match performance,
- common failures on some structured adversarial families,
- and a sharp architecture-dependent split on one specific pattern family.

### 6.2 Shared Weaknesses Across Baselines

Under the current bounded Project 4 evaluation path, all three baseline families remained weak in exact-match terms.

More importantly, all three collapsed on at least some structured adversarial families, especially:
- **alternating carry**
- **full propagation chain**

This is significant because these are exactly the kinds of structured tests that ordinary random evaluation tends to under-emphasize. Their shared collapse suggests that strong arithmetic competence should not be inferred from standard random-style success alone.

In other words, the framework immediately revealed that:
- the baseline models were not broadly robust,
- and that structured stress testing is necessary before intervention analysis even begins.

### 6.3 Architecture-Dependent Split on Block-Boundary Stress

The strongest and most informative baseline result was the behavior on **block-boundary stress**.

This pattern produced a clear and repeated split:

- **MLP:** stable success
- **Transformer:** stable success
- **LSTM:** stable failure

This was not a one-off anomaly. The pattern remained stable under repeated-run validation.

This result is scientifically important because it shows that structured adversarial evaluation can reveal differences that are not obvious from aggregate performance alone. If evaluation stopped at a single overall score, this architecture-dependent split might remain hidden.

It also shows that the baseline families differ not only in degree of weakness, but also in **type of vulnerability**. Under the Project 4 framework, the LSTM did not merely perform slightly worse than the others. It failed specifically on a pattern family where MLP and Transformer remained stable.

That makes block-boundary stress the first especially discriminative pattern family in Project 4.

### 6.4 More Than a Numerical Ranking

The baseline matrix is valuable not because it lets us say “model A is best” in a simplistic sense. Its value is diagnostic.

The baseline findings already show:
- where all models fail together
- where models remain weak in common
- and where architecture-specific structure appears

This is stronger than a ranking alone because it helps identify:
- which pattern families are globally difficult
- which pattern families are selectively difficult
- and which families are likely to be especially informative for intervention design

That is precisely the kind of information a diagnostic framework should surface.

### 6.5 Bounded Interpretation

The correct interpretation of the baseline matrix remains bounded.

Project 4 does **not** claim at this stage that:
- any model has reached stronger algorithm-like behavior
- the baseline matrix settles all architecture questions
- or the observed differences already prove a deep mechanistic explanation

What it does support is narrower and more defensible:

> the Project 4 baseline framework can detect stable architecture-dependent differences under structured stress, and those differences are meaningful enough to guide intervention design.

This is already a significant methodological success.

### 6.6 Why the Baseline Matrix Matters for Intervention Design

The stable baseline matrix gave Project 4 exactly what it needed before intervention work:

- a stable reference set
- a map of globally difficult families
- and a discriminative pattern family (`block_boundary stress`) for testing transfer and architecture sensitivity

That baseline map directly motivated the first MVP intervention:
- adversarial training

---

## 7. Adversarial Training as MVP Intervention

After establishing a stable baseline matrix, Project 4 moved to its first intervention stage:
- **adversarial training**

This intervention was chosen because it directly tests one of the framework’s central questions:

> If a model is exposed to difficult structured adversarial families during training, does that exposure produce broader robustness, or only narrow performance gains on the trained families themselves?

This is exactly the kind of distinction that benchmark-driven evaluation often obscures. A model can improve after intervention and still fail to generalize in the stronger sense that matters most.

### 7.1 Why Adversarial Training Was the Right First Intervention

Adversarial training was an ideal MVP intervention because it is simple, intuitive, and directly diagnostic.

A natural expectation might be:
- if a model is explicitly trained on difficult structured cases,
- then it should become more robust in a broader sense.

But another possibility is equally plausible:
- the model may simply learn to handle the specific adversarial family it has seen,
- without gaining broader structural robustness.

Project 4 was designed specifically to separate these two possibilities.

This is why the intervention setup distinguished between:
- **seen adversarial families**
- **held-out adversarial families**

Without that distinction, intervention success could easily be overstated.

### 7.2 Seen-Family Gain Versus Held-Out Transfer

The first intervention produced a clear and stable pattern:

- strong improvement on a **seen adversarial family**
- no broad gain across all difficult families
- failure on a **held-out adversarial family**

This matters because it breaks a common but weak inference:
- “the intervention improved performance, therefore it improved robustness”

Project 4 shows that this inference is too crude.

The intervention produced a real effect, but the effect was **narrow** rather than broadly transferable.

### 7.3 Why This Is a Strong Result

This result is important not because it shows adversarial training “failed” in a simplistic sense. The intervention did succeed in changing the model’s behavior.

What makes the result scientifically valuable is that the framework can distinguish:
- **real gain**
from
- **robust transfer**

The first intervention therefore validates the framework itself.

If Project 4 had reported only:
- one improved adversarial score

then the intervention might look broadly successful.
But because the framework includes:
- held-out families
- repeated-run stability
- pattern-wise reporting
- and explicit qualification

the interpretation becomes much sharper.

This is exactly the kind of result the framework was designed to produce.

### 7.4 Main Diagnostic Conclusion

The most defensible interpretation of the first intervention is:

> adversarial training can improve performance on a specifically seen structured family without producing broad structural robustness transfer.

This is not a trivial result.

It tells us that:
- intervention gains should not be treated as automatically general
- structured evaluation families must remain distinct
- and held-out structured stress is necessary for meaningful robustness evaluation

In that sense, the intervention confirmed the need for the framework.

### 7.5 Why This Result Is Methodologically Strong

The intervention result is scientifically strong because it is:
- repeated
- stable
- structurally interpretable
- and framed against a baseline matrix

That allows a more precise conclusion than:
- “the intervention helped”
or
- “the intervention failed”

Instead, the result shows:
- the intervention produced a real gain
- the gain was family-specific
- and broad transfer did not follow automatically

That is a much more useful scientific conclusion.

### 7.6 Bounded Interpretation

The interpretation remains intentionally bounded.

Project 4 does **not** claim from this intervention alone that:
- adversarial training can never produce broader robustness
- all intervention gains are merely memorization
- or the exact internal cause of the observed trade-off has been identified

Those claims would be too strong.

What the current evidence supports is narrower:
- the first intervention yielded stable narrow gain
- broad held-out transfer was not observed
- and intervention behavior must therefore be evaluated family-by-family rather than by aggregate improvement alone

### 7.7 Why This Matters Beyond This Intervention

The significance of this result extends beyond the specific adversarial-training setup used here.

It supports a broader methodological lesson:

> intervention success should be judged by transfer across structured stress families, not by local gain alone.

That lesson could matter well beyond arithmetic. Wherever a model is evaluated on:
- compositional structure
- adversarially organized inputs
- or distribution-sensitive tasks

there is a risk that local gains will be mistaken for broader capability.

Project 4 provides one concrete framework for avoiding that mistake.

### 7.8 Why This Was Enough for MVP

At this point in the project, the first intervention had already succeeded in one important sense:
- it showed that the framework can separate local improvement from broader robustness transfer

That was enough for MVP-level scientific value.

This is why the accepted Project 4 synthesis rests primarily on:
- the stable baseline matrix
- and the stable first intervention signal
rather than on unresolved extension branches.

---

## 8. What the Framework Reveals

The value of Project 4 does not lie only in the individual numbers reported for baselines or interventions. Its real value lies in what becomes visible once those numbers are placed inside a diagnostic structure.

What the framework reveals is not simply which model is better, or whether one intervention improved a metric. It reveals the *shape* of arithmetic competence and the *limits* of that competence under structured stress.

This is the central contribution of Project 4.

### 8.1 Why Standard Accuracy Is Not Enough

If evaluation stopped at in-distribution accuracy alone, the scientific picture would be severely incomplete.

A model could appear competitive under standard random evaluation while still:
- collapsing on particular structured families
- depending on narrow support conditions
- or improving only on the exact families it saw during intervention

The framework reveals that these are often the most informative parts of the result.

Standard accuracy tells us whether a model performs.
The framework asks *what kind of performance that is*.

### 8.2 Why Family Identity Matters

One of the clearest lessons from the baseline and intervention results is that arithmetic weakness is not uniform.

Different pattern families expose different forms of limitation.

A model can:
- fail catastrophically on one structured family
- remain strong on another
- and improve on one family while not transferring to another

Without explicit family-level structure, these differences would collapse into an average and become harder to interpret.

The framework reveals that **family identity matters**.

That is scientifically important because it shifts the evaluation question from:
- “Did accuracy go up?”
to
- “On what structure did it go up, and did that transfer?”

### 8.3 Why Baselines and Interventions Must Be Read Together

Another key lesson is that baselines and interventions cannot be interpreted in isolation.

The stable baseline matrix tells us:
- where models already differ before intervention
- which families are globally hard
- and which families are especially discriminative

The intervention result then tells us:
- whether intervention changes those baseline patterns
- whether it improves one family only
- or whether it shifts robustness in a broader way

This combined reading is stronger than either baselines or interventions alone.

Project 4 therefore reveals not only behavior, but **change relative to a structured baseline map**.

### 8.4 Stable Weakness Is Scientifically Valuable

A stable failure pattern is often more informative than a high score with no diagnostic structure.

A model that repeatedly fails on one adversarial family but succeeds on another tells us more than a single average would. Likewise, an intervention that repeatedly improves a seen family while failing to transfer still yields a scientifically meaningful result.

This is one of the strongest commitments of Project 4:
- negative and qualified results are not consolation prizes
- they are central evidence

### 8.5 Why This Matters for Arithmetic Research

Arithmetic is often treated as a benchmark domain because it has a known rule structure and a clear notion of correctness. But that same clarity can create false confidence if evaluation is too narrow.

Project 4 shows that arithmetic reasoning research should be careful in at least three ways:
1. benchmark success should not be interpreted alone
2. structured adversarial evaluation is not optional
3. intervention claims require transfer testing

These are methodological lessons, but they are also scientific ones.

### 8.6 Why This Matters Beyond Arithmetic

The broader relevance of the framework comes from the fact that arithmetic is only one domain where benchmark scores can conceal narrow solutions.

The same problem appears whenever a task has:
- latent compositional structure
- multiple possible shortcut strategies
- or a difference between standard examples and structured stress cases

The broader methodological logic may therefore generalize:
- evaluate family-by-family
- preserve worst-case structure
- validate repeated runs
- separate local gain from transfer

The exact scorecard will still need domain-specific redesign, but the underlying logic is portable.

### 8.7 The Main Methodological Takeaway

The strongest lesson that Project 4 makes explicit is:

> A model can become better in a real sense without becoming broadly robust in the sense that matters most.

This is why Project 4 is a diagnostic framework project rather than a benchmark race.

Its value lies in forcing a stronger standard of evidence:
- not “did the score improve?”
but
- “what exactly improved, where, and how far did that improvement transfer?”

### 8.8 Why the MVP Is Already Enough

Project 4 does not need a Regime 3 model to matter.

The framework already succeeded because it produced:
- a stable baseline matrix
- a stable intervention signal
- and a principled distinction between narrow gain and broader transfer

That is enough to justify the MVP as a meaningful scientific contribution.

The framework revealed something important:
- improvement can be genuine
- and still remain structurally limited

That is the key result Project 4 contributes to the research line.

---

## 9. Limitations

Although Project 4 achieved its MVP objective, its conclusions remain intentionally bounded. This is a strength rather than a weakness: the framework was designed to separate what the evidence supports from what it does not yet support.

Several limitations therefore remain explicit.

### 9.1 No Regime 3 Claim

Project 4 does not establish that any tested model reached stronger algorithm-like behavior.

This was never required for MVP success, and no such claim should be inferred from the current results.

### 9.2 Uneven Maturity Across Scorecard Dimensions

The framework includes multiple dimensions, but not all are equally mature in implementation at the current stage.

In particular:
- some dimensions were already central and empirically informative, especially structured adversarial behavior and stable baseline/intervention comparisons
- other dimensions, such as some mechanism-sensitive probes, remain less mature in bounded implementation form

This does not invalidate the framework, but it means the framework should be read as:
- operational and useful
- but still evolving in implementation maturity

### 9.3 Blockwise Decomposition Remains Unresolved

Project 4 included a first blockwise decomposition attempt, but that branch was not accepted into the scientific result core because the implementation path became methodologically unresolved during debugging.

This means:
- Project 4 does not yet provide a clean answer to the blockwise structural hypothesis
- and stronger claims about chunking or carry-interface decomposition remain open

That branch is documented, but excluded from the accepted MVP result core.

### 9.4 No Full Mechanistic Proof

Project 4 is a diagnostic framework and intervention study, not a completed mechanistic interpretability analysis.

It can reveal:
- stable weaknesses
- transfer failures
- architecture-dependent differences
- and family-specific intervention gains

But it does not yet prove:
- the exact internal computation strategy of any model
- the representational basis of carry handling
- or the circuit-level reason why one architecture succeeds where another fails

Those remain valid future directions.

### 9.5 Bounded Scope

The implementations in Project 4 were designed to be operational, reproducible, and bounded rather than maximally exhaustive.

This means:
- not every architecture or intervention variant was explored
- some paths were intentionally simplified at MVP stage
- engineering completeness was sometimes deferred in favor of a stable diagnostic core

This is acceptable for MVP, but it limits how far the current conclusions should be stretched.

### 9.6 Arithmetic as a Special Domain

Arithmetic is unusually useful for this kind of work because:
- correctness is explicit
- structure is well-defined
- and stress patterns can be designed cleanly

But this also means caution is needed when generalizing outward.

Project 4 supports a methodological claim that likely extends beyond arithmetic:
- benchmark success should be stress-tested against structured evaluation

However, it does not by itself prove that the exact same families, thresholds, or regime behavior will transfer unchanged to other domains.

### 9.7 Diagnosis Rather Than Final Theory

Project 4 is strongest when read as:
- a diagnostic system
- a measurement philosophy
- and a structured intervention-testing framework

It is weaker if over-read as:
- a final theory of arithmetic reasoning in neural networks
- a definitive architecture ranking
- or a complete mechanistic account

This is not a defect. It is part of what makes the project’s claims credible.

### 9.8 Why These Limitations Matter

These limitations are not decorative disclaimers. They define the boundary of the project’s valid contribution.

Project 4 established:
- that structured diagnostics can reveal baseline differences hidden by simpler evaluation
- that intervention gains can be narrow and non-transferable
- and that repeated-run stability matters for interpreting those signals

That is already substantial.

The limitations simply prevent those findings from being overstated.

### 9.9 Practical Interpretation Boundary

The correct final use of Project 4 is therefore:
- as a meaningful MVP diagnostic contribution
- as a stable baseline/intervention study
- and as a framework that can be extended later

It should not yet be used as proof that the full problem of arithmetic robustness has been solved, nor as a complete account of the mechanisms underlying the observed patterns.

---

## 10. Conclusion

This work began from a simple but increasingly important problem: high arithmetic accuracy is not enough to justify strong claims about robust reasoning. Neural models can appear highly successful under standard evaluation while remaining fragile under structured stress. If evaluation stops at benchmark-style performance, this distinction can remain hidden.

Project 4 addressed this problem by introducing a diagnostic framework for arithmetic reasoning. Rather than asking only whether a model performs well, the framework asks what kind of competence that performance represents. To do this, it combines a multi-dimensional scorecard, structured adversarial families, repeated-run validation, and rule-guided interpretation. The goal is not merely to rank models, but to distinguish between distribution-bound fit, bounded compositional competence, and stronger algorithm-like behavior.

Using this framework, we obtained a stable baseline matrix across three model families and identified a clear architecture-dependent split on block-boundary stress. We then tested a first intervention based on adversarial training and found that it can produce strong gains on a seen adversarial family without yielding broad held-out robustness transfer. This is the key empirical result of the project: intervention gains can be real, stable, and still structurally narrow.

The broader contribution of Project 4 is methodological. It shows that arithmetic evaluation should move beyond raw accuracy reporting and toward transfer-sensitive, structure-aware diagnostics. In this sense, the project contributes not a final theory of arithmetic reasoning, but a more rigorous way to evaluate it.

This is why Project 4 succeeds even without a Regime 3 model. Its MVP objective was not to prove that stronger algorithm-like behavior had been found, but to build a framework capable of distinguishing local gains from broader robustness. That objective was met. The project now provides:
- a working diagnostic framework,
- a stable baseline comparison matrix,
- and a stable first intervention signal with a scientifically meaningful interpretation.

At the same time, the work remains explicitly bounded. It does not provide a full mechanistic account of model behavior, it does not resolve the blockwise hypothesis, and it does not claim that the current framework exhausts every relevant diagnostic dimension. These limitations are not weaknesses to hide. They are part of what makes the current contribution credible.

The strongest final conclusion is therefore straightforward:

> high arithmetic performance is not sufficient evidence of robust reasoning, and intervention gains should be evaluated by their ability to transfer across structured stress families rather than by local improvement alone.

Project 4 establishes a practical framework for making that distinction. That is its central contribution, and it provides a concrete methodological foundation for future work on arithmetic reasoning, robustness, and structured generalization in neural systems.