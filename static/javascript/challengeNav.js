
function challengeNavShow (challenge) {
    let elementID = document.getElementById(challenge);
    $(elementID).toggle(150);
}

function collapseMegaChallenge () {
    let challenges = document.getElementsByClassName("subChallenge")
    let i = 1
    for (i; i < challenges.length; i++){
        challenges[i].style.display = 'none'
    }
}

function collapseSubSection (currentExpo) {
    let expoList = document.getElementsByClassName("anExpo")
    console.log(expoList)
    let currentIndex = expoList.indexOf(currentExpo)
    console.log(currentIndex)
    return expoList[currentIndex +1]
}