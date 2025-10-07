from textnode import TextNode, TextType


def main():
    node = TextNode("lorem ipsum", TextType.LINK, "https://boot.dev")
    print(node)


if __name__ == "__main__":
    main()
