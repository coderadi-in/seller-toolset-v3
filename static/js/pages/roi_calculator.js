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

// * FUNCTION TO CALCULATE PROFIT-MARGIN
function calculateProfitMargin(
    productCost,
    sellingPrice
) {
    return (sellingPrice - productCost) / sellingPrice;
}

// * FUNCTION TO CALCULATE BREAK-EVEN ROI
function calculateBEROI(
    profitMargin
) {
    return 1 / profitMargin
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
        summary = "PROFIT";
        classToAdd = "p";
    } else if (roi < beROI) {
        summary = "LOSS";
        classToAdd = "l";
    } else {
        summary = "BREAK-EVEN";
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
const productCost = document.getElementById("productCost");
const sellingPrice = document.getElementById("sellingPrice");
const roiMade = document.getElementById("roiMade");

// ? OUTPUTS
const roiOutput = document.getElementById("roiOutput");
const profitMarginOutput = document.getElementById("profitMarginOutput");
const beROIOutput = document.getElementById("beROIOutput");
const roiDifferentOutput = document.getElementById("roiDifferentOutput");
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
    const productCostValue = Number(productCost.value) || 0;
    const sellingPriceValue = Number(sellingPrice.value) || 0;
    const roiMadeValue = Number(roiMade.value) || 0;

    // IMPLEMENT MATH
    let calculatedPM = calculateProfitMargin(productCostValue, sellingPriceValue);
    let calculatedBEROI = calculateBEROI(calculatedPM);
    let calculatedSummary = calculateDiff(roiMadeValue, calculatedBEROI);

    // UPDATE OUTPUT
    roiOutput.textContent = roiMadeValue.toFixed(2);
    profitMarginOutput.textContent = calculatedPM.toFixed(2);
    beROIOutput.textContent = calculatedBEROI.toFixed(2);
    roiDifferentOutput.textContent = calculatedSummary.diff.toFixed(2);
    overallOutput.textContent = calculatedSummary.summary;

    roiDifferentOutput.classList.add(calculatedSummary.classToAdd);
    overallOutput.classList.add(calculatedSummary.classToAdd);
})

// & EVENT LISTENER FOR RESET-BTN CLICK
resBtn.addEventListener('click', () => {
    productCost.value = '';
    sellingPrice.value = '';
    adsCost.value = '';
    revenueMade.value = '';

    roiOutput.textContent = '\u20B9 0.00'
    profitMarginOutput.textContent = '0.00'
    beROIOutput.textContent = '0.00'
    roiDifferentOutput.textContent = '0.00'
    overallOutput.textContent = 'NaN'
})