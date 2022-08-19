import os
import sys
import re


def read_doc(path):
    with open(path, "r") as fd:
        contents = fd.read()
    return contents


def resolve_inputs(contents, cwd):
    get_input_path = re.compile(r"\\(?:input|include){(.*?)}")

    match = get_input_path.search(contents)
    while match is not None:
        match_path = os.path.join(cwd, match[1])
        match_path = os.path.join(os.path.dirname(match_path), os.path.splitext(
            os.path.basename(match_path))[0] + ".tex")
        match_content = read_doc(match_path)
        match_content = remove_comments(match_content)
        match_content = resolve_inputs(match_content, cwd)
        contents = re.sub(
            get_input_path, lambda x: match_content, contents, count=1)

        match = get_input_path.search(contents)

    return contents


def extract_document_body(doc):
    return re.sub(r"\\begin{document}(.*?)\\end{document}", r"\1", doc, flags=re.DOTALL)


def extract_environments(doc):
    environments = ["itemize", "enumerate"]
    re_extract = re.compile(
        r"\\begin{(" + '|'.join(environments) + r")}(.*?)\\end{\1}", flags=re.DOTALL)

    old_doc = ""
    while doc != old_doc:
        old_doc = doc
        doc = re.sub(re_extract, r"\2", old_doc)

    return doc


def remove_environments(doc):
    return re.sub(r"\\begin{(.*?)}.*?\\end{\1}", "", doc, flags=re.DOTALL)


def remove_commands(doc):
    doc = re.sub(r"\\\w*(?=[\s\\])", "", doc)
    old_doc = ""

    while doc != old_doc:
        old_doc = doc
        doc = re.sub(r"\\[^ \\\n.[\]{}]*(?:{[^{]*?}|\[[^[]*?])+", "", old_doc)

    return doc


def remove_math(doc):
    doc = re.sub(r"\$\$[^$]*?\$\$", "", doc)  # TeX display math
    doc = re.sub(r"\$[^$]*?\$", "", doc)  # TeX inline math
    doc = re.sub(r"\\\[[^$]*?\\]", "", doc)  # LaTeX display math
    doc = re.sub(r"\\\([^$]*?\\\)", "", doc)  # LaTeX inline math
    return doc


def remove_comments(doc):
    return re.sub(r"%.*", "", doc)


def flatten_doc(doc):
    doc = re.sub(r"\n+", " ", doc, flags=re.MULTILINE)  # Remove all newlines
    # Remove all duplicate spaces
    doc = re.sub(r" {2,}", " ", doc, flags=re.MULTILINE)
    return doc


def main():
    mf_path = str(sys.argv[1])  # Main file path
    mf = read_doc(mf_path)

    mf = remove_comments(mf)
    mf = resolve_inputs(mf, os.path.dirname(mf_path))  # Main file contents
    mf = extract_document_body(mf)
    mf = extract_environments(mf)
    mf = remove_environments(mf)
    mf = remove_commands(mf)
    mf = remove_math(mf)
    mf = flatten_doc(mf)
    # print(mf)

    print("N characters (with spaces/punctuation)...: {}".format(len(mf)))
    print("N characters (without spaces/punctuation): {}".format(len(re.sub(r"\W", "", mf))))
    print("N pages (of 2400 characters).............: {:.2f}".format(
        len(mf) / 2400))


if __name__ == "__main__":
    main()
