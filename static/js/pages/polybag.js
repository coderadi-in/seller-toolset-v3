// ==================================================
// FADE IN/OUT PAGE
// ==================================================

// ? IMPORTING OBSERVER
import { observer } from '../base/observer.js';

// ? GETTING SECTION ELEMENTS
const inputSection = document.querySelector('.inputs');
const outputSection = document.querySelector('.outputs');

// & PREPARING OBSERVABLES ARRAY
const observables = [inputSection, outputSection];

// & OBSERVING SECTIONS
observables.forEach((observable) => {
    observer.observe(observable);
})

// ==================================================
// GETTING DOC ELEMENTS
// ==================================================

// ? INPUTS
const lengthInput = document.getElementById('productLength');
const widthInput = document.getElementById('productWidth');
const heightInput = document.getElementById('productHeight');

// ? ACTIONS
const calcBtn = document.getElementById("calcBtn");
const resBtn = document.getElementById("resBtn");

// ? OUTPUTS
const lengthOutput = document.getElementById('lengthOutput');
const heightOutput = document.getElementById('heightOutput');

// ==================================================
// FUNCTIONS
// ==================================================

// * FUNCTION TO CALCULATE POLYBAG SIZE
function calculatePolyBagSize(
    productLength,
    productWidth,
    productHeight
) {
    // CALCULATE OUTPUT
    let outputLength = productLength + productHeight + 1;
    let outputHeight = productWidth + productHeight + 1;

    // RETURN OUTPUT
    return {
        l: outputLength,
        h: outputHeight
    }
}

// ==================================================
// EVENT LISTENERS
// ==================================================

// & EVENT LISTENER FOR CALCULATE BUTTON CLICK
calcBtn.addEventListener('click', () => {
    // ACCESS VALUES
    const productLength = parseFloat(lengthInput.value || 0);
    const productWidth = parseFloat(widthInput.value || 0);
    const productHeight = parseFloat(heightInput.value || 0);

    // CALCULATE POLYBAG SIZE
    const polyBagSize = calculatePolyBagSize(
        productLength,
        productWidth,
        productHeight,
    );

    // UPDATE OUTPUT
    lengthOutput.textContent = `${polyBagSize.l} inches`;
    heightOutput.textContent = `${polyBagSize.h} inches`;
});

// & EVENT LISTENER FOR RESET BUTTON CLICK
resBtn.addEventListener('click', () => {
    // RESET INPUT
    lengthInput.value = '';
    widthInput.value = '';
    heightInput.value = '';

    // RESET OUTPUT
    lengthOutput.textContent = '0 inches';
    heightOutput.textContent = '0 inches';
});