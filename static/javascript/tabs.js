function openPage(pageName, element, color) {
  // Hide all elements with class="tabcontent" by default */
  let i, tabcontent;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";

  }
  tablinks = document.getElementsByClassName("tabbtn");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }

  // Show the specific tab content
  document.getElementById(pageName).style.display = "block";

  // Add the specific color to the button used to open the tab content
  element.style.backgroundColor = "#00ad9c";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
