# 参与共建

感谢参与《信任力》的持续完善。

## 最简单的参与方式

把下面这句话交给你的 Agent：

```text
阅读 https://github.com/flyingpig707/PowerofTrust/tree/main/skills/power-of-trust-coauthor 并参与《信任力》共同写作
```

完整流程和文件格式由 [`skills/power-of-trust-coauthor/SKILL.md`](skills/power-of-trust-coauthor/SKILL.md) 说明。也可以先创建“共同写作提案”Issue，与维护者确认范围。

## 适合提交的内容

- 错别字、格式、链接或图片问题；
- 数据、引文和案例的原始来源补充；
- 对“三层五真”等框架的边界与反例；
- 可公开核验的品牌实践案例；
- 随书工具的使用反馈和改进建议。

## 提交建议时请说明

1. 涉及的章节与原文位置；
2. 建议修改的内容；
3. 修改理由；
4. 可核验来源及观察日期；
5. 内容属于事实、推断、作者观点还是教学推演。

## 内容原则

- 不提交无法核验的企业内部信息或个人隐私；
- 不伪造数据、评价、认证或第三方背书；
- 不把对 AI 平台机制的推断写成已公开事实；
- 不提交未获授权的大段第三方版权内容；
- 不利用共建入口发布广告或攻击性内容。

## 投稿与正式书稿的边界

参与者只在 `contributions/<github-login>/<proposal-slug>/` 提交结构化提案，不直接修改 `book/`。确定性检查通过后，提案可以进入公开提案库，但仍不代表作者认可。作者或维护者决定采用时，另行创建编辑 Pull Request 修改正式书稿并记录署名。

投稿前必须阅读并明确接受 [`CONTRIBUTOR-TERMS.md`](CONTRIBUTOR-TERMS.md)。公开仓库当前仍未附加整书开源许可证；投稿授权不等于为整本书授权复制、改编或商业使用。

本地检查：

```bash
python3 scripts/validate_contributions.py contributions/<github-login>/<proposal-slug> --write-self-check
python3 scripts/validate_pull_request.py --base-ref origin/main
```

维护者会根据证据质量、适用边界、原创性、读者价值和全书一致性决定是否采纳。详见 [`GOVERNANCE.md`](GOVERNANCE.md)。
