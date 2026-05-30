---
title: '可灵 AI 视频生成操作手册'
aliases:
  - 'Kling AI 视频生成操作手册'
  - '可灵视频生成手册'
tags:
  - AIGC
  - AIGC/AI-Video
  - AIGC/Kling
  - AIGC/Prompt-Engineering
  - video-generation
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\可灵 AI 视频生成操作手册.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# 可灵 AI 视频生成操作手册
Last_Updated: 2026-05-23

## Overview
- Purpose: 将可灵 AI 视频生成能力整理为模型使用知识，聚焦任务入口、控制能力、提示词范式和失败修正。
- Scope: Covers 文生视频、图生视频、多图参考、视频延长、质量模式、运动控制和结构化场景提示词。Does not cover 临时 UI 路径、平台政策绕过、未验证参数。

## Core Concepts
- **文生视频**: 从文本直接生成场景，prompt 必须完整描述主体、场景、动作、镜头和风格。
- **图生视频**: 参考图承担身份、构图或风格锚定，文本主要描述时间变化和镜头运动。
- **多图参考**: 多张图可拆分角色、场景、道具或风格，但必须说明每张图的作用。
- **视频延长**: 续写需要保持上一段的主体、运动方向、光线和镜头节奏。
- **质量模式**: 高质量通常换取更高成本或更长生成时间，适合最终输出；快速模式适合探索。
- **运动幅度**: 动作越大，身份和细节漂移风险越高。

## Consolidated Principles
- P1 [Critical]: 图生视频必须先声明参考图的保留项，再声明运动变化。
- P2 [Critical]: 多图参考不能让不同图的角色身份、服装或场景规则互相冲突。
- P3 [High]: 镜头运动应简单明确，优先 pan、tilt、dolly、zoom 等单一运动。
- P4 [High]: 延长视频要延续上一段状态，避免突然改变时间、天气、服装或空间。
- P5 [High]: prompt 应包含动作起点、过程和终点，避免只写动态形容词。
- P6 [Normal]: 质量模式选择应跟任务阶段匹配，探索期重速度，成片期重稳定。

## Mechanisms & Logic
- Flow: 1. 选择文生或图生入口 -> 2. 定义主体与场景 -> 3. 写动作时间线 -> 4. 写镜头运动 -> 5. 写光影风格 -> 6. 加质量和安全约束。
- Decision Rules: 如果角色漂移，减少动作幅度并强化参考图保留项。
- Decision Rules: 如果镜头混乱，拆分为单一镜头运动。
- Decision Rules: 如果续写断裂，重申上一段结尾状态、运动方向和光照条件。
- Decision Rules: 如果画面过静，增加微动作和环境运动，如 hair moving、dust drifting、light flickering。

## Constraints
- 不要把多个镜头切换塞进一个短 prompt。
- 不要让主体动作与镜头动作方向互相抵消。
- 不要只写 high quality、cinematic，而不写可见镜头和光影。
- 不要使用平台规避、敏感内容弱化或不合规提示。

## Output Format / Style Hints
- Kling Prompt Skeleton: subject；reference role；setting；motion timeline；camera movement；lighting；style；duration or quality mode；constraints。

## Related
- [[AI视频生成标准化提示词规范]]
- [[AI视频提示词标准化文档生成]]
- [[ai_video_prompt_engineering]]
- [[Seedance 2]]
- [[Image understanding]]
