---
title: 'Image understanding'
aliases:
  - '图像理解输入规范'
  - 'Gemini Image Understanding'
tags:
  - AIGC
  - AIGC/Image-Understanding
  - AIGC/Multimodal
  - model-notes
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Image understanding.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# Image understanding
Last_Updated: 2026-05-23

## Overview
- Purpose: 定义图像理解任务中的观察层级、描述边界和从视觉证据到结论的推理方式。
- Scope: Covers 图像内容识别、构图分析、风格判断、视觉缺陷诊断和生成提示词反推。Does not cover 无证据推断、人物身份识别、医学或法律结论。

## Core Concepts
- **图像理解**: 从可见像素中提取主体、关系、空间、动作、风格、文本和异常信息。
- **视觉证据**: 只能来自图像中可观察的形状、颜色、光影、材质、位置、文字和上下文。
- **分层观察**: 先全局后局部，先客观后解释，先描述再判断。
- **不确定性标注**: 当信息不足时使用可能、倾向、无法确认，而不是伪造事实。
- **反向提示词**: 将图像特征转译为可生成的主体、场景、镜头、光影、风格和约束。

## Consolidated Principles
- P1 [Critical]: 不能把不可见信息当作事实，例如身份、年龄精确值、动机、真实地点或拍摄设备。
- P2 [Critical]: 安全敏感判断必须保守，尤其涉及未成年人、裸露、伤害、身份和版权。
- P3 [High]: 图像分析应区分描述、解释、推测和建议。
- P4 [High]: 构图与风格判断必须绑定可见证据，如视平线、明度分组、色彩关系和焦点位置。
- P5 [High]: 反推 prompt 时要保留核心视觉关系，删除无法生成的分析性语句。
- P6 [Normal]: 对复杂图像使用清单式输出，避免长段落遮蔽证据链。

## Mechanisms & Logic
- Flow: 1. 识别画面主体 -> 2. 记录空间关系 -> 3. 分析光影与色彩 -> 4. 判断风格与媒介 -> 5. 标注异常和不确定性 -> 6. 输出描述或反推 prompt。
- Decision Rules: 如果问题要求评价质量，先说明评价维度，再给出改进建议。
- Decision Rules: 如果图中有文字，逐字记录可读文本，无法辨认处标注不可读。
- Decision Rules: 如果需要生成同风格图像，把分析结论转成可见描述。

## Constraints
- 不要识别现实人物身份，除非用户已提供身份并只要求图像内分析。
- 不要根据外表推断敏感属性。
- 不要把图像之外的背景故事写成事实。
- 不要忽略画面中明显的安全、版权或合规风险。

## Related
- [[AI视频生成标准化提示词规范]]
- [[AI视频提示词标准化文档生成]]
- [[doc_zimage_architecture_policy]]
- [[Seedance 2]]
- [[可灵 AI 视频生成操作手册]]
