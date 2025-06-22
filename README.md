# aeb-model-generation
# AEB Model Generation Prompts
This repository contains prompts and generated XMI models for the Autonomous Emergency Braking (AEB) system, as described in the paper "Enhancing Safety-Critical System Verification: Integrating Large Language Models with Model-Driven Engineering."

## Structure
- `prompts/`: Contains Few-Shot prompts for generating XMI models.
- `models/`: Contains generated XMI models for each scenario.

## Metamodel Summary
- AEBSystem: systemID (String), operatingMode (Normal/Emergency), ...
- Constraints: SpeedRange (Pedestrian <= 30.0 km/h, Vehicle <= 120.0 km/h), ...

## Usage
Use these prompts with Grok (xAI API, https://x.ai/api) or other LLMs like GPT-4. Configure with temperature=0.7, max_tokens=2048.
