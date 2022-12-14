#fait par Alex
from io import TextIOWrapper
from iiwServerHelperv2 import *
from os import listdir


def create404Page(path: str) -> str:
    return """<!DOCTYPE html>
<html>

<head>
<link href="./monCSS.css" rel="stylesheet"/>
    <meta charset="uft-8">
    <title>404 Page not found</title>
</head>

<body>
    <h1>Error 404</h1>
    <h2>Page not found</h2>
    <p>Votre page na pas pu être trouver</p>
    <br>
    <p>Retour a la page d'acceuil <a href="/">ici</a></p>
</body>

</html>"""


def getFileExtension(path: str) -> str:
    tempo2: str = str("")
    for i in range(len(path) - 1, -1, -1):
        tempo2 = path[i] + tempo2
        if path[i - 1] == ".":
            return tempo2
    return "error"


# print(getFileExtension("eghfdgjjhjhg... erg.oij.ert.webp"))


def getContentType(extension: str) -> str:
    if extension == "html" or extension == "css" or extension == "csv":
        return "text/" + extension
    if extension == "png" or extension == "jpeg" or extension == "gif" or extension == "webp":
        return "image/" + extension
    if extension == "txt":
        return "text/plain"
    if extension == "jpg":
        return "image/jpeg"
    else:
        return "NoneType"


def isBinaryFile(contenttype: str) -> bool:
    prefixe = contenttype[0:5]
    return prefixe == "image"


def getPostFilePath(path: str) -> str:
    return "./posts" + path + ".txt"


def getPostTitle(postpath: str) -> str:
    if doesFileExist(postpath):
        f = open(postpath, "r", encoding="utf-8")
        alllines = f.readlines()
        try:
            return alllines[0]
        except:
            return "post doesnt exist"
    return "post doesnt exist"


def getPostContent(postpath: str) -> str:
    if doesFileExist(postpath):
        f: TextIOWrapper = open(postpath, "r", encoding="utf-8")
        alllines: list[str] = f.readlines()
        alltext: str = str()
        for i in range(1, len(alllines)):
            alltext += alllines[i]
        return alltext
    return "error"


# a = """**test**
# ca marche?**
# oui**
# non?"""

# print(a)


def addHtmlParagraphs(text: str) -> str:
    text = text.replace("\n", "</p><p>")
    return "<p>" + text + "</p>"


def addHtmlBold(text: str) -> str:
    while "**" in text:
        text = text.replace("**", "<strong>", 1)
        text = text.replace("**", "</strong>", 1)
    return text


def addHtmlItalic(text: str) -> str:
    while "//" in text:
        text = text.replace("//", "<i>", 1)
        text = text.replace("//", "</i>", 1)
    return text


def addHtmlImage(text: str) -> str:
    while "##" in text:
        text = text.replace("##", '<img src="', 1)
        text = text.replace("##", '"/>', 1)
    return text


def addSpecificFormattingv1(text: str) -> str:
    return addHtmlBold(addHtmlItalic(addHtmlImage(addHtmlParagraphs(text))))



def createBlogPage(titre: str, page: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link href="./monCSS.css" rel="stylesheet"/>
    <title>{titre}</title>
</head>
<body>
<h1>{titre}</h1>
    {page}
</body>
</html>"""


def removeExtension(name: str) -> str:
    for i in range(len(name) - 1, -1, -1):
        if name[i] == ".":
            return name[0:i]
    return "error"


def askExtension(path: str) -> bool:
    for i in range(len(path)):
        if path[i] == ".":
            return True
    return False


# print(removeExtension("test.test.test.txt"))


def createListofAnchor() -> str:
    listeelement: list[str] = listdir("./posts")
    listeelement.remove("temp")
    listeelement.remove("error.txt")
    listeanchor: str = ""
    for i in range(len(listeelement)):
        listeanchor += '<li><a href="%s">%s</a></li></br>' % (str(removeExtension(listeelement[i])), removeExtension(listeelement[i]))
    return "<ul>" + listeanchor + "</ul>"


def createIndexPage(body: str) -> str:
    return f"""<!DOCTYPE html>
<html>

<head>
    <title>Ma page personnel</title>
    <meta charset=" utf8" />
    <link href="./monCSS.css" rel="stylesheet"/>

</head>

<body>
    <h1>
        Index de blog fait par Alex
    </h1>
    {body}
    <h3><a href="addPost.html">Faire un post</a>
</body>

</html>
    """


# print(createIndexPage(createListofAnchor()))


def search(where: str, path: str) -> str:
    listeelement: list[str] = listdir(where)  #cherche dans ce répertoire
    print(listeelement)
    for i in range(len(listeelement)):
        if path == "/" + listeelement[i]:
            return str(path + listeelement[i])
    return "error"


def handlePostRequest(post: list[PostedData]) -> None:
    # print(post)
    content: TextIOWrapper = open("./posts/error.txt")
    file = ""
    filename = ""
    # [PostedData(name='title', value='testest'), PostedData(name='content', value='test'), PostedData(name='pictureFileName', value=''), PostedData(name='pictureFile', value=b'')]
    for i in range(len(post)):
        print(post)
        if post[i].name == "title":
            titre: str = post[i].value
            titre: str = titre.replace(" ", "-")
            content = open("./posts/%s.txt" % (titre), "w", encoding="UTF-8")
        if post[i].name == "content":
            body: str = post[i].value
            content.write(body)
        if post[i].name == "pictureFileName":
            post[i].name=post[i].name.replace(" ","-")
            filename: str = post[i].value
        if post[i].name == "pictureFile":
            file = post[i].value
    if not doesFileExist("./posts/temp/%s" % (filename)):
        picture = open("./posts/temp/%s" % (filename), "wb")
        picture.write(file)  #type:ignore
    texte: str = content.name
    textesplit = texte.split("##")
    for i in range(len(textesplit)):
        if textesplit[i] == filename:
            texte.replace(filename, "./posts/temp/%s" % (filename))
            content.write(texte)

    fileSend = createIndexPage(createListofAnchor())
    sendResponse(200)
    sendHeader("Content-Type", "text/html")
    sendTextualFileContent(fileSend)


def handleGetRequest(path: str) -> None:
    print(path)
    pathtofile = ""
    if path == "/" or path == "":
        path = "index.html"

    if askExtension(path) == False:
        listeelement: list[str] = listdir("./posts")
        print(listeelement)
        for i in range(len(listeelement)):
            if "/" + removeExtension(listeelement[i]) == path:
                path = "./posts/" + listeelement[i]

    if search("./posts/temp", path) != "error":
        path = "./posts/temp" + path

    if not path.startswith("./posts"):
        path = "./html/" + path

    if doesFileExist(path) == True:
        contentType = getContentType(getFileExtension(path))
        mode: str
        pathtofile = path
        if isBinaryFile(contentType) == True:
            mode = 'rb'
            fileContent = open(pathtofile, mode)
            sendResponse(200)
            sendHeader("Content-Type", contentType)
            sendBinaryFileContent(fileContent.read())
            fileContent.close()

        else:
            fileContent = open(pathtofile, 'r', encoding="utf-8")
            fileSend = fileContent.read()

            if contentType == "text/plain":
                contentType = "text/html"
                # fileContent = open(pathtofile,"r")
                # text:str=fileContent.read()
                # print(text)
                Titre = getPostTitle(pathtofile)
                body = getPostContent(pathtofile)
                fileSend = createBlogPage(Titre, addSpecificFormattingv1(body))
                # fileSend=addSpecificFormattingv1(fileContent.read())

            if pathtofile == "./html/index.html":
                fileSend = createIndexPage(createListofAnchor())

            sendResponse(200)
            sendHeader("Content-Type", contentType)
            sendTextualFileContent(fileSend)
            fileContent.close()

    else:
        sendResponse(404)
        sendHeader("Content-Type", "text/html; charset=utf-8")
        sendTextualFileContent(create404Page(path))


setHandlePostRequest(handlePostRequest)
setHandleGetRequest(handleGetRequest)
launchServer("127.0.0.1", 8888)

# ------getFileExtension-Solution---------
#solution 3
#tempo:str=str("")
# for i in range(len(path)):
#     tempo+=path[i-len(path)-1]
#     if path[i-len(path)-1]==".":
#         return tempo

#solution 2
# temp:str=str("")
# for i in range(len(path)):
#     temp+=path[i]
#     if path[i]==".":
#         temp=""
# return temp

#solution 1
# afterpath = False
# extension: str = ""
# for i in range(len(path)):
#     if path[i] == ".":
#         afterpath = True
#     elif afterpath == True:
#         extension = extension+path[i]
# return extension

# boolean:bool=False
# for i in range(len(text)):
#     if boolean==False:
#         text=text.replace("**","<strong>",1)
#         boolean:bool=True
#     else:
#         text=text.replace("**","</strong>",1)
#         boolean:bool=False
# return text

# ------addHtml-Solution---------
# def addHtmlParagraphs(text:str)->str:
#     paragraphe=text.split("/n")
#     for i in paragraphe:
#         textparagraphe:str=textparagraphe+i+"</p><p>"
#     return "<p>"+textparagraphe+"</p>"

# def addHtmlBold(text:str)->str:
#     gras=text.split("**")
#     for i in range(1,len(gras),2):
#         textgras:str=gras[i-1]+"<strong>"+gras[i]+"</strong>"
#     return textgras

# def addHtmlItalic(text:str)->str:
#     boolean:bool=False
#     for i in range(len(text)):
#         if boolean==False:
#             text=text.replace("//","<i>",1)
#             boolean:bool=True
#         else:
#             text=text.replace("**","</i>",1)
#             boolean:bool=False
#     return text

# def addHtmlImage(text:str)->str:
#     boolean:bool=False
#     for i in range(len(text)):
#         if boolean==False:
#             text.replace("##",'<img src="',1)
#             boolean:bool=True
#         else:
#             text.replace("##",'"/>',1)
#             boolean:bool=False
#     return text

    # balise:str=""
    # format:str=""
    # b:bool=False
    # for i in range(len(text)):
    #     if text[i:i+1]=="**":
    #         format:str="**"
    #         balise:str="strong"
    #     if text[i:i+1]=="//":
    #         format:str="//"
    #         balise:str="i"
    #     if b==False:
    #         text=text.replace(format,"<"+balise+">",1)
    #         b:bool=True
    #     else:
    #         text=text.replace(format,"</"+balise+">",1)
    #         b:bool=False
    # return text


# print(addHtmlBold("zaza **gras ** **zozo**toto"))

# if extension == "html":
#     return "text/html"
# if extension == "css":
#     return "text/css"
# if extension == "csv":
#     return "text/csv"
# if extension == "txt":
#     return "text/plain"
# if extension == "png":
#     return "image/png"
# if extension == "jpeg":
#     return "image/jpeg"
# if extension == "jpg":
#     return "image/jpeg"
# if extension == "gif":
#     return "image/gif"
# if extension == "webp":
#     return "image/webp"
# else:
#     return "text/html"
