# AEB-model-generation
## Repository Structure

- v1_initial: Initial artifacts from early submission
- v2_revision: Revised and extended artifacts used in the revised manuscript

# v2_revision — Revised Evaluation and Extended Artifacts

This folder contains the revised and extended artifacts used in the second version of the *AEB Model Generation* project, corresponding to the updated evaluation and methodology presented in the revised manuscript.

The goal of this revision is to support the paper’s enhanced evaluation pipeline, which integrates Large Language Models (LLMs), model-driven engineering constructs (metamodel, EVL validation, EGL transformation), and formal verification via UPPAAL.

---

## Contents

- **Prompts/**  
  Few-shot learning prompts used to generate AEB models from natural-language driving scenarios.

- **Models/**  
  Generated XMI models for each evaluation scenario, produced by three different LLMs (DeepSeek, GPT-4, Grok-3).

- **Evaluation/**  
  Artifacts related to the rule-based comparative evaluation, including summary tables and analysis data.

- **Scripts/**  
  Python helper scripts for running prompt-based model generation and performing rule-based evaluation.

---

## Overview of Key Components

### Metamodel
The AEB metamodel defines the structural and semantic primitives of the automated emergency braking system. It is implemented in the Eclipse Modeling Framework (EMF) and serves as the schema for all generated XMI models.

### EVL Validation
EVL (Epsilon Validation Language) constraints enforce domain-specific rules that cannot be captured purely in the metamodel. These constraints ensure that generated models satisfy safety-relevant and semantic conditions before transformation.

### EGL Transformation
EGL (Epsilon Generation Language) templates automatically convert validated EMF-compliant models into UPPAAL-compatible XML specifications, enabling formal verification without manual intervention.

### Formal Verification with UPPAAL
The generated UPPAAL models are verified against representative timing and safety properties. The evaluation focuses on methodological feasibility rather than exhaustive industrial-grade automotive analysis.

---
## Evaluation Approach

The revised evaluation:

* Uses 13 diverse driving scenarios.
* Compares three LLMs (DeepSeek, GPT-4, Grok-3).
* Applies a rule-based evaluation framework (structural, semantic, behavioral).
* Replaces precision/recall-style metrics with interpretable rule satisfaction tables.
* Provides aggregated comparative scores across models.

---

## Notes

* All models are generated automatically without manual correction.
* EVL constraints are used exclusively for model validation.
* UPPAAL verification demonstrates feasibility and consistency rather than full industrial deployment.

---

## License

This repository is intended for academic and research use. Usage is subject to the terms of the associated manuscript and applicable API licenses.



