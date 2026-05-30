---
title: 'Midjourney 16_9 构图生成指南'
aliases:
  - 'Midjourney 16:9 构图指南'
tags:
  - AIGC
  - AIGC/Midjourney
  - AIGC/Composition
  - prompt-engineering
  - visual-design
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Midjourney 16_9 构图生成指南.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# Midjourney 16_9 构图生成指南
Last_Updated: 2026-05-23

## Overview
- Purpose: 解决 Midjourney 在 16:9 横幅中生成角色、全身与环境时的构图失控问题。
- Scope: Covers 16:9 画幅策略、主体锚定、镜头语言、全身约束、负空间管理和横向叙事构图。Does not cover 单张作品审美评价、侵权角色复刻、平台绕过。

## Core Concepts
- **几何悖论**: 16:9 横幅天然强调横向空间，人物全身天然强调纵向比例，两者会争夺画面面积。
- **主体锚定**: 通过 full body、feet visible、standing on ground、head-to-toe 等可见状态锁定全身。
- **横向叙事**: 16:9 不应只把人物缩小居中，而应使用环境、动作方向、道具和负空间扩展叙事。
- **镜头约束**: wide shot、full-body shot、low angle、long lens、wide-angle 等词会改变人物占比和透视。
- **安全区**: 头、手、脚、武器和关键轮廓需要避开画幅边缘，防止裁切。
- **视觉锚点**: 地面接触、阴影、脚部和前景物可帮助模型保持完整身体。

## Consolidated Principles
- P1 [Critical]: 16:9 全身角色必须同时写画幅、景别、身体完整性和地面接触，单写 16:9 不足以控制构图。
- P2 [Critical]: 不要让特写词和全身词同时竞争，例如 close-up portrait 与 full body。
- P3 [High]: 横幅构图要利用动作方向、对角线、道具延伸和背景层次，而不是空白填充。
- P4 [High]: 人物在画面中的位置要明确，如 centered full body、left third 或 right third。
- P5 [High]: 脚部可见性是全身生成的关键硬约束，应明确写出 visible feet 或 full figure from head to toe。
- P6 [Normal]: 风格词应放在主体与构图之后，避免抢占注意力。

## Mechanisms & Logic
- Flow: 1. 设定 aspect ratio 16:9 -> 2. 写完整主体和姿态 -> 3. 写全身锚点 -> 4. 写相机距离与角度 -> 5. 写环境负空间 -> 6. 写风格与细节。
- Decision Rules: 如果模型裁脚，增加 standing on visible ground、feet fully visible、full body framed with margins。
- Decision Rules: 如果主体太小，使用 full-body hero shot、occupying center frame、clear silhouette。
- Decision Rules: 如果画面空，增加前景、中景、背景和动作方向，而不是增加无关物体。
- Decision Rules: 如果透视夸张导致身体变形，降低 wide-angle 强度，使用 moderate lens 或 eye-level framing。

## Constraints
- 不要混用 portrait、headshot、close-up 与 full body 主目标。
- 不要用过多风格词挤占构图控制词。
- 不要只依赖参数 ar 16:9；参数决定画布，不决定构图。
- 不要让人物与武器、翅膀、披风同时占满边缘，容易造成裁切。

## Output Format / Style Hints
- Prompt Skeleton: full-body subject；visible head-to-toe；pose and ground contact；16:9 cinematic wide composition；camera distance and angle；foreground midground background；lighting；style；parameters。

## Related
- [[Midjourney Prompt Construction Standards]]
- [[Midjourney 提示词规范与实践]]
- [[Midjourney 构图技巧与全身照]]
- [[midjourney_v7_best_practices]]
- [[midjourney-prompt-guide]]
- [[midjourney-parameters-guide]]
