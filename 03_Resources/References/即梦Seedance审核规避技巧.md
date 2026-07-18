---
title: '即梦Seedance合规风险与安全提示词边界'
aliases:
  - 'Seedance 安全提示词边界'
  - '即梦视频生成合规风险识别'
tags:
  - AIGC
  - AIGC/AI-Video
  - AIGC/Safety
  - AIGC/Seedance
  - safety-review
  - source-material
  - imported/drive-download
  - source/docx
  - status/distilled
source_title: '即梦Seedance审核规避技巧.docx'
imported: 2026-05-23
original_format: docx
target_folder: '03_Resources/References'
status: distilled
safety_review_required: true
---

# 即梦Seedance合规风险与安全提示词边界
Last_Updated: 2026-05-23

> [!warning] Safety Boundary
> 本笔记仅用于合规风险识别与安全边界整理。不得将其中内容改写为审核绕过、检测规避、敏感词替换或平台测试流程。

## Overview
- Purpose: 将原始“审核规避”主题改写为 Seedance / 即梦视频生成中的合规风险识别和安全提示词边界。
- Scope: Covers 视频生成中的人物年龄、服装覆盖、动作语义、参考素材、版权、平台政策和拒绝场景。Does not cover 绕过审核、替换敏感词、规避检测或滥用工作流。

## Core Concepts
- **视频安全风险**: 视频比静态图更容易因动作、镜头推进、身体接触和时序变化产生性化、暴力或误导性风险。
- **素材绑定风险**: 参考图、视频和文本若绑定不清，可能把不安全特征迁移到输出。
- **成人身份明确化**: 涉及人物身体、服装或亲密动作时，必须明确成人、非性化、非剥削和公开安全语境。
- **动作语义边界**: 舞蹈、运动、时装展示等可允许场景应写成健康、专业、非挑逗的动作。
- **版权与肖像边界**: 不复刻名人、影视角色、游戏角色或受保护形象。

## Consolidated Principles
- P1 [Critical]: 不提供任何即梦或 Seedance 审核绕过方法。
- P2 [Critical]: 年龄不明、幼态、校园化或未成年人相关人物不得与性化动作、暴露服装或亲密镜头结合。
- P3 [High]: 参考素材必须说明保留项和禁止迁移项，避免不安全视觉特征扩散。
- P4 [High]: 镜头语言不能用于强化窥视、跟拍身体局部或隐私侵犯。
- P5 [High]: 可安全生成的内容应转向时装、舞台、运动、广告或电影化中性场景。
- P6 [Normal]: 平台限制应作为设计边界，而不是对抗目标。

## Mechanisms & Logic
- Flow: 1. 检查人物年龄和身份 -> 2. 检查动作与服装 -> 3. 检查参考素材来源 -> 4. 判断拒绝或安全改写 -> 5. 输出合规视频 prompt。
- Decision Rules: 请求要求“避开审核”或“换词通过” -> 拒绝。
- Decision Rules: 动作可能被理解为挑逗 -> 改为明确的舞台表演、健身动作或时装走秀，并保留非性化边界。
- Decision Rules: 镜头聚焦身体局部 -> 改为全身、中景或动作整体呈现。
- Decision Rules: 参考素材含受保护人物或角色 -> 改为原创角色与一般风格。

## Constraints
- 不要保存可执行规避步骤、敏感词替换或平台检测推测。
- 不要用“艺术”“实验”“隐喻”等词弱化安全边界。
- 不要让镜头、动作和服装共同构成性化未成年人或非自愿场景。
- 不要使用他人肖像或受版权保护角色做替代复刻。

## Output Format / Style Hints
- Safe Video Prompt: adult subject if relevant；neutral or professional action；clear clothing coverage；public or fictional safe setting；camera framing；lighting；style；explicit safety boundary。

## Related
- [[02_Knowledge/AIGC/Governance/敏感词规避与提示词合规治理|敏感词规避与提示词合规治理]]
- [[02_Knowledge/AIGC/Video/AI视频生成提示词标准化规范|AI视频生成提示词标准化规范]]
- [[ai_video_prompt_engineering]]
- [[02_Knowledge/AIGC/Governance/敏感词规避与提示词合规治理|敏感词规避与提示词合规治理]]
