// ==================================================
// FADE IN/OUT ANIMATION
// ==================================================

// ? IMPORTING OBSERVER
import { observer } from '../base/observer.js';

// ? GETTING SECTION ELEMENTS
const generatorSection = document.querySelector('.generator');

// & OBSERVING SECTIONS
observer.observe(generatorSection);

// ==================================================
// FORM SUBMISSION EFFECT
// ==================================================

// ? GETTING DOC ELEMENTS
const form = document.querySelector('.form');
const submitBtn = document.getElementById('genBtn');
const submitBtnContent = document.querySelector("#genBtn span");

// & EVENT LISTENER FOR SUBMIT BUTTON
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI START STATE
    submitBtn.disabled = true;
    submitBtnContent.classList.remove('text', 'title');
    submitBtnContent.classList.add('symbol', 'rotate');
    submitBtnContent.textContent = "progress_activity";

    try {
        const formData = new FormData(form);

        const res = await fetch(form.action, {
            method: "POST",
            body: formData
        });

        const blob = await res.blob();

        // TRIGGER DOWNLOAD
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "batch_label.pdf";
        a.click();

        window.URL.revokeObjectURL(url);

    } catch (err) {
        alert("Something went wrong");
    }

    // UI RESET STATE
    submitBtn.disabled = false;
    submitBtnContent.classList.add('text', 'title');
    submitBtnContent.classList.remove('symbol', 'rotate');
    submitBtnContent.textContent = "Generate Batch";
});