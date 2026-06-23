document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const button = document.querySelector("button");

    form.addEventListener("submit", function () {

        button.innerHTML = "🤖 AI is Predicting...";
        button.disabled = true;

    });

});

  window.onload = function () {

    const prediction = document.querySelector(".prediction-card");

    if (prediction) {

        document.querySelector("form").reset();

    }

};

