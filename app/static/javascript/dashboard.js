document.addEventListener("DOMContentLoaded", function () {
    // Select the scroll buttons
    const scrollLeftButton = document.getElementById("scrollLeft");
    const scrollRightButton = document.getElementById("scrollRight");

    // Add click event listeners to the buttons
    scrollLeftButton.addEventListener("click", scrollLeft);
    scrollRightButton.addEventListener("click", scrollRight);

    // Function to scroll to the left
    function scrollLeft() {
      document.querySelector(".table_section").scrollLeft -= 50;
    }

    // Function to scroll to the right
    function scrollRight() {
      document.querySelector(".table_section").scrollLeft += 50;
    }
  });