---
title: 'AI绘画合规风险与提示词边界指南'
aliases:
  - 'AI绘画安全提示词边界'
  - 'AI绘画合规风险识别'
tags:
  - AIGC
  - AIGC/Safety
  - safety-review
  - source-material
  - imported/drive-download
  - source/docx
  - status/distilled
source_title: 'AI绘画审核规避实战指南.docx'
imported: 2026-05-23
original_format: docx
target_folder: '03_Resources/References'
status: distilled
safety_review_required: true
---

# AI绘画合规风险与提示词边界指南
Last_Updated: 2026-05-23

> [!warning] Safety Boundary
> 本笔记仅用于合规风险识别与安全边界整理。不得将其中内容改写为审核绕过、检测规避、敏感词替换或平台测试流程。

## Overview
- Purpose: 将原始“审核规避”材料改写为合规风险识别与安全提示词边界，避免形成绕过平台审核的操作手册。
- Scope: Covers AI 绘画中的敏感内容风险、禁止模式、合规改写原则、拒绝边界和安全审查清单。Does not cover 审核绕过技巧、替换词表、检测规避流程或平台滥用策略。

## Core Concepts
- **合规边界**: 提示词必须尊重平台政策、法律要求、版权约束和人物安全边界。
- **风险触发项**: 未成年人、非自愿裸露、性化姿态、仇恨、暴力伤害、名人深度伪造、受保护 IP 复刻等场景需要拒绝或改写。
- **正向安全描述**: 将不安全或模糊请求改写为成人、非性化、原创、公开场景、健康语境和明确服装覆盖的描述。
- **拒绝边界**: 当请求目标本身是规避审核、隐藏敏感意图或生成违规内容时，应拒绝而不是优化。
- **来源材料定位**: 此笔记保留为资源区参考，目的为风险治理，不作为可执行生成 SOP。

## Consolidated Principles
- P1 [Critical]: 不保留、不生成、不优化任何绕过审核、规避检测或弱化安全系统的步骤。
- P2 [Critical]: 对未成年人或年龄不明人物，禁止性化、裸露化或亲密化描述。
- P3 [High]: 对版权角色和名人请求，应转向原创角色、一般风格特征和合法视觉属性。
- P4 [High]: 对敏感身体、暴力或歧视内容，优先判断是否应拒绝；可允许的情况必须转为非图形化、教育性或中性描述。
- P5 [High]: 安全改写应减少风险，而不是用隐晦词替代敏感词。
- P6 [Normal]: 记录风险类型、原因和安全替代方向，比保存原始规避话术更有价值。

## Mechanisms & Logic
- Flow: 1. 识别请求目标 -> 2. 标记风险类别 -> 3. 判断拒绝或安全改写 -> 4. 输出合规描述 -> 5. 保留禁止边界。
- Decision Rules: 请求明确要求绕过、规避、骗过审核 -> 拒绝。
- Decision Rules: 请求涉及年龄不明且性化 -> 要求明确成人且改为非性化，无法改写则拒绝。
- Decision Rules: 请求复刻 IP 或名人 -> 改为原创视觉特征，避免名称、标志和专属符号。
- Decision Rules: 请求可转为普通美术或摄影描述 -> 保留构图、光影、材质和风格，删除违规目标。

## Constraints
- 不要提供敏感词替换表。
- 不要提供平台审核机制推测、检测规避路径或分步测试方法。
- 不要把违规目标包装成艺术、学术或隐喻后继续执行。
- 不要把资源区材料升级为可操作绕过指南。

## Output Format / Style Hints
- Safety Rewrite Format: 风险类型；不可执行原因；安全替代目标；合规提示词方向；必须拒绝的边界。

## Related
- [[02_Knowledge/AIGC/Governance/敏感词规避与提示词合规治理|敏感词规避与提示词合规治理]]
- [[02_Knowledge/AIGC/Z-Image/Z-Image Prompt Engineering 使用指南|Z-Image Prompt Engineering 使用指南]]
- Image understanding（原始参考材料未保留为独立笔记）
- [[02_Knowledge/AIGC/Midjourney/Midjourney 提示词工程实践手册|Midjourney 提示词工程实践手册]]
