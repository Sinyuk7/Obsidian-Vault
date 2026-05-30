---
title: 'AI视频生成标准化提示词规范'
aliases:
  - 'AI 视频生成提示词规范'
tags:
  - AIGC
  - AIGC/AI-Video
  - AIGC/Prompt-Engineering
  - video-generation
  - prompt-engineering
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\AI视频生成标准化提示词规范.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# AI视频生成标准化提示词规范
Last_Updated: 2026-05-23

## Overview
- Purpose: 定义跨视频生成模型可迁移的提示词结构，使画面、运动、镜头和风格在同一语义框架内被控制。
- Scope: Covers Sora、Wan、Seedance 等模型的共性提示词层级、常见反模式、七层架构和质量检查。Does not cover 单一平台 UI 操作、未经验证的新参数、规避审核策略。

## Core Concepts
- **物理中心主义**: 视频模型需要可推演的运动关系，动作必须符合重力、惯性、接触、遮挡和空间连续性。
- **美学分层**: 视觉效果由主体、场景、镜头、光影、色彩、材质和后期风格共同决定。
- **序列约束**: 视频 prompt 必须描述时间序列，避免只给终态。
- **七层架构**: 任务意图、主体、场景、动作、镜头、视觉风格、技术与安全约束构成完整提示词骨架。
- **Anti-Pattern**: 抽象形容词、互相冲突的动作、多镜头混写、负面提示词堆叠和过长装饰语会降低可控性。
- **时态固化**: 同一镜头内的人物、服装、位置和光源关系应保持连续，除非明确写出变化。

## Consolidated Principles
- P1 [Critical]: 主体和动作必须绑定，不能只写一个主体再追加模糊运动词。
- P2 [Critical]: 镜头运动和主体运动必须相容；相机推进、主体后退、背景变化需要形成同一空间逻辑。
- P3 [High]: 每个镜头只承载一个核心动作，复杂叙事拆成多个镜头单元。
- P4 [High]: 风格描述应服务于可见结果，优先使用摄影、灯光、材质和色彩术语。
- P5 [High]: 禁止把否定句当作主要控制手段；用正向状态替代。
- P6 [Normal]: 参数只在模型支持时出现，不能让参数替代语义描述。

## Mechanisms & Logic
- Flow: 1. 定义任务类型 -> 2. 写主体身份和不可变特征 -> 3. 写场景与空间关系 -> 4. 写动作时间线 -> 5. 写镜头语法 -> 6. 写光影风格 -> 7. 写技术与安全约束。
- Decision Rules: 静态主体要用 posture、gesture、gaze、breathing 等微运动保持生命感。
- Decision Rules: 动作复杂时使用 beginning、middle、end 的三段式描述。
- Decision Rules: 有参考图时先指定保留项，再指定允许变化项。
- Decision Rules: 多主体互动必须描述相对位置和接触关系。

## Constraints
- 不要使用互斥词组，如 simultaneously running and standing still。
- 不要把 wide shot、close-up、macro 等景别混在同一镜头中。
- 不要依赖 beautiful、epic、cinematic 等孤立形容词。
- 不要把不同平台参数直接迁移到不支持的平台。
- 不要忽略输出时长，过长动作会在短视频中被压缩或省略。

## Output Format / Style Hints
- Prompt Order: Subject -> Setting -> Action Timeline -> Camera -> Lighting -> Style -> Technical Constraints -> Safety Constraints。
- Quality Check: 主体是否唯一；动作是否可拍摄；镜头是否可执行；风格是否可见；约束是否正向表达。

## Related
- [[AI视频提示词标准化文档生成]]
- [[ai_video_prompt_engineering]]
- [[Seedance 2]]
- [[可灵 AI 视频生成操作手册]]
- [[Image understanding]]
