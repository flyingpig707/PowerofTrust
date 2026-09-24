import { defineConfig } from "vitepress";

const repository = "https://github.com/flyingpig707/PowerofTrust";
const editBranch = process.env.VITEPRESS_EDIT_BRANCH || "book/v0.2-three-part-structure";
const siteUrl = process.env.VITEPRESS_SITE_URL || "https://trust.learn-together.cn";

export default defineConfig({
  lang: "zh-CN",
  title: "信任力",
  titleTemplate: ":title · 信任力",
  description: "AI时代，我们如何信任别人，又如何被别人相信？《信任力》开放书稿与V0.2改版阅读站。",
  cleanUrls: true,
  lastUpdated: true,
  sitemap: { hostname: siteUrl },
  head: [
    ["meta", { name: "theme-color", content: "#b42318" }],
    ["meta", { name: "author", content: "任国刚、钟沈军、吴鹏" }],
    ["meta", { name: "keywords", content: "信任力,AI时代,人机共生,三层五真,GEO,信任飞轮" }]
  ],
  themeConfig: {
    logo: "/ai-symbiosis-logo.png",
    siteTitle: "信任力",
    nav: [
      { text: "首页", link: "/" },
      { text: "V0.2结构", link: "/00-V0.2三部十二章目录" },
      { text: "V0.1书稿", link: "/00-封面" },
      { text: "GitHub", link: repository }
    ],
    sidebar: [
      {
        text: "V0.2改版",
        collapsed: false,
        items: [
          { text: "三部十二章目录", link: "/00-V0.2三部十二章目录" }
        ]
      },
      {
        text: "V0.1完整书稿",
        collapsed: true,
        items: [
          { text: "封面与全书目录", link: "/00-封面" },
          { text: "前言 · 信任缘起", link: "/01-前言 信任缘起AI时代品牌竞争新规则" },
          { text: "核心术语释义", link: "/02-全书核心术语释义" },
          { text: "范式崩塌", link: "/03-范式崩塌" },
          { text: "信任之力", link: "/04-信任之力" },
          { text: "旅程重构", link: "/05-旅程重构" },
          { text: "GEO之战", link: "/06-GEO之战" },
          { text: "信任之基", link: "/07-信任之基" },
          { text: "飞轮效应", link: "/08-飞轮效应AI驱动的信任自增强系统" },
          { text: "度量之道", link: "/09-度量之道" },
          { text: "组织之力", link: "/10-组织之力" },
          { text: "生态之力", link: "/11-生态之力" },
          { text: "未来已来", link: "/12-未来已来" },
          { text: "结语 · 认知主权", link: "/13-结语 认知主权" },
          { text: "附录 · 落地工具", link: "/14-附录 落地工具" }
        ]
      }
    ],
    search: { provider: "local" },
    outline: { level: [2, 3], label: "本页目录" },
    docFooter: { prev: "上一篇", next: "下一篇" },
    lastUpdated: { text: "最后更新" },
    editLink: {
      pattern: `${repository}/edit/${editBranch}/book/:path`,
      text: "在GitHub上改进此页"
    },
    socialLinks: [{ icon: "github", link: repository }],
    footer: {
      message: "AI共生岛丛书 · 开放阅读与共同写作",
      copyright: "《信任力》任国刚、钟沈军、吴鹏 合著"
    }
  }
});
