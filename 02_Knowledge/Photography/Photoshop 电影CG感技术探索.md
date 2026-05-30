---
title: 'Photoshop 电影CG感技术探索'
aliases:
  - 'Photoshop 电影感与CG感技术探索'
tags:
  - Photography
  - Photography/Post-Processing
  - AIGC/Photoshop
  - Photoshop
  - color-grading
  - film-look
  - visual-design
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Photoshop 电影CG感技术探索.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/Photography'
status: distilled
safety_review_required: false
---

# Photoshop 电影CG感技术探索
Last_Updated: 2026-05-23

## Overview
- Purpose: 整理 Photoshop 中实现电影感与 CG/原画感的视觉机制，强调光学、影调、色彩、材质和分层工作流。
- Scope: Covers 色差、Bloom、Halation、胶片颗粒、Teal and Orange、留银、景深、AO、Z-Depth、材质高光和非破坏性 pass。Does not cover 单一步骤式按钮教程。

## Core Concepts
- **电影感**: 对真实镜头、胶片和调色流程痕迹的受控重建，核心是自然记录质感与风格化平衡。
- **CG/原画感**: 通过结构化光影、材质可读性、形体层级、空间秩序和设计感让画面更清晰。
- **受控瑕疵**: 色差、颗粒、暗角、Bloom、Halation、漏光和污渍只能局部、低强度、合逻辑使用。
- **影调塑形**: 高光 roll-off、抬黑位、中间调对比和局部 Dodge & Burn 决定画面底子。
- **色彩组织**: 冷暖分离、LUT、通道曲线、Selective Color、Gradient Map 用于叙事和空间分离。
- **Pass思维**: 技术校正、影调、色彩、材质、镜头痕迹和输出锐化应分层处理。

## Consolidated Principles
- P1 [Critical]: 电影感和 CG 感都不是滤镜名，而是多组视觉线索协同后的结果。
- P2 [Critical]: 先建立结构、影调和空间，再叠加颗粒、光斑、色差等表层痕迹。
- P3 [High]: 数字图像常见问题是过干净、过平、过锐；电影化依赖受控破坏这种完美。
- P4 [High]: CG 感依赖可读材质、轮廓光、AO、Z-Depth 和明度分组。
- P5 [High]: 色彩不是装饰，而是主体分离、情绪建立和空间组织工具。
- P6 [Normal]: 最终质感来自清晰结构与物理级不完美之间的平衡。

## Mechanisms & Logic
- Flow: 1. 基础曝光和白平衡校正 -> 2. 建立明度结构 -> 3. 组织色彩关系 -> 4. 强化空间和材质 -> 5. 添加镜头/胶片痕迹 -> 6. 输出锐度、噪点和统一性检查。
- Decision Rules: 高光过硬 -> 使用 roll-off、Bloom 或 Halation 的局部逻辑。
- Decision Rules: 画面太平 -> 增加 AO、局部对比、景深或空气透视。
- Decision Rules: 材质不可信 -> 重塑高光形状、粗糙度、边缘光和微纹理。
- Decision Rules: 风格不稳 -> 拆成 pass，减少一次性全局滤镜。

## Constraints
- 不要把电影感理解为加 LUT、暗角和黑边。
- 不要把 CG 感理解为单纯锐化、提高对比或清晰度。
- 不要全图平均施加色差、Halation、Bloom、漏光和污渍。
- 不要让肤色被全局冷暖分离污染。
- 不要在 8-bit 大面积渐变中重度推色，容易产生 banding。

## Related
- [[Photoshop Cinematic Look Principles]]
- [[Photoshop Cinematic and CG Look Guide]]
- [[Atmospheric Perspective in Visual Storytelling]]
- [[Cinematic Value and Planar Composition]]
- [[6头身性感写实液化指南]]
