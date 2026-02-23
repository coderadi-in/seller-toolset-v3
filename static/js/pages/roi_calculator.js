// ==================================================
// FADE IN/OUT ANIMATION
// ==================================================

// ? IMPORTING OBSERVER
import { observer } from '../base/observer.js';

// ? GETTING SECTION ELEMENTS
const calculatorSection = document.querySelector('.calculator');

// & OBSERVING SECTIONS
observer.observe(calculatorSection);

// ==================================================
// FUNCTIONS
// ==================================================

// * FUNCTION TO CALCULATE PROFIT MARGIN
function calculatePM(
    profitMargin,
    sellingPrice
) {
    let value = (profitMargin / sellingPrice);
    return isNaN(value) ? 0 : value.toFixed(2);
}

// * FUNCTION TO CALCULATE BREAK-EVEN ROI
function calculateBEROI(
    profitMargin
) {
    let beROI = 1 / profitMargin;
    return isNaN(beROI) ? 0 : beROI.toFixed(2);
}

// * FUNCTION TO CALCULATE ROI DIFF. AND SUMMARY
function calculateDiff(
    roi,
    beROI
) {
    // CALCULATE DIFFERENCE
    let diff = roi - beROI;
    let summary = "NaN";
    let classToAdd = "be";

    // CALCULATE SUMMARY
    if (roi > beROI) {
        summary = "Profitable ROI";
        classToAdd = "p";
    } else if (roi < beROI) {
        summary = "Loss Making ROI";
        classToAdd = "l";
    } else {
        summary = "Needs Optimization (No profit No Loss)";
        classToAdd = "be";
    }

    // RETURN OUTPUT
    return {
        diff: diff,
        summary: summary,
        classToAdd: classToAdd
    }
}

// ==================================================
// ACCESS ELEMENTS
// ==================================================

// ? INPUTS
const profitMargin = document.getElementById("profitMargin");
const sellingPrice = document.getElementById("sellingPrice");
const roiMade = document.getElementById("roiMade");

// ? OUTPUTS
const overallOutput = document.getElementById("overallOutput");

// ? ACTIONS
const calcBtn = document.getElementById("calcBtn");
const resBtn = document.getElementById("resBtn");

// ==================================================
// WORKFLOW IMPLEMENTATION
// ==================================================

// & EVENT LISTENER FOR CALCULATE-BTN CLICK
calcBtn.addEventListener('click', () => {
    // FETCH VALUE
    const profitMarginValue = Number(profitMargin.value) || 0;
    const sellingPriceValue = Number(sellingPrice.value) || 0;
    const roiMadeValue = Number(roiMade.value) || 0;

    // IMPLEMENT MATH
    let calculatedPM = calculatePM(profitMarginValue, sellingPriceValue);
    let calculatedBEROI = calculateBEROI(calculatedPM);
    let calculatedSummary = calculateDiff(roiMadeValue, calculatedBEROI);

    // UPDATE OUTPUT
    overallOutput.textContent = calculatedSummary.summary;

    overallOutput.classList.remove('p', 'l', 'be');
    overallOutput.classList.add(calculatedSummary.classToAdd);
})

// & EVENT LISTENER FOR RESET-BTN CLICK
resBtn.addEventListener('click', () => {
    productCost.value = '';
    sellingPrice.value = '';
    roiMade.value = '';

    overallOutput.textContent = 'NaN'
    overallOutput.classList.remove('p', 'l', 'be');
})