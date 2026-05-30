---
title: 'Midjourney 构图技巧与全身照'
aliases:
  - 'Midjourney 全身照构图技巧'
tags:
  - AIGC
  - AIGC/Midjourney
  - AIGC/Composition
  - Photography/Composition
  - prompt-engineering
  - visual-design
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Midjourney 构图技巧与全身照.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# Midjourney 构图技巧与全身照
Last_Updated: 2026-05-23

## Overview
- Purpose: 定义在 Midjourney 中提升构图可控性和全身照完整性的提示词策略。
- Scope: Covers 扩散模型构图随机性、景别控制、相机角度、全身协议、参数微调、Pan 与 Vary Region 修正。Does not cover 后期绘画教程、侵权角色复制、绕过平台限制。

## Core Concepts
- **肖像倾向**: 训练数据和审美偏好会让人物生成偏向半身或近景。
- **景别控制**: wide shot、full shot、medium shot、close-up 决定主体与环境的比例。
- **相机角度**: eye-level、low angle、high angle、bird's-eye、Dutch angle 会改变心理感受和透视。
- **全身协议**: full body、head-to-toe、visible feet、standing on ground、entire figure in frame 需要组合使用。
- **构图锚点**: 地面、阴影、完整轮廓、边距和环境尺度帮助模型保持身体完整。
- **后期修正生态**: Pan、Vary Region、outpainting 等用于修复裁切和局部错误。

## Consolidated Principles
- P1 [Critical]: 全身照必须明确脚、头、身体边距和画幅内完整性，不能只写 full body。
- P2 [Critical]: close-up、portrait、bust shot 会抵消全身目标，应避免同用。
- P3 [High]: 景别词比抽象构图词更直接影响主体占比。
- P4 [High]: 角色姿态越复杂，越需要写重心、地面接触和肢体可见性。
- P5 [High]: 构图失败优先修正景别与相机距离，再调整风格参数。
- P6 [Normal]: 需要动态画面时使用对角线、动作方向和前中后景，而不是增加对象数量。

## Mechanisms & Logic
- Flow: 1. 定义主体数量 -> 2. 写景别和相机距离 -> 3. 写身体完整性锚点 -> 4. 写姿态与地面接触 -> 5. 写环境尺度 -> 6. 写参数。
- Decision Rules: 裁脚 -> 加 visible feet、full figure、floor visible、margin around body。
- Decision Rules: 人物太小 -> 加 centered full-body hero subject、clear silhouette。
- Decision Rules: 肢体错乱 -> 降低动作复杂度，明确手脚数量与方向。
- Decision Rules: 构图空洞 -> 加 foreground framing、background depth、leading lines。

## Constraints
- 不要同时使用多个互斥景别。
- 不要把 full body 放在风格词之后太靠后的位置。
- 不要让武器、披风、翅膀等延伸物遮挡四肢完整性。
- 不要依赖单个参数解决语义冲突。

## Output Format / Style Hints
- Full-Body Prompt Skeleton: subject；full body from head to toe；visible feet and hands；pose；camera distance；composition；environment scale；lighting；style；parameters。

## Related
- [[Midjourney 16_9 构图生成指南]]
- [[Midjourney Prompt Construction Standards]]
- [[Midjourney 提示词规范与实践]]
- [[midjourney_v7_best_practices]]
- [[角色原画结构分析技巧清单]]
