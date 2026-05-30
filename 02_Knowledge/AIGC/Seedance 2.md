---
title: 'Seedance 2.0 LLM 使用指南'
aliases:
  - 'Seedance 2'
  - 'Seedance 2.0'
tags:
  - AIGC
  - AIGC/AI-Video
  - AIGC/Seedance
  - AIGC/Prompt-Engineering
  - video-generation
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Seedance 2.0 LLM 使用指南.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# Seedance 2.0 LLM 使用指南
Last_Updated: 2026-05-23

## Overview
- Purpose: 蒸馏 Seedance 2.0 在多模态视频生成中的输入约束、路由逻辑和提示词绑定方法。
- Scope: Covers 全局限制、素材格式、交互入口、显性绑定、参考图/视频控制和场景 prompt 构建。Does not cover 平台审核绕过、未确认的内部模型机制、超出接口能力的参数。

## Core Concepts
- **显性绑定**: 使用 @ 语法或等价引用方式把文本描述绑定到具体素材，减少参考图、视频和文本之间的错配。
- **多模态输入**: 支持图像、视频、音频和文本，但每类素材都有数量、大小、时长和分辨率边界。
- **参考优先级**: 参考素材用于锁定角色、场景、运动或风格，文本用于说明保留项和变化项。
- **路由逻辑**: 文生视频、图生视频、参考视频和音频驱动任务应走不同 prompt 结构。
- **输出时长**: 生成时长通常为短片段，动作设计必须适配 4-15 秒范围。

## Consolidated Principles
- P1 [Critical]: 多素材任务必须显性绑定素材和描述，否则模型可能错用参考对象。
- P2 [Critical]: 素材上限是硬边界：图像最多 9 张，视频最多 3 个，音频最多 3 个。
- P3 [High]: 视频参考总时长限定在 2-15 秒，单文件小于 50MB，分辨率范围约 480p 到 720p。
- P4 [High]: 图像参考单文件小于 30MB；音频总时长不超过 15 秒，单文件小于 15MB。
- P5 [High]: 图生视频先锁定参考图不可变特征，再写允许发生的运动。
- P6 [Normal]: 成本较高的参考视频应只用于必要的运动或风格约束。

## Mechanisms & Logic
- Flow: 1. 判断任务入口 -> 2. 上传并命名素材 -> 3. 用显性绑定描述每个素材作用 -> 4. 写主体与运动 -> 5. 写镜头和风格 -> 6. 写保留与变化边界。
- Decision Rules: 角色一致性优先时，参考图绑定身份、服装、发型和面部特征。
- Decision Rules: 动作一致性优先时，参考视频绑定运动轨迹和节奏，文本只补充场景与风格。
- Decision Rules: 音频驱动时，动作节拍、表情和镜头切换应服从音频时间线。

## Constraints
- 不要上传超过数量、大小、时长或分辨率限制的素材。
- 不要让多个素材同时绑定同一不可兼容角色特征。
- 不要把参考素材的所有内容都设为必须保留，否则会压制运动变化。
- 不要使用规避审核或弱化安全限制的描述。

## Output Format / Style Hints
- Seedance Prompt Skeleton: task type；bound references；preserved features；allowed changes；motion timeline；camera movement；lighting and style；output duration；safety constraints。

## Related
- [[AI视频生成标准化提示词规范]]
- [[AI视频提示词标准化文档生成]]
- [[ai_video_prompt_engineering]]
- [[可灵 AI 视频生成操作手册]]
- [[即梦Seedance审核规避技巧|即梦Seedance合规风险与安全提示词边界]]
