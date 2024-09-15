const { execSync } = require("child_process")
const fs = require("fs")
const path = require("path")

execSync("git clone git@github.com:JayClock/knowledge-graden-blog.git")

// 拷贝文件到仓库 B 的特定目录
const repoBDir = path.join(__dirname, "knowledge-graden-blog")
const contentDir = path.join(__dirname, "content", "Express")
const postsDir = path.join(repoBDir, "source", "_posts")

execSync("git config core.quotepath false")

// 获取 commit 变更的文件列表
const filesChanged = execSync(`git show HEAD --name-only`)
  .toString()
  .trim()
  .split("\n")
  .filter((file) => file.includes("Express"))
  .map((file) => file.split("/Express/")[1].trim())

// 如果 Express 没有代码变更，则直接退出
if (filesChanged.length === 0) {
  console.log("没有输出变更")
  process.exit(0)
}

filesChanged.forEach((fileName) => {
  const src = path.join(contentDir, fileName)
  const dest = path.join(postsDir, fileName)
  const content = fs.readFileSync(src).toString()
  const regex = /(!?)\[\[([^\]]+)\]\]/g
  const matchs = content.match(regex)
  if (matchs && matchs.length) {
    let updatedContent = content
    matchs.forEach((item) => {
      const link = item.substring(2, item.length - 2)
      const final = link.split("|")[1].trim()
      updatedContent = updatedContent.replace(item, final)
    })
    fs.writeFileSync(dest, updatedContent)
  }
})

// 切换到仓库 B 目录
process.chdir(repoBDir)

// 添加更改
execSync("git add .")

// 提交更改
execSync('git commit -m "Sync content knowledge-graden"')

// 推送更改到仓库 B
execSync("git push origin main")
