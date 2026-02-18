// ==================================================
// FADE IN/OUT ANIMATION
// ==================================================

// ? IMPORTING OBSERVER
import { observer } from '../base/observer.js';

// ? GETTING SECTION ELEMENTS
const calculatorSection = document.querySelector('.calculator');

// & PREPARING OBSERVABLES ARRAY
const observables = [calculatorSection];

// & OBSERVING ELEMENTS
observables.forEach((observable) => {
    observer.observe(observable);
});

// ==================================================
// FUNCTIONS
// ==================================================

// * FUNCTION TO CALCULATE TOTAL COST
function calculateTotalCost(
    productCost,
    shippingCost,
    packagingCost,
    crLoss,
    rtoLoss,
    adsCost,
) {
    // SUM-UP ALL VALUES
    let c = productCost + shippingCost + packagingCost + crLoss + rtoLoss + adsCost;
    return c;
}

// * FUNCTION TO ADD GST
function addGST(
    spBase,
    gstValue
) {
    let gstToAdd = spBase * gstValue / 100;
    let spFinal = spBase + gstToAdd;

    return {
        spFinal: spFinal,
        gstToAdd: gstToAdd
    }
}

// * FUNCTION TO ADD PLATFORM FEES
function addPlatformFees(
    spBase,
    fees
) {
    let feesDecimalized = fees / 100;
    let spFinal = spBase + (spBase * feesDecimalized);

    return {
        spFinal: spFinal,
        feesDecimalized: spBase * feesDecimalized
    }
}

// * FUNCTION TO ADD DISCOUNTS
function discountify(
    sellingPrice,
    discountValue
) {
    let denominator = 1 - discountValue / 100;
    let listingPrice = sellingPrice / denominator;
    return listingPrice;
}

// ==================================================
// CALCULATOR ELEMENTS
// ==================================================

// ? INPUTS
const productCost = document.getElementById("productCost");
const packagingCost = document.getElementById("packagingCost");
const shippingCost = document.getElementById("shippingCost");
const crLoss = document.getElementById("customerReturn");
const rtoLoss = document.getElementById("rtoLoss");
const adsCost = document.getElementById("adsCost");
const platformFees = document.getElementById("platformFees");
const gst = document.getElementById("gst");
const profitMargin = document.getElementById("profitMargin");
const discount = document.getElementById("discount");

// ? OUTPUTS
const totalCostOutput = document.getElementById("totalCostOutput");
const platformFeesOutput = document.getElementById("platformFeesOutput");
const gstOutput = document.getElementById("gstOutput");
const sellingPriceOutput = document.getElementById("sellingPriceOutput");

// ? ACTIONS
const calcBtn = document.getElementById("calcBtn");
const resBtn = document.getElementById("resBtn");

// ==================================================
// EVENT LISTENERS
// ==================================================

// & EVENT LISTENER FOR CALC-BTN CLICK
calcBtn.addEventListener("click", () => {
    const productCostValue = Number(productCost.value) || 0;
    const packagingCostValue = Number(packagingCost.value) || 0;
    const shippingCostValue = Number(shippingCost.value) || 0;
    const crLossValue = Number(crLoss.value) || 0;
    const rtoLossValue = Number(rtoLoss.value) || 0;
    const adsCostValue = Number(adsCost.value) || 0;
    const platformFeesValue = Number(platformFees.value) || 0;
    const gstValue = Number(gst.value) || 0;
    const profitMarginValue = Number(profitMargin.value) || 0;
    const discountValue = Number(discount.value) || 0;

    // CALCULATE TOTAL COST AND PLATFORM FEES
    let c = calculateTotalCost(
        productCostValue,
        shippingCostValue,
        packagingCostValue,
        crLossValue,
        rtoLossValue,
        adsCostValue,
    );

    // ADD PROFIT
    let spBase = c + profitMarginValue;

    // ADD ADDITIONAL EXPENSE
    let platformAdded = addPlatformFees(spBase, platformFeesValue);
    let gstAdded = addGST(platformAdded.spFinal, gstValue);

    // ADD DISCOUNTS
    let priceAfterDiscount = discountify(gstAdded.spFinal, discountValue);

    // UPDATE OUTPUT
    totalCostOutput.textContent = `\u20B9 ${c.toFixed(2)}`;
    platformFeesOutput.textContent = `\u20B9 ${platformAdded.feesDecimalized.toFixed(2)}`;
    gstOutput.textContent = `\u20B9 ${gstAdded.gstToAdd.toFixed(2)}`;
    sellingPriceOutput.textContent = `\u20B9 ${priceAfterDiscount.toFixed(2)}`;
})

// & EVENT LISTENER FOR RESET-BTN CLICK
resBtn.addEventListener('click', () => {
    productCost.value = "";
    packagingCost.value = "";
    shippingCost.value = "";
    crLoss.value = "";
    rtoLoss.value = "";
    adsCost.value = "";
    platformFees.value = "";
    gst.value = "";
    profitMargin.value = "";
    discount.value = "";

    totalCostOutput.textContent = "\u20B9 0.00";
    platformFeesOutput.textContent = "\u20B9 0.00";
    gstOutput.textContent = "\u20B9 0.00";
    sellingPriceOutput.textContent = "\u20B9 0.00";
})
