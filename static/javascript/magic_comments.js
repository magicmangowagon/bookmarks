let djPageIndex = 0
let djPages = document.getElementsByClassName("djPage")

function next() {
    if (djPageIndex < djPages.length - 1) {
        djPageIndex++
        paginateDesignJournal(djPageIndex)
    }
}

function previous() {
    if (djPageIndex > 0) {
        djPageIndex--
        paginateDesignJournal(djPageIndex)
    }
}
function paginateDesignJournal(num) {

    $(djPages).hide()
    $(djPages[num]).show()
}

function show(elem) {
    let element = document.getElementById(elem)
    element.style.display = "Block"
    saveText()
}

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

document.getElementById("djContent").addEventListener("mousedown", function(){
    highlightText()
})
document.getElementById("djContent").addEventListener("mouseup", showAddButton)

function showAddButton () {
    let x = event.clientX
    let y = event.clientY
    //console.log(x, y)
    let addFeedback = document.getElementById("addFeedback")
    let djContent = document.getElementById("djContent")
    let topMath = djContent.clientHeight - y
    addFeedback.style.display = "block"
    addFeedback.style.left = x + "px"
    addFeedback.style.top = y + "px"
}

function removeHighlight() {
    window.getSelection().empty()
}

function showCommentContainer (display) {
    let addFeedbackDiv = document.getElementById("addFeedback")
    addFeedbackDiv.style.display = "none"
    let cc = document.getElementById("commentContainer")
    cc.style.display = display
}

let yClick = 0

function getCoordinates() {
    //let yClick = event.clientY
    //console.log(yClick)
    yClick = event.clientY
    //return yClick
}
let spanId = 0

let highlightColor = {
    'A': '#ffec65',
    'B': 'pink',
    'C': '#63cde8',
    'D': '#12c064'
}

function returnHighlightColor(string) {
    return highlightColor[string]
}

let selectedText = ""

function highlightText() {
    let selection = window.getSelection();
    let range = selection.getRangeAt(0);
    console.log(selection.toString())
    selectedText = selection.toString()
    saveText()
    let newNode = document.createElement("span");
    newNode.setAttribute("style", "background-color: pink;");
    newNode.id = "highlight" + spanId.toString()
    newNode.className = "highlightedText"
    spanId += 1
    range.surroundContents(newNode);
    getCoordinates()
    removeHighlight()
}

function loadConversation(text) {
    let responseForm = document.getElementById("responseForm")
    let initialComment = document.getElementById("initialComment")
    initialComment.innerText = text
    responseForm.style.display = "block"

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

function hideThis (name) {
    let thisThing = document.getElementById(name)
    thisThing.style.display = "none"
    thisThing.addEventListener('mouseup', function (e) {
        e.stopImmediatePropagation()
    })


}

function loadStubs (stubs) {
    //removeBtns()
    //console.log("stubs")
    //console.log(stubs)
    //console.log(stubs.length)
    let divMenu = document.getElementById("commentContainer")
    for (const[k, v] of stubs.entries()) {
        //console.log(k, v)
        let form = document.getElementById("stubForm")
        let newBtn = document.createElement("button")
        newBtn.className = "subBtn"
        newBtn.innerText = v["questionText"]
        newBtn.onclick = function () {
            createFeedback(v["questionText"])
            setContainerValues(v['id'])
            console.log(v['id'])
            saveText()
        }

        $(divMenu.append(newBtn))
    }
}



function addHighlights() {
    console.log("add highlights")
    let oldComments = document.getElementsByClassName("hiddenText")
    let djContent = document.getElementById("djLong")
    for (let i = 0; i < oldComments.length; i++) {
        let regex = new RegExp($(oldComments[i]).text())
        //console.log(regex)
        console.log($(djContent).text().replace().match(regex), regex)
        let category = oldComments[i].getAttribute("data-key").toString()
        let color = returnHighlightColor(category)
        //console.log(djContent.innerText.replace(regex,'<span class="highlight">regex</span>'))
        //$(djContent).text().replace($(djContent).text().match($(oldComments[i]).text()), '<span class="highlight">$(oldComments[i]).text</span>')
        //$(djContent).text().replace(regex, '<span class="highlight">regex</span>')
        //$(djContent).text().replace($(djContent).text().match($(regex), '<span class="highlight">$(regex)</span>'))
        djContent.innerHTML = djContent.innerHTML.replace(regex, '<span style="background-color: ' + color + '">' +  regex + '</span>')
    }
}

function createFeedback(qText) {
    // document.getElementById("djContent").removeEventListener("click", getCoordinates)
    let body = document.getElementById("designJournalContainer")
    let comment = document.createElement("div")
    let evalBox = document.getElementById("postedComments")
    let containerForm = document.getElementById("containerForm")
    containerForm.style.display = "block"
    //comment.className = "commentBox"
    //let inputField = document.createElement("textarea")
    //inputField.defaultValue = qText
    //comment.append(inputField)
    //let submit = document.createElement("button")
    //submit.value = "Submit"
    //submit.className = "submitBtn"
    //comment.append(submit)
    //submit.textContent = "Submit"
    let postedComment = document.createElement("div")
        postedComment.className = "postedComment"

    body.append(comment)

}

function connectComment(id) {
    let comment = document.getElementById(id)
    comment.style.border = "red 1pt solid"
}


function addNewFeedback(los) {
    let parentContainer = document.getElementById("newFeedbackContent")
    let compBtns = document.getElementsByClassName("newFeedbackComp")
    console.log(compBtns)
    $(compBtns).hide()
    let existingBtns = document.getElementsByClassName("newFeedbackBtn")
    $(existingBtns).remove()
    for (const[k, v] of los.entries()) {
        //console.log(v)
        let newBtn = document.createElement("button")
        newBtn.innerText = v["fields"]["name"]
        newBtn.className = "newFeedbackBtn"
        //newBtn.onclick = function () {newFeedbackForm(v["fields"]["name"])}
        //parentContainer.append(newBtn)
    }
}

function newFeedbackForm(name) {
    let existingBtns = document.getElementsByClassName("newFeedbackBtn")
    $(existingBtns).remove()
    let parentContainer = document.getElementById("newFeedbackContent")
    let loName = document.createElement("h4")
    loName.textContent = name
    parentContainer.append(loName)
    let questionType = document.createElement("select")
    let questionText = document.createElement("textarea")
    let stepBack = document.createElement("option")
    stepBack.text = "Step Back"
    let goDeeper = document.createElement("option")
    goDeeper.text = "Go Deeper"
    let tryIt = document.createElement("option")
    tryIt.text = "Try it Out"
    questionType.add(stepBack)
    questionType.add(goDeeper)
    questionType.add(tryIt)
    questionType.className = "newFeedbackBtn"
    questionText.className = "newFeedbackBtn"
    parentContainer.append(questionType)
    parentContainer.append(questionText)
}

function backToComps(className) {
    let compBtns = document.getElementsByClassName("newFeedbackComp")
    let loBtns = document.getElementsByClassName("newFeedbackBtn")
    $(loBtns).remove()
    $(compBtns).show()
}

function removeBtns() {
    let btns = document.getElementsByClassName("subBtn")
    $(btns).remove()
}

let djContent = document.getElementById("djContent")

function highlightSelection() {
    let selection = window.getSelection();
    let userSelection = selection.getRangeAt(0);
    //let userSelection = window.getSelection().getRangeAt(0);
    let safeRanges = getSafeRanges(userSelection);
    for (let i = 0; i < safeRanges.length; i++) {
        highlightRange(safeRanges[i]);
    }
}

function getSafeRanges(dangerous) {
    let a = dangerous.commonAncestorContainer;
    // Starts -- Work inward from the start, selecting the largest safe range
    let s = new Array(0), rs = new Array(0);
    if (dangerous.startContainer !== a)
        for(let i = dangerous.startContainer; i !== a; i = i.parentNode)
            s.push(i)
    ;
    if (0 < s.length) for(let i = 0; i < s.length; i++) {
        let xs = document.createRange();
        if (i) {
            xs.setStartAfter(s[i-1]);
            xs.setEndAfter(s[i].lastChild);
        }
        else {
            xs.setStart(s[i], dangerous.startOffset);
            xs.setEndAfter(
                (s[i].nodeType === Node.TEXT_NODE)
                ? s[i] : s[i].lastChild
            );
        }
        rs.push(xs);
    }

    // Ends -- basically the same code reversed
    let e = new Array(0), re = new Array(0);
    if (dangerous.endContainer !== a)
        for(let i = dangerous.endContainer; i !== a; i = i.parentNode)
            e.push(i)
    ;
    if (0 < e.length) for(let i = 0; i < e.length; i++) {
        let xe = document.createRange();
        if (i) {
            xe.setStartBefore(e[i].firstChild);
            xe.setEndBefore(e[i-1]);
        }
        else {
            xe.setStartBefore(
                (e[i].nodeType === Node.TEXT_NODE)
                ? e[i] : e[i].firstChild
            );
            xe.setEnd(e[i], dangerous.endOffset);
        }
        re.unshift(xe);
    }

    // Middle -- the uncaptured middle
    if ((0 < s.length) && (0 < e.length)) {
        let xm = document.createRange();
        xm.setStartAfter(s[s.length - 1]);
        xm.setEndBefore(e[e.length - 1]);
    }
    else {
        return [dangerous];
    }

    // Concat
    rs.push(xm);
    let response = rs.concat(re);

    // Send to Console
    return response;
}


function setContainerValues(id) {
    let form = document.getElementById("id_comment")
    form.value = id
    let displayPar = document.getElementById("label")
    displayPar.innerText = form.options[form.selectedIndex].text
}

function saveText() {
    let form = document.getElementById("id_highlight")
    form.value = selectedText
    //let displayPar = document.getElementById("label")
    //displayPar.innerText = form.options[form.selectedIndex].text
}
