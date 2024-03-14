import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/header.scss"

const Header: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return children.length > 0 ? <header class="page-bg">{children}</header> : null
}

Header.css = style

export default (() => Header) satisfies QuartzComponentConstructor
