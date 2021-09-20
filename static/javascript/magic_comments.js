

function addComment(menu) {
    let divShow = document.getElementById(menu)
    if (divShow.style.display === "none") {
        divShow.style.display = "flex"
    }
    else {
        divShow.style.display = "none"
    }
}

function returnDefault(list) {
    return list
}

function loadList(list) {
    let mainList = list
    let divMenu = document.getElementById("commentContainer")
    //console.log("Running")
    //let list2 = JSON.parse(list)
    let btnContainer = document.createElement("div")
    //console.log(list)
    removeBtns()
    let backBtn = document.createElement("button")
    backBtn.onclick = function () {
        loadList(mainList)
    }
    backBtn.innerText = "Back"
    backBtn.className = "subBtn"
    divMenu.append(backBtn)
    let stubs = []
        for (const[k, v] of list.entries()) {
            if (v["children"]) {
                console.log(v["name"])
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
                console.log("stubs")
                stubs.push(v)
            }
        }
        loadStubs(stubs)


}

function loadStubs (stubs) {
    //removeBtns()
    console.log("stubs")
    console.log(stubs)
    //console.log(stubs.length)
    let divMenu = document.getElementById("commentContainer")
    for (const[k, v] of stubs.entries()) {
        console.log(k, v)
        let newBtn = document.createElement("button")
        newBtn.innerText = v["questionText"]
        newBtn.onclick = function () {
            createFeedback(v["questionText"])
        }
        $(divMenu.append(newBtn))
    }
}

function createFeedback(qText) {
    let body = document.getElementById("designJournalContainer")
    let comment = document.createElement("div")
    let evalBox = document.getElementById("commentContainer")
    comment.className = "commentBox"
    let inputField = document.createElement("textarea")
    inputField.defaultValue = qText
    comment.append(inputField)
    let submit = document.createElement("button")
    submit.value = "Submit"
    comment.append(submit)
    submit.textContent = "Submit"
    let postedComment = document.createElement("div")
        postedComment.className = "postedComment"

    body.append(comment)
    submit.onclick = function () {

        postedComment.textContent = inputField.value
        evalBox.append(postedComment)
        comment.remove()
    }
    //comment.innerText = qText


}

function removeBtns() {
    let btns = document.getElementsByClassName("subBtn")
    $(btns).remove()
}