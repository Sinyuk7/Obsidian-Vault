---
title: 'AI视频提示词标准化文档生成'
aliases:
  - 'AI Video Prompt Standardization Document Generation'
tags:
  - AIGC
  - AIGC/AI-Video
  - AIGC/Prompt-Engineering
  - video-generation
  - prompt-engineering
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\AI视频提示词标准化文档生成.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# AI视频提示词标准化文档生成
Last_Updated: 2026-05-23

## Overview
- Purpose: 将 AI 视频提示词文档从长篇材料压缩为稳定、可复用、可审查的知识规范。
- Scope: Covers 视频提示词文档的生成框架、信息保留规则、模型差异归纳、输出结构与质量检查。Does not cover 单次生成任务的完整代写、平台绕过技巧、未经验证的模型内部机制。

## Core Concepts
- **标准化文档生成**: 将多来源模型经验转化为统一 Markdown 知识文档，重点保留概念、原则、约束、机制和输出格式。
- **视频提示词**: 面向视频模型的时空描述，不只描述画面主体，还必须描述运动、镜头、节奏、场景连续性和约束。
- **模型差异层**: Sora、Wan、Seedance、可灵等模型的提示词偏好不同，文档应把共性规范与平台特定约束分离。
- **认知层与动作层分离**: 文档保存原理和决策规则，具体点击路径、临时 UI 操作和一次性 SOP 只在必要时压缩为机制。
- **可复用模板**: 输出应能支持后续写 prompt，而不是只保存某个样例。
- **风险边界**: 涉及人物、版权、未成年人、敏感场景或平台政策时，应优先记录合规约束。

## Consolidated Principles
- P1 [Critical]: 视频提示词文档必须先定义任务目标，再定义主体、运动、镜头、环境、光影、风格和限制。
- P2 [Critical]: 时间连续性比静态画面美感更容易出错，必须显式写出动作起点、过程、终点和镜头持续方式。
- P3 [High]: 不同模型的参数和语义偏好不能混写成单一规则；共性规则放正文，平台差异放机制或约束。
- P4 [High]: 负面约束应转写为正向可见状态，避免让模型关注不想出现的对象。
- P5 [High]: 示例只服务于抽象规则，不能让文档退化成样例堆。
- P6 [Normal]: 模板要短而完整，优先保留可迁移字段，删除修饰性背景。

## Mechanisms & Logic
- Flow: 1. 识别视频任务类型 -> 2. 抽取主体与场景 -> 3. 补齐运动和镜头 -> 4. 标注模型特定参数 -> 5. 输出检查清单。
- Decision Rules: 如果任务依赖参考图，先锁定参考对象与不可变特征，再描述运动变化。
- Decision Rules: 如果任务强调电影感，优先写镜头、景别、运动和光影，而不是堆叠风格形容词。
- Decision Rules: 如果需要多镜头，必须拆为镜头单元，避免在一个长句里混合多个时间段。
- Decision Rules: 如果输出用于知识库，保留原则与模板，删除一次性上下文。

## Constraints
- 不要把视频 prompt 写成静态图像 prompt 加上 movement。
- 不要把平台参数、模型版本和通用语义规则混为同一层级。
- 不要在标准文档中保留绕过审核、规避检测或弱化安全边界的策略。
- 不要保留空模块、表格、长引用、导入摘要或自动目录。
- 不要过度承诺模型能力；未验证的效果应写成倾向而不是事实。

## Output Format / Style Hints
- Format: 使用 Overview、Core Concepts、Consolidated Principles、Mechanisms & Logic、Constraints、Output Format / Style Hints。
- Prompt Skeleton: 主体与身份；场景与时代；动作与状态变化；镜头与运动；光影与色彩；风格与质感；技术约束；合规边界。
- Review Checklist: 是否有时间线；是否有主体一致性；是否有镜头逻辑；是否有安全边界；是否删除无信息修饰词。

## Related
- [[AI视频生成标准化提示词规范]]
- [[ai_video_prompt_engineering]]
- [[Seedance 2]]
- [[可灵 AI 视频生成操作手册]]
- [[Image understanding]]
