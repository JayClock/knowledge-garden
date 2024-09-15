const { execSync } = require("child_process")
const fs = require("fs")
const path = require("path")

execSync("git clone git@github.com:JayClock/knowledge-graden-blog.git")

// 拷贝文件到仓库 B 的特定目录
const repoBDir = path.join(__dirname, "knowledge-graden-blog")
const contentDir = path.join(__dirname, "content", "Express")
const postsDir = path.join(repoBDir, "source", "_posts")

// 检查是否有文件更新
const hasChanges = fs.readdirSync(contentDir).some((file) => {
  const src = path.join(contentDir, file);
  const dest = path.join(postsDir, file);
  // 如果目标文件不存在，或者内容不同，则认为有更新
  return !fs.existsSync(dest) || !fs.readFileSync(src).equals(fs.readFileSync(dest));
});

if (!hasChanges) {
  console.log("没有代码变更，结束程序");
  process.exit(0);
}

// 确保目标目录存在
if (!fs.existsSync(postsDir)) {
  fs.mkdirSync(postsDir, { recursive: true })
}

// 复制文件
fs.readdirSync(contentDir).forEach((file) => {
  const src = path.join(contentDir, file)
  const dest = path.join(postsDir, file)
  fs.copyFileSync(src, dest)
})

// 移除 hexo 不支持的双链语法
fs.readdirSync(postsDir).forEach((file) => {
  const filePath = path.join(postsDir, file)
  const content = fs.readFileSync(filePath).toString()
  const regex = /(!?)\[\[([^\]]+)\]\]/g
  const matchs = content.match(regex)
  if (matchs && matchs.length) {
    let updatedContent = content
    matchs.forEach((item) => {
      const link = item.substring(2, item.length - 2)
      const final = link.split("|")[1].trim()
      updatedContent = updatedContent.replace(item, final)
    })
    fs.writeFileSync(filePath, updatedContent)
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