import { ElementContent, Root as HTMLRoot } from "hast"

import { Options } from "vfile"
import { QuartzTransformerPlugin } from "../types"
import { visit } from "unist-util-visit"
import path from "path"
import { readFileSync } from "fs"
import rehypeParse from "rehype-parse"
import { rehype } from "rehype"
import { resolveRelative } from "../../util/path"

export const Image: QuartzTransformerPlugin<Partial<Options> | undefined> = (userOpts) => {
  return {
    name: "Image",
    htmlPlugins(ctx) {
      return [
        () => {
          return async (tree: HTMLRoot, file) => {
            visit(tree, "element", (node) => {
              if (node.tagName === "img" && (node.properties?.src as string).includes(".svg")) {
                const src = node.properties?.src as string
                const startIndex = src.indexOf("images")
                const absolutePath = path.resolve(`content/${src.slice(startIndex)}`)
                const svgString = readFileSync(absolutePath).toString()
                const parser = rehype().use(rehypeParse, { fragment: true })
                const svgElement = parser.parse(svgString).children[0] as ElementContent
                delete (svgElement as any).properties.width
                delete (svgElement as any).properties.height
                node.tagName = "div"
                node.properties = {
                  class: "excalidraw-svg",
                }

                visit(svgElement, "element", (node) => {
                  if (node.tagName === "a") {
                    const herf = node.properties.href as string
                    const targetName = herf.slice(2, -2)
                    const targetSlug = ctx.allSlugs.find((slug) => slug.endsWith(targetName))
                    node.properties.href = resolveRelative(file.data.slug!, targetSlug!)
                  }
                })
                node.children = [svgElement]
              }
            })
          }
        },
      ]
    },
  }
}
