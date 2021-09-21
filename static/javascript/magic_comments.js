

function addComment(menu) {
    let divShow = document.getElementById(menu)
    if (divShow.style.display === "none") {
        divShow.style.display = "flex"
    }
    else {
        divShow.style.display = "none"
    }
}
let defaultList = []
function returnDefault(list) {
    defaultList = list
    return list
}

document.getElementById("djContent").addEventListener("mousedown", highlightText)
document.getElementById("djContent").addEventListener("mouseup", function () {
    showCommentContainer("flex")
    //getCoordinates()
    // removeHighlight()
})

function removeHighlight() {
    window.getSelection().empty()
}

function showCommentContainer (display) {
    let cc = document.getElementById("commentContainer")
    cc.style.display = display
}

let yClick = 0

function getCoordinates() {
    //let yClick = event.clientY
    console.log(yClick)
    yClick = event.clientY
    //return yClick
}
let spanId = 0
function highlightText() {
    let selection = window.getSelection();
    let range = selection.getRangeAt(0);
    console.log(range)
    let newNode = document.createElement("span");
    newNode.setAttribute("style", "background-color: pink;");
    newNode.id = "highlight" + spanId.toString()
    newNode.className = "highlightedText"
    spanId += 1
    range.surroundContents(newNode);
    getCoordinates()
    removeHighlight()
}

function loadList(list) {
    let mainList = list
    //removeHighlight()
    let divMenu = document.getElementById("commentContainer")
    //console.log("Running")
    //let list2 = JSON.parse(list)
    let btnContainer = document.createElement("div")
    //console.log(list)
    removeBtns()
    let backBtn = document.createElement("button")
    backBtn.onclick = function () {
        loadList(defaultList)
    }
    backBtn.innerText = "Back"
    backBtn.className = "subBtn"
    divMenu.append(backBtn)
    let stubs = []
        for (const[k, v] of list.entries()) {
            if (v["children"]) {
                //console.log(v["name"])
                //consonale.log(v['name'])
                let newBtn = document.createElement("button")
                // $(newBtn).button("option", "label", v['fields']['name'])
                newBtn.innerText = v['name']
                newBtn.className = "subBtn"
                $(divMenu.append(newBtn))
                //console.log(v['children'])
                newBtn.onclick = function () {
                    loadList(v['children'])
                }
            }
            else {
                //console.log("stubs")
                stubs.push(v)
            }
        }
        loadStubs(stubs)
}

function loadStubs (stubs) {
    //removeBtns()
    //console.log("stubs")
    //console.log(stubs)
    //console.log(stubs.length)
    let divMenu = document.getElementById("commentContainer")
    for (const[k, v] of stubs.entries()) {
        //console.log(k, v)
        let newBtn = document.createElement("button")
        newBtn.className = "subBtn"
        newBtn.innerText = v["questionText"]
        newBtn.onclick = function () {
            createFeedback(v["questionText"])

        }
        $(divMenu.append(newBtn))
    }
}

function createFeedback(qText) {
    // document.getElementById("djContent").removeEventListener("click", getCoordinates)
    let body = document.getElementById("designJournalContainer")
    let comment = document.createElement("div")
    let evalBox = document.getElementById("postedComments")
    comment.className = "commentBox"
    let inputField = document.createElement("textarea")
    inputField.defaultValue = qText
    comment.append(inputField)
    let submit = document.createElement("button")
    submit.value = "Submit"
    submit.className = "submitBtn"
    comment.append(submit)
    submit.textContent = "Submit"
    let postedComment = document.createElement("div")
        postedComment.className = "postedComment"

    body.append(comment)
    submit.onclick = function () {

        postedComment.textContent = inputField.value
        evalBox.append(postedComment)
        let idToGet = spanId
        postedComment.id = "pC" + spanId.toString()

        //postedComment.style.top = yClick.toString() + "px"
        comment.remove()
        removeBtns()
        loadList(defaultList)
        showCommentContainer("none")
        // document.getElementById("djContent").addEventListener("click", getCoordinates)
        //
    }
}

function connectComment(id) {
    let comment = document.getElementById(id)
    comment.style.border = "red 1pt solid"
}

function removeBtns() {
    let btns = document.getElementsByClassName("subBtn")
    $(btns).remove()
}