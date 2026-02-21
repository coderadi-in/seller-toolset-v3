// ? IMPORTING OBSERVER
import { observer } from '../base/observer.js';

// ? GETTING INPUTS
// const totalOrders = document.getElementById("totalOrders");
const totalOrders = 100;
const totalReturn = document.getElementById("totalReturn");
const returnLoss = document.getElementById("returnLoss");
const packagingLoss = document.getElementById("packagingLoss");
const totalRto = document.getElementById("totalRto");
const rtoLoss = document.getElementById("rtoLoss");

// ? GETTING OUTPUTS
const crLossOutput = document.getElementById("crLossOutput");
const rtoLossOutput = document.getElementById("rtoLossOutput");
const totalLossOutput = document.getElementById("totalLossOutput");

// ? GETTING ACTION ELEMENTS [BUTTONS]
const calculateBtn = document.getElementById("calcbtn");
const resetBtn = document.getElementById("resbtn");

// * FUNCTION TO CALCULATE CUSTOMER RETURN
function calculateCRLoss(
    totalOrders,
    totalReturn,
    returnLoss,
    packagingLoss,
    totalRto
) {
    // CONVERT TOTAL RETURN-RATE AND TOTAL RTO-RATE TO DECIMAL
    let totalReturnDecimal = (totalReturn / 100) * totalOrders;
    let totalRtoDecimal = (totalRto / 100) * totalOrders;

    // CALCULATE LOSS
    let output = totalReturnDecimal * (returnLoss + packagingLoss) / (totalOrders - totalReturnDecimal - totalRtoDecimal);
    return output;
}

// * FUNCTION TO CALCULATE RTO LOSS
function calculateRTOLoss(
    totalOrders,
    totalRto,
    rtoLoss,
    packagingLoss,
    totalReturn
) {
    // CONVERT TOTAL RETURN-RATE AND TOTAL RTO-RATE TO DECIMAL
    let totalReturnDecimal = (totalReturn / 100) * totalOrders;
    let totalRtoDecimal = (totalRto / 100) * totalOrders;

    // CALCULATE LOSS
    let output = totalReturnDecimal * (rtoLoss + packagingLoss) / (totalOrders - totalReturnDecimal - totalRtoDecimal);
    return output;
}

// & LOSS CALCULATION FUNCTIONALITY
calculateBtn.addEventListener('click', () => {
    // GET ALL INPUT VALUES
    let totalOrdersValue = totalOrders;
    let totalReturnValue = Number(totalReturn.value) || 0;
    let returnLossValue = Number(returnLoss.value) || 0;
    let packagingLossValue = Number(packagingLoss.value) || 0;
    let totalRtoValue = Number(totalRto.value) || 0;
    let rtoLossValue = Number(rtoLoss.value) || 0;

    // CALCULATE CR LOSS
    const crLossResult = calculateCRLoss(
        totalOrdersValue,
        totalReturnValue,
        returnLossValue,
        packagingLossValue,
        totalRtoValue
    );

    // CALCULATE RTO LOSS
    const rtoLossResult = calculateRTOLoss(
        totalOrdersValue,
        totalRtoValue,
        rtoLossValue,
        packagingLossValue,
        totalReturnValue
    );

    // CALCULATE TOTAL LOSS
    const totalLossResult = crLossResult + rtoLossResult;

    // FORMAT CURRENCY AND SHOW OUTPUT
    const formatCurrency = (value) => `\u20B9 ${value.toFixed(2)}`;
    crLossOutput.textContent = formatCurrency(crLossResult);
    rtoLossOutput.textContent = formatCurrency(rtoLossResult);
    totalLossOutput.textContent = formatCurrency(totalLossResult);
})

// & RESET FUNCTIONALITY
resetBtn.addEventListener('click', () => {
    // RESET ALL INPUTS
    totalOrders.value = '';
    totalReturn.value = '';
    returnLoss.value = '';
    packagingLoss.value = '';
    totalRto.value = '';
    rtoLoss.value = '';

    // RESET ALL OUTPUTS
    crLossOutput.textContent = '\u20B9 0.00';
    rtoLossOutput.textContent = '\u20B9 0.00';
    totalLossOutput.textContent = '\u20B9 0.00';
})

// ? GETTING SECTION ELEMENTS
const calculatorSection = document.querySelector('.calculator');

// & PREPARING OBSERVABLES ARRAY
const observables = [calculatorSection];

// & OBSERVING ELEMENTS
observables.forEach((observable) => {
    observer.observe(observable)
})

